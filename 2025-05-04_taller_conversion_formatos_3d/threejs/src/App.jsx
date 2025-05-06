import React, { useState, useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import VisualizadorModelo from './components/ModelViewer'
import './App.css'

// Componente principal de la aplicación
const Aplicacion = () => {
  // Estados para controlar la aplicación
  const [tipoFormato, setTipoFormato] = useState('OBJ')
  const [contadorVertices, setContadorVertices] = useState(0)
  const [estaCargando, setEstaCargando] = useState(true)
  const referenciaCanvas = useRef(null)

  // Función para manejar cuando el modelo termina de cargar
  const manejarModeloCargado = modeloCargado => {
    setEstaCargando(false)

    // Contador de vértices
    let totalVertices = 0
    modeloCargado.traverse?.(elemento => {
      if (elemento.isMesh) {
        totalVertices += elemento.geometry.attributes?.position?.count || 0
      }
    })

    setContadorVertices(totalVertices)
  }

  return (
    <div className='app-container'>
      {/* Barra superior de control */}
      <div className='top-ui-container'>
        <div className='ui-panel'>
          <h1 className='app-title'>Visualizador 3D</h1>

          <div className='control-group'>
            <label htmlFor='formato'>Formato:</label>
            <select
              id='formato'
              value={tipoFormato}
              onChange={evento => {
                setTipoFormato(evento.target.value)
                setEstaCargando(true)
              }}
              className='select-format'
            >
              <option value='OBJ'>OBJ</option>
              <option value='STL'>STL</option>
              <option value='GLB'>GLB</option>
            </select>
          </div>

          <div className='stats-group'>
            <div className='stat-item'>
              <span>Tipo:</span>
              <span>{tipoFormato}</span>
            </div>
            <div className='stat-item'>
              <span>Vértices:</span>
              <span>
                {estaCargando ? '...' : contadorVertices.toLocaleString()}
              </span>
            </div>
            <div className='stat-item'>
              <span>Estado:</span>
              <span>{estaCargando ? 'Cargando' : 'Completado'}</span>
            </div>
          </div>

          <div className='controls-hint'>
            Controles: arrastrar para rotar, rueda para zoom
          </div>
        </div>
      </div>

      {/* Área de renderizado 3D */}
      <Canvas ref={referenciaCanvas}>
        {estaCargando && (
          <mesh position={[0, 0, -5]}>
            <sphereGeometry args={[0.5, 16, 16]} />
            <meshStandardMaterial color='#3498db' wireframe />
          </mesh>
        )}
        <VisualizadorModelo
          format={tipoFormato}
          onModelLoaded={manejarModeloCargado}
        />
      </Canvas>
    </div>
  )
}

export default Aplicacion
