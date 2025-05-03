import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import './App.css'

function MultiColorTorusKnot() {
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame(({ clock }) => {
    if (!groupRef.current) return
    
    const elapsedTime = clock.getElapsedTime()
    
    // Translate along a sinusoidal path
    groupRef.current.position.x = Math.sin(elapsedTime) * 2
    groupRef.current.position.y = Math.cos(elapsedTime) * 2
    
    // Rotate on its own axis
    groupRef.current.rotation.x += 0.01
    groupRef.current.rotation.y += 0.005
    groupRef.current.rotation.z += 0.002
    
    // Scale smoothly using a temporal function
    const scale = 1 + Math.sin(elapsedTime) * 0.2
    groupRef.current.scale.set(scale, scale, scale)
  })
  
  // Create a single torus knot with vertex colors
  const torusKnot = useMemo(() => {
    // Create the color array for the geometry
    const geometry = new THREE.TorusKnotGeometry(0.7, 0.3, 128, 32, 2, 3)
    const colors = []
    const vertexCount = geometry.getAttribute('position').count
    
    // Create 6 color bands around the torus knot
    const colorArray = [
      new THREE.Color("#ff1744"), // Neon red
      new THREE.Color("#ff9500"), // Vibrant orange
      new THREE.Color("#ffea00"), // Bright yellow
      new THREE.Color("#39ff14"), // Neon green
      new THREE.Color("#00aaff"), // Electric blue
      new THREE.Color("#ff00cc"), // Hot pink
    ]
    
    // Assign colors to vertices
    for (let i = 0; i < vertexCount; i++) {
      // Get the vertex position
      const x = geometry.getAttribute('position').getX(i)
      const y = geometry.getAttribute('position').getY(i)
      
      // Calculate angle in XY plane
      const angle = Math.atan2(y, x)
      const normalizedAngle = (angle + Math.PI) / (Math.PI * 2) // normalized to 0-1
      
      // Pick a color based on the angle
      const colorIndex = Math.floor(normalizedAngle * 6) % 6
      const color = colorArray[colorIndex]
      
      // Add the color to the array
      colors.push(color.r, color.g, color.b)
    }
    
    // Create the color attribute
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))
    
    return (
      <mesh castShadow>
        <primitive object={geometry} attach="geometry" />
        <meshPhysicalMaterial
          vertexColors
          roughness={0.0}
          metalness={0.1}
          clearcoat={1.0}
          clearcoatRoughness={0.1}
          emissive="#ffffff"
          emissiveIntensity={0.3}
          reflectivity={1}
        />
      </mesh>
    )
  }, [])
  
  return (
    <group ref={groupRef}>
      {torusKnot}
    </group>
  )
}

function App() {
  return (
    <div className="canvas-container">
      <Canvas camera={{ position: [0, 0, 6] }} shadows>
        <color attach="background" args={['#ffffff']} /> {/* Pure white background */}
        <ambientLight intensity={0.9} />
        <pointLight position={[10, 10, 10]} intensity={1.8} castShadow />
        <pointLight position={[-10, -10, -10]} intensity={1.0} color="#ffffff" />
        <spotLight position={[0, 5, 0]} intensity={0.8} angle={0.5} penumbra={0.5} />
        <MultiColorTorusKnot />
        <OrbitControls />
      </Canvas>
    </div>
  )
}

export default App
