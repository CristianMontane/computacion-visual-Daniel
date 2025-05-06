import React, { useEffect, Suspense } from 'react'
import { useLoader } from '@react-three/fiber'
import {
  OrbitControls,
  Environment,
  PresentationControls,
  ContactShadows,
  Html,
} from '@react-three/drei'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import * as THREE from 'three'

/**
 * Componente para visualizar modelos 3D en diferentes formatos
 */
const VisualizadorModelo = ({ format, onModelLoaded }) => {
  // Cargadores para diferentes formatos de modelo
  const modeloOBJ = useLoader(OBJLoader, '/model.obj', cargador => {
    cargador.setRequestHeader({
      'Access-Control-Allow-Origin': '*',
    })
  })

  // Carga de geometría STL
  const geometriaSTL = useLoader(STLLoader, '/model.stl')

  // Carga de modelo GLB/GLTF
  const modeloGLB = useLoader(GLTFLoader, '/model.glb')

  // Creación de la malla para STL con material personalizado
  const mallaSTL = new THREE.Mesh(
    geometriaSTL,
    new THREE.MeshStandardMaterial({
      color: '#67B7D1',
      roughness: 0.5,
      metalness: 0.2,
    })
  )

  // Corregir la orientación del modelo STL (rotación de -90 grados en X para ponerlo vertical)
  mallaSTL.rotation.x = -Math.PI / 2

  // Notificar al componente padre cuando el modelo está cargado
  useEffect(() => {
    switch (format) {
      case 'OBJ':
        onModelLoaded(modeloOBJ)
        break
      case 'STL':
        onModelLoaded(mallaSTL)
        break
      case 'GLB':
        onModelLoaded(modeloGLB.scene)
        break
      default:
      // No hacer nada en caso de formato desconocido
    }
  }, [format, modeloOBJ, mallaSTL, modeloGLB, onModelLoaded])

  // Mensaje de carga para mostrar mientras el modelo se está cargando
  const mensajeCarga = (
    <Html center>
      <div
        style={{
          color: 'white',
          background: 'rgba(0,0,0,0.7)',
          padding: '12px 24px',
          borderRadius: '8px',
          fontFamily: 'Inter, sans-serif',
        }}
      >
        Cargando modelo...
      </div>
    </Html>
  )

  // Función para renderizar el modelo según el formato
  const renderizarModelo = () => {
    switch (format) {
      case 'OBJ':
        return <primitive object={modeloOBJ} />
      case 'STL':
        return <primitive object={mallaSTL} />
      case 'GLB':
        return <primitive object={modeloGLB.scene} />
      default:
        return null
    }
  }

  return (
    <>
      {/* Sistema de iluminación */}
      <ambientLight intensity={0.3} />
      <spotLight
        position={[10, 10, 10]}
        angle={0.15}
        penumbra={1}
        intensity={1}
        castShadow
      />
      <pointLight position={[-10, -10, -10]} intensity={0.5} />

      {/* Controles de interacción y presentación */}
      <PresentationControls
        global
        snap
        rotation={[0, -Math.PI / 4, 0]}
        polar={[-Math.PI / 4, Math.PI / 4]}
        azimuth={[-Math.PI / 4, Math.PI / 4]}
      >
        <Suspense fallback={mensajeCarga}>{renderizarModelo()}</Suspense>
      </PresentationControls>

      {/* Efectos visuales adicionales */}
      <ContactShadows
        position={[0, -1.5, 0]}
        opacity={0.75}
        scale={10}
        blur={2.5}
        far={4}
      />
      <Environment preset='night' />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
        makeDefault
      />
    </>
  )
}

export default VisualizadorModelo
