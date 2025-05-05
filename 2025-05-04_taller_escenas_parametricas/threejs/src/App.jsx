import './App.css'
import { Canvas } from '@react-three/fiber'
import Scene from './Scene'

function App() {
  return (
    <div className='App'>
      <div className='toolbar'>
        <h1>Parametric Scene</h1>
      </div>
      <Canvas className='canvas' camera={{ position: [5, 5, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <Scene />
      </Canvas>
    </div>
  )
}

export default App
