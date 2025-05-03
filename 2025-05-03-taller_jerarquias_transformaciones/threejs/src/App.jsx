import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { useControls } from 'leva'
import './App.css'

// Parent component that contains child objects
function HierarchyGroup() {
  // Create controls for parent transformations using Leva
  const parentControls = useControls('Parent Transformations', {
    rotationX: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    rotationY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    rotationZ: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    positionX: { value: 0, min: -5, max: 5, step: 0.1 },
    positionY: { value: 0, min: -5, max: 5, step: 0.1 },
    positionZ: { value: 0, min: -5, max: 5, step: 0.1 },
  })

  // Child controls
  const childControls = useControls('Child Transformations', {
    childRotationY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    childDistance: { value: 2, min: 1, max: 4, step: 0.1 },
  })

  // Grandchild controls
  const grandchildControls = useControls('Grandchild Transformations', {
    grandchildRotationZ: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    grandchildDistance: { value: 1, min: 0.5, max: 2, step: 0.1 },
  })

  return (
    // Parent Group - all transformations applied here affect children
    <group
      position={[
        parentControls.positionX,
        parentControls.positionY,
        parentControls.positionZ,
      ]}
      rotation={[
        parentControls.rotationX,
        parentControls.rotationY,
        parentControls.rotationZ,
      ]}
    >
      {/* Parent object - red cube */}
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color='red' />
      </mesh>

      {/* Child Group - affected by parent transformations + its own */}
      <group
        position={[childControls.childDistance, 0, 0]}
        rotation={[0, childControls.childRotationY, 0]}
      >
        {/* Child object - green sphere */}
        <mesh>
          <sphereGeometry args={[0.7, 32, 16]} />
          <meshStandardMaterial color='green' />
        </mesh>

        {/* Grandchild Group - affected by parent and child transformations + its own */}
        <group
          position={[grandchildControls.grandchildDistance, 0, 0]}
          rotation={[0, 0, grandchildControls.grandchildRotationZ]}
        >
          {/* Grandchild object - blue cylinder */}
          <mesh>
            <cylinderGeometry args={[0.3, 0.3, 1, 32]} />
            <meshStandardMaterial color='blue' />
          </mesh>
        </group>
      </group>
    </group>
  )
}

function App() {
  return (
    <div className='App'>
      <h1>Hierarchical Transformations</h1>
      <div className='scene-container'>
        <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <directionalLight position={[10, 10, 5]} intensity={1} />
          <HierarchyGroup />
          <OrbitControls />
          <axesHelper args={[5]} />
          <gridHelper />
        </Canvas>
      </div>
    </div>
  )
}

export default App
