# 🧪 Taller - Jerarquías y Transformaciones: El Árbol del Movimiento

## 📅 Fecha
`2025-05-03`

---

## 🔍 Objetivo del taller

Aplicar estructuras jerárquicas y árboles de transformación para organizar escenas y simular movimiento relativo entre objetos. Se busca comprender cómo las transformaciones afectan a los nodos hijos en una estructura padre-hijo y cómo visualizar estos efectos en tiempo real.

---

## 🧠 Conceptos Aprendidos

Lista de conceptos clave aplicados en el taller:

- [ ] Implementación de estructuras jerárquicas con React Three Fiber
- [ ] Uso de componentes `<group>` para crear relaciones padre-hijo
- [ ] Aplicación de transformaciones (rotación, traslación) en escenas 3D
- [ ] Visualización del efecto cascada de transformaciones en objetos anidados
- [ ] Implementación de controles interactivos en tiempo real con Leva
- [ ] Sistemas de coordenadas locales vs. globales en escenas 3D

---

## 🔧 Herramientas y Entornos

- JavaScript / React (`react`, `@react-three/fiber`, `@react-three/drei`)
- Three.js para renderizado 3D
- Leva para controles UI interactivos
- Vite como entorno de desarrollo

---

## 📁 Estructura del Proyecto

```
2025-05-03-taller_jerarquias_transformaciones/
├── threejs/              # Implementación en React Three Fiber
│   ├── src/              # Código fuente
│   │   ├── App.jsx       # Componente principal con la jerarquía de objetos
│   │   ├── App.css       # Estilos para la aplicación
│   │   └── ...
│   └── ...
├── README.md             # Este archivo
```

---

## 🧪 Implementación

### 🔹 Three.js con React Three Fiber

La implementación consiste en una escena 3D con una estructura jerárquica de tres niveles:

1. **Objeto Padre (Cubo Rojo)**: Objeto raíz que puede ser transformado con controles de rotación y traslación.
2. **Objeto Hijo (Esfera Verde)**: Primer nivel de anidamiento que hereda las transformaciones del padre.
3. **Objeto Nieto (Cilindro Azul)**: Segundo nivel de anidamiento que hereda transformaciones tanto del padre como del hijo.

Se implementaron controles interactivos utilizando Leva para permitir:
- Controlar la posición (X, Y, Z) del objeto padre
- Ajustar la rotación (X, Y, Z) del objeto padre
- Modificar la rotación (Y) y distancia del objeto hijo
- Configurar la rotación (Z) y distancia del objeto nieto

La aplicación demuestra claramente cómo las transformaciones aplicadas a un objeto padre afectan a todos sus descendientes en la jerarquía, mientras que las transformaciones aplicadas a un hijo solo afectan a ese objeto y sus propios descendientes.

### 🔹 Código relevante

#### Estructura Jerárquica (`App.jsx`)

```jsx
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
```

#### Controles Interactivos con Leva (`App.jsx`)

```jsx
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
```

---

## 📊 Resultados Visuales

### 🌐 Three.js con React Three Fiber

Se implementó una aplicación web interactiva que permite manipular la posición y rotación de objetos en una jerarquía de tres niveles.

![Animación Three.js](Capturas/threejs/hierarchy-demo.gif)



---

## 🧩 Prompts Usados (Ejemplos)

```text
"Cómo implementar una estructura jerárquica con grupos en React Three Fiber"
"Implementación de controles de transformación en tiempo real con Leva"
"Cómo afectan las transformaciones en estructuras padre-hijo en Three.js"
"Configuración de una escena básica con React Three Fiber y Vite"
```

---

## 💬 Reflexión Final

Este taller proporcionó una valiosa experiencia práctica en la implementación de estructuras jerárquicas en entornos 3D. Comprender el comportamiento en cascada de las transformaciones es fundamental para cualquier desarrollo de gráficos 3D, ya que constituye la base de la animación y la interactividad en entornos virtuales.

Las principales dificultades encontradas fueron:
- Comprender la diferencia entre espacios de coordenadas locales y globales
- Visualizar mentalmente cómo las transformaciones se acumulan en una cadena de objetos
- Configurar correctamente los límites para los controles interactivos para mantener los objetos visibles

El uso de React Three Fiber facilitó significativamente la implementación, gracias a su enfoque declarativo para construir escenas 3D. La biblioteca Leva también resultó ser una excelente herramienta para añadir controles interactivos de forma rápida y estéticamente agradable.

Como mejoras futuras, sería interesante implementar:
- Visualización de matrices de transformación en tiempo real
- Trazado de líneas para visualizar las jerarquías
- Modo de visualización "wireframe" para mejor comprensión espacial
- Implementación de diferentes formas de interpolación para las transformaciones
