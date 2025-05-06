import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Aplicacion from './App.jsx'

// Inicialización de la aplicación y renderizado en el DOM
const elementoRaiz = document.getElementById('root')
const renderizador = createRoot(elementoRaiz)

// Renderizado con StrictMode para detectar problemas potenciales
renderizador.render(
  <StrictMode>
    <Aplicacion />
  </StrictMode>
)
