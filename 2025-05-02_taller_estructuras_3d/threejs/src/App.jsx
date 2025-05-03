import React, { useState, useMemo } from 'react'
import { Canvas, useLoader } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import './App.css'

function Model({ viewMode, onVertexCount }) {
  // Load the OBJ model from the public folder
  const obj = useLoader(OBJLoader, '/models/14-girl-obj/girl%20OBJ.obj')

  // Extract geometries from the loaded object
  const geometries = useMemo(() => {
    const geoms = []
    obj.traverse(child => {
      if (child.isMesh) geoms.push(child.geometry.clone())
    })
    return geoms
  }, [obj])

  // Compute and report total vertices back to parent
  useMemo(() => {
    let total = 0
    geometries.forEach(geometry => {
      total += geometry.attributes.position.count
    })
    onVertexCount(total)
  }, [geometries, onVertexCount])

  return (
    <group>
      {geometries.map((geometry, index) => (
        <React.Fragment key={index}>
          {/* Faces */}
          <mesh geometry={geometry} visible={viewMode === 'faces'}>
            <meshStandardMaterial color='#aaaaaa' flatShading />
          </mesh>
          {/* Edges */}
          <lineSegments geometry={geometry} visible={viewMode === 'edges'}>
            <lineBasicMaterial color='white' />
          </lineSegments>
          {/* Vertices */}
          <points geometry={geometry} visible={viewMode === 'points'}>
            <pointsMaterial size={0.01} color='red' />
          </points>
        </React.Fragment>
      ))}
    </group>
  )
}

export default function App() {
  const [viewMode, setViewMode] = useState('faces')
  const [vertexCount, setVertexCount] = useState(0)

  return (
    <div className='container'>
      <Canvas shadows camera={{ position: [0, 0, 3], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <Model viewMode={viewMode} onVertexCount={setVertexCount} />
        <OrbitControls />
      </Canvas>

      <div className='controls'>
        <button
          onClick={() => setViewMode('faces')}
          className={viewMode === 'faces' ? 'active' : ''}
        >
          Caras
        </button>
        <button
          onClick={() => setViewMode('edges')}
          className={viewMode === 'edges' ? 'active' : ''}
        >
          Aristas
        </button>
        <button
          onClick={() => setViewMode('points')}
          className={viewMode === 'points' ? 'active' : ''}
        >
          Vértices
        </button>
        <div className='info'>Vértices: {vertexCount}</div>
      </div>
    </div>
  )
}
