import { useState, useRef, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Center, PerspectiveCamera } from '@react-three/drei'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { Edges, Points, Wireframe } from '@react-three/drei'
import * as THREE from 'three'
import './App.css'

function ModelViewer({
  url,
  displayMode = 'all',
  color = 'white',
  setModelInfo,
  scale = 0.01,
}) {
  const objRef = useRef()
  const [model, setModel] = useState(null)

  useEffect(() => {
    const loader = new OBJLoader()
    loader.load(url, obj => {
      // Center and normalize the model
      const box = new THREE.Box3().setFromObject(obj)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())

      // Center the model at origin
      obj.position.sub(center)

      setModel(obj)

      // Calculate model stats
      let vertexCount = 0
      let faceCount = 0

      obj.traverse(child => {
        if (child.isMesh) {
          const geometry = child.geometry
          vertexCount += geometry.attributes.position.count
          if (geometry.index) {
            faceCount += geometry.index.count / 3
          } else {
            faceCount += geometry.attributes.position.count / 3
          }
        }
      })

      setModelInfo({
        vertices: vertexCount,
        faces: faceCount,
        edges: Math.round((faceCount * 3) / 2),
        dimensions: {
          width: size.x.toFixed(2),
          height: size.y.toFixed(2),
          depth: size.z.toFixed(2),
        },
      })
    })
  }, [url, setModelInfo])

  if (!model) return null

  return (
    <group ref={objRef} scale={[scale, scale, scale]}>
      {model &&
        model.children.map((mesh, i) => {
          // Clone the mesh to avoid mutating the original
          const clonedMesh = mesh.clone()

          return (
            <mesh
              key={i}
              geometry={clonedMesh.geometry}
              position={clonedMesh.position}
            >
              <meshStandardMaterial
                color={color}
                roughness={0.5}
                metalness={0.2}
                transparent={displayMode !== 'all'}
                opacity={displayMode === 'all' ? 1 : 0.1}
              />

              {(displayMode === 'edges' || displayMode === 'all') && (
                <Edges
                  threshold={15}
                  color='#000000'
                  scale={1}
                  visible={true}
                />
              )}

              {displayMode === 'wireframe' && (
                <Wireframe thickness={1} color='#ff0000' />
              )}

              {displayMode === 'vertices' && (
                <Points size={3} color='#0000ff' threshold={0.1} />
              )}
            </mesh>
          )
        })}
    </group>
  )
}

function App() {
  const [displayMode, setDisplayMode] = useState('all')
  const [modelInfo, setModelInfo] = useState({
    vertices: 0,
    faces: 0,
    edges: 0,
    dimensions: { width: 0, height: 0, depth: 0 },
  })
  const [scale, setScale] = useState(0.01)

  const handleScaleChange = event => {
    setScale(parseFloat(event.target.value))
  }

  return (
    <div className='app-container'>
      <div className='controls-panel'>
        <h1>3D Model Viewer</h1>

        <div className='view-controls'>
          <h3>Display Mode</h3>
          <div className='buttons-container'>
            <button
              className={displayMode === 'all' ? 'active' : ''}
              onClick={() => setDisplayMode('all')}
            >
              Full Model
            </button>
            <button
              className={displayMode === 'vertices' ? 'active' : ''}
              onClick={() => setDisplayMode('vertices')}
            >
              Vertices
            </button>
            <button
              className={displayMode === 'edges' ? 'active' : ''}
              onClick={() => setDisplayMode('edges')}
            >
              Edges
            </button>
            <button
              className={displayMode === 'wireframe' ? 'active' : ''}
              onClick={() => setDisplayMode('wireframe')}
            >
              Wireframe
            </button>
          </div>
        </div>

        <div className='scale-control'>
          <h3>Model Scale</h3>
          <input
            type='range'
            min='0.001'
            max='0.1'
            step='0.001'
            value={scale}
            onChange={handleScaleChange}
          />
          <span>{scale.toFixed(3)}</span>
        </div>

        <div className='model-info'>
          <h3>Model Information</h3>
          <p>Vertices: {modelInfo.vertices}</p>
          <p>Faces: {modelInfo.faces}</p>
          <p>Edges: {modelInfo.edges}</p>
          {modelInfo.dimensions && (
            <>
              <p>Width: {modelInfo.dimensions.width}</p>
              <p>Height: {modelInfo.dimensions.height}</p>
              <p>Depth: {modelInfo.dimensions.depth}</p>
            </>
          )}
        </div>
      </div>

      <div className='canvas-container'>
        <Canvas shadows>
          <ambientLight intensity={0.4} />
          <spotLight
            position={[100, 100, 100]}
            angle={0.15}
            penumbra={1}
            intensity={1}
            castShadow
          />
          {/* Increase camera distance to ensure it's outside the model */}
          <PerspectiveCamera makeDefault position={[0, 0, 50]} fov={40} />
          <Center>
            <ModelViewer
              url='/models/qilin.obj'
              displayMode={displayMode}
              setModelInfo={setModelInfo}
              scale={scale}
            />
          </Center>
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            minDistance={2}
            maxDistance={200}
          />
        </Canvas>
      </div>
    </div>
  )
}

export default App
