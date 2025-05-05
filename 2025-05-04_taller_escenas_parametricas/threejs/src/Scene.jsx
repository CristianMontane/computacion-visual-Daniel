import React, { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useControls } from 'leva'

function Scene() {
  // define dynamic controls
  const { globalScale, boxColor, rotateAll, rotationSpeed } = useControls({
    globalScale: { value: 1, min: 0.1, max: 3, step: 0.1 },
    boxColor: '#ff0000',
    rotateAll: true,
    rotationSpeed: { value: 0.01, min: 0, max: 0.1, step: 0.005 },
  })

  const groupRef = useRef()
  useFrame(() => {
    if (rotateAll && groupRef.current) {
      groupRef.current.rotation.y += rotationSpeed
    }
  })

  const objects = [
    {
      id: '1',
      type: 'box',
      position: [-2, 0, 0],
      scale: [1, 1, 1],
      color: boxColor,
      rotation: [0, 0, 0],
    },
    {
      id: '2',
      type: 'sphere',
      position: [2, 0, 0],
      scale: [1.5, 1.5, 1.5],
      color: '#00ff00',
      rotation: [0, 0, 0],
    },
    {
      id: '3',
      type: 'cone',
      position: [0, 2, 0],
      scale: [1, 2, 1],
      color: '#0000ff',
      rotation: [0, 0, 0],
    },
  ]

  return (
    <group ref={groupRef}>
      {objects.map(obj => (
        <mesh
          key={obj.id}
          position={obj.position}
          scale={obj.scale.map(s => s * globalScale)}
          rotation={obj.rotation}
        >
          {obj.type === 'box' && <boxGeometry args={[1, 1, 1]} />}
          {obj.type === 'sphere' && <sphereGeometry args={[1, 32, 32]} />}
          {obj.type === 'cone' && <coneGeometry args={[1, 2, 32]} />}
          <meshStandardMaterial color={obj.color} />
        </mesh>
      ))}
    </group>
  )
}

export default Scene
