# 🧪 Taller - Escenas Paramétricas: Creación de Objetos desde Datos

## 📅 Fecha
`2025-05-04` 

---

## 🎯 Objetivo del Taller

Generar objetos 3D de manera programada a partir de listas de coordenadas o datos estructurados. El propósito es entender cómo crear geometría en tiempo real y de forma flexible mediante código, utilizando bucles, estructuras condicionales y exportando o renderizando las escenas generadas.

---

## 🧠 Conceptos Aprendidos


- [ ] Carga de datos de coordenadas 3D desde archivos JSON/CSV (`pandas`).
- [ ] Generación de primitivas geométricas 3D (esferas, cubos, cilindros) en posiciones específicas.
- [ ] Uso de bibliotecas de visualización/manipulación 3D:
- [ ] Exportación de escenas 3D a formatos estándar (.obj, .stl, .glb, .ply).
- [ ] Aplicación de materiales estándar (`meshStandardMaterial`).
- [ ] Implementación de animación básica (rotación) usando el hook `useFrame`.

---

## 🔧 Herramientas y Entornos

- **Python:** `numpy`, `pandas`, `vedo`, `trimesh`, `open3d`
- **JavaScript/Frontend:** `Node.js`, `npm`/`bun`, `Vite`, `React`, `Three.js`, `@react-three/fiber`, `leva`
- **Formatos de Datos/Escena:** JSON, CSV, OBJ, STL, GLB, PLY

---

## 📁 Estructura del Proyecto

```plaintext
2025-05-04_taller_escenas_parametricas/
├── python/                     # Scripts y datos para generación de escenas en Python
│   ├── parametricas.py         # Script principal para generar escenas desde puntos
│   ├── data.json               # Puntos de entrada (x,y,z)
│   └── resultados_modificados/ # Directorio para escenas exportadas por Python
├── threejs/                    # Proyecto de visualización con React y Three.js
│   ├── public/                 # Archivos estáticos
│   ├── src/                    # Código fuente de React/Three.js
│   │   ├── App.jsx             # Componente principal de la aplicación React
│   │   ├── Scene.jsx           # Componente de la escena Three.js
│   │   └── main.jsx            # Punto de entrada de la aplicación
│   ├── package.json            # Dependencias y scripts de Node.js
│   ├── vite.config.js          # Configuración de Vite
│   └── ...                     # Otros archivos de configuración y node_modules
├── resultados/                 # GIFs de demostración
│   ├── python.gif              # Demostración de la salida de vedo (Python)
│   └── threejs.gif             # Demostración de la escena interactiva Three.js
└── README.md                   # Documentación del taller (este archivo)
```  

---

## 🧪 Implementación

### 🔹 Parte Python (`python/parametricas.py`)

1.  **Carga de Puntos:** Lee coordenadas (x, y, z) desde un archivo de entrada (por defecto `data.json`).
2.  **Generación de Escena (Backends):** Itera sobre los puntos cargados. Para cada punto, instancia primitivas geométricas (esferas, cubos, cilindros) usando una o más bibliotecas seleccionadas (`vedo`, `trimesh`, `open3d`). Las formas, tamaños y colores pueden variar según el índice del punto y el backend.
3.  **Visualización (Opcional):** Algunos backends (`vedo`, `open3d`) muestran la escena generada en una ventana interactiva.
4.  **Exportación:** Guarda las escenas generadas por cada backend en varios formatos de archivo 3D (`.obj`, `.stl`, `.glb`, `.ply`) en el directorio `resultados_modificados`.

**Código Relevante (Ejemplo con `vedo`):**
```python
import vedo
import numpy as np
import os

# ... (carga de puntos) ...

def demo_vedo(points, output_prefix):
    objects = []
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33F3', '#33FFF3']
    
    for i, (x, y, z) in enumerate(points):
        shape_type = i % 3
        scaling_factor = 0.08 + abs(np.sin(i * 0.4)) * 0.2
        
        if shape_type == 0:
            obj = vedo.Sphere(pos=(x, y, z), r=scaling_factor, c=colors[i % len(colors)], res=12)
        # ... (otros tipos de forma: Cube, Cylinder) ...
        else:
             obj = vedo.Cylinder(pos=(x, y, z), r=scaling_factor*0.7, height=scaling_factor*2, c=colors[i % len(colors)], res=12)

        objects.append(obj)
    
    scene = vedo.Assembly(objects)
    plt = vedo.Plotter(title='Simple Geometric Distribution')
    plt.show(scene)
    # ... (exportación) ...
```

### 🔹 Parte Three.js (`threejs/src/`)

1.  **Configuración de React:** Utiliza Vite para configurar un proyecto React. `main.jsx` monta el componente principal `App.jsx`.
2.  **Configuración de Canvas:** `App.jsx` configura el `Canvas` de React Three Fiber, estableciendo la cámara inicial y añadiendo iluminación básica (ambiental y direccional).
3.  **Componente de Escena:** `Scene.jsx` define la escena 3D:
    *   Define un array hardcodeado de objetos (caja, esfera, cono) con sus propiedades (posición, escala, color).
    *   Utiliza el hook `useControls` de `leva` para crear controles interactivos (escala global, color de la caja, activación/velocidad de rotación).
    *   Renderiza los objetos como `<mesh>` dentro de un `<group>`.
    *   Aplica las geometrías correspondientes (`boxGeometry`, `sphereGeometry`, `coneGeometry`) y un `meshStandardMaterial`.
    *   Utiliza el hook `useFrame` para animar la rotación del grupo de objetos si el control `rotateAll` está activo.

**Código Relevante (`Scene.jsx`):**
```jsx
import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useControls } from 'leva';

function Scene() {
  const { globalScale, boxColor, rotateAll, rotationSpeed } = useControls({
    // ... controles de leva ...
  });

  const groupRef = useRef();
  useFrame(() => {
    if (rotateAll && groupRef.current) {
      groupRef.current.rotation.y += rotationSpeed;
    }
  });

  // Array hardcodeado de objetos (no usa data.json)
  const objects = [ 
    { id: '1', type: 'box', position: [-2, 0, 0], scale: [1, 1, 1], color: boxColor },
    { id: '2', type: 'sphere', position: [2, 0, 0], scale: [1.5, 1.5, 1.5], color: '#00ff00' },
    { id: '3', type: 'cone', position: [0, 2, 0], scale: [1, 2, 1], color: '#0000ff' },
  ];

  return (
    <group ref={groupRef}>
      {objects.map(obj => (
        <mesh
          key={obj.id}
          position={obj.position}
          scale={obj.scale.map(s => s * globalScale)}
        >
          {obj.type === 'box' && <boxGeometry args={[1, 1, 1]} />}
          {obj.type === 'sphere' && <sphereGeometry args={[1, 32, 32]} />}
          {obj.type === 'cone' && <coneGeometry args={[1, 2, 32]} />}
          <meshStandardMaterial color={obj.color} />
        </mesh>
      ))}
    </group>
  );
}

export default Scene;
```

---

## 📊 Resultados Visuales

A continuación se muestran GIFs que ilustran los resultados de ambas partes del proyecto:

**Python (Visualización con `vedo`):**
![Visualización Python](./resultados/python.gif)

**Three.js (Escena Interactiva):**
![Visualización Three.js](./resultados/threejs.gif)

---

## 🧩 Prompts Usados (Ejemplos)

```text
"Cómo leer puntos x,y,z desde un JSON con pandas en Python?"
"Generar una escena 3D con vedo colocando esferas en coordenadas dadas"
"Exportar una escena de trimesh a formato GLB"
"Crear una escena básica con React Three Fiber y añadir controles con leva"
"Cómo animar la rotación de un objeto en React Three Fiber usando useFrame?"
"Colocar una caja, esfera y cono en Three.js usando React Three Fiber"
```

---

## 💬 Reflexión Final

Este taller permitió explorar dos enfoques diferentes para trabajar con escenas 3D: la generación procedural basada en datos con Python y la visualización interactiva en tiempo real con Three.js/React.

La parte de Python demostró la potencia de bibliotecas como `vedo`, `trimesh` y `open3d` para crear y manipular geometría 3D programáticamente y exportarla a formatos estándar, lo cual es útil para pipelines de procesamiento de datos o generación de assets. El desafío fue entender las diferentes APIs y sistemas de coordenadas de cada biblioteca.

La parte de Three.js con React Three Fiber y `leva` mostró cómo construir rápidamente visualizaciones interactivas en el navegador. La abstracción que ofrece R3F sobre Three.js simplifica la creación de escenas declarativas. La desconexión entre los datos generados en Python y la escena visualizada en Three.js es una limitación del estado actual; un paso futuro interesante sería cargar los puntos o modelos exportados por Python en la aplicación Three.js.
