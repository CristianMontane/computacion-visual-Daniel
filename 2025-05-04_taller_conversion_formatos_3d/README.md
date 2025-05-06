# 🧪 Taller - Importando el Mundo: Visualización y Conversión de Formatos 3D

## 📅 Fecha
`2025-05-04`

---

## 🔍 Objetivo del taller

Comparar y convertir entre distintos formatos de modelos 3D: .OBJ, .STL y .GLTF, y visualizar sus diferencias en geometría y materiales. El objetivo es entender la estructura interna de los archivos 3D, su compatibilidad entre entornos, y cómo se interpretan en distintas plataformas de visualización.

---

## 🧠 Conceptos Aprendidos

Lista de conceptos clave aplicados en el taller:

- [ ] Diferencias estructurales entre formatos 3D (.OBJ, .STL, .GLTF)
- [ ] Técnicas de conversión entre formatos usando bibliotecas Python
- [ ] Visualización de modelos 3D en Python con trimesh/open3d
- [ ] Comparación de rendimiento y fidelidad entre formatos
- [ ] Manejo de materiales y texturas en diferentes formatos

---

## 🔧 Herramientas y Entornos

- Python (`trimesh`, `open3d`, `numpy`)
- JavaScript / React (`react`, `@react-three/fiber`, `@react-three/drei`)
- Three.js para renderizado 3D
- Formatos analizados: .OBJ, .STL, .GLTF

---

## 📁 Estructura del Proyecto

```
2025-05-04_taller_conversion_formatos_3d/
├── python/              # Implementación en Python (notebook)
│   ├── conversiones.ipynb    # Código para conversión y análisis
│   └── ...
├── threejs/             # Implementación en React Three Fiber
│   ├── src/             # Código fuente
│   │   ├── App.jsx      # Componente principal con visualizador
│   │   ├── ModelViewer.jsx  # Componente de visualización
│   │   └── ...
│   └── ...
├── Capturas/            # Capturas y resultados visuales
│   ├── python/          # Resultados del análisis en Python
│   └── threejs/         # Capturas de la visualización web
├── README.md            # Este archivo
```

---

## 🧪 Implementación

### 🔹 Python con trimesh/open3d

Se implementó un notebook para cargar, analizar y convertir modelos 3D entre los formatos .OBJ, .STL y .GLTF. El flujo de trabajo incluyó:

1. **Carga de modelos**: Utilizando trimesh para cargar modelos en diferentes formatos.
2. **Análisis de propiedades**: Extracción de métricas como número de vértices, caras, presencia de duplicados y propiedades de "watertight" (estanqueidad).
3. **Visualización**: Renderizado de los modelos para comparación visual.
4. **Conversión**: Transformación entre formatos preservando la geometría y, cuando es posible, los materiales.

#### Resultados del análisis:

```
+----------------------+--------------+--------------+-----------------+------------+
| Modelo               | Vértices     | Caras        | Duplicados      | Watertight |
+----------------------+--------------+--------------+-----------------+------------+
| base.obj             | 36443        | 50000        | 11415           | No         |
| base.stl             | 25028        | 50000        | 0               | Sí         |
| base_basic_shaded.glb | 36546        | 50000        | 11518           | No         |
+----------------------+--------------+--------------+-----------------+------------+
```

#### Código relevante para la conversión:

```python
# Cargar modelo OBJ
mesh_obj = trimesh.load('models/base.obj')

# Convertir a STL
mesh_obj.export('converted/base.stl')

# Convertir a GLTF
mesh_obj.export('converted/base.glb')

# Análisis de propiedades
print(f"Vértices: {len(mesh_obj.vertices)}")
print(f"Caras: {len(mesh_obj.faces)}")
print(f"Duplicados: {len(mesh_obj.vertices) - len(np.unique(mesh_obj.vertices, axis=0))}")
print(f"Watertight: {mesh_obj.is_watertight}")
```

### 🔹 Three.js con React Three Fiber

Se desarrolló una aplicación web interactiva que permite:

1. **Cargar modelos**: Visualización de los tres formatos (.OBJ, .STL, .GLTF) convertidos.
2. **Comparar visualmente**: Interfaz para alternar entre formatos y observar diferencias.
3. **Explorar**: Implementación de OrbitControls para navegar alrededor de los modelos.
4. **Analizar**: Mostrar información sobre el modelo seleccionado (formato, vértices, caras).

#### Código relevante:

```jsx
// Componente para cargar y mostrar modelos 3D
function ModelViewer({ format }) {
  const [modelInfo, setModelInfo] = useState(null);
  
  // Seleccionar el modelo según el formato
  const modelPath = useMemo(() => {
    switch(format) {
      case 'obj': return '/models/converted_base.obj';
      case 'stl': return '/models/converted_base.stl';
      case 'gltf': return '/models/converted_base.glb';
      default: return '/models/converted_base.glb';
    }
  }, [format]);
  
  // Cargar el modelo y extraer información
  useEffect(() => {
    // Código para cargar y analizar el modelo...
  }, [modelPath]);

  return (
    <>
      <Canvas camera={{ position: [0, 5, 10] }}>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <Suspense fallback={<Loader />}>
          {format === 'obj' && <OBJLoader url={modelPath} />}
          {format === 'stl' && <STLLoader url={modelPath} />}
          {format === 'gltf' && <GLTFLoader url={modelPath} />}
        </Suspense>
        <OrbitControls />
        <axesHelper args={[5]} />
      </Canvas>
      
      {modelInfo && (
        <div className="info-panel">
          <h3>Modelo: {format.toUpperCase()}</h3>
          <p>Vértices: {modelInfo.vertices}</p>
          <p>Caras: {modelInfo.faces}</p>
        </div>
      )}
    </>
  );
}
```

---

## 📊 Resultados Visuales

### 🔹 Python: Análisis y Visualización

![Resultados Python](Capturas/python/Resultados.gif)

### 🔹 Three.js: Visualización Interactiva

![Visualización Three.js](Capturas/threejs/Evidencia.gif)



---

## 🧩 Prompts Usados

```text
"Cómo convertir modelos 3D entre formatos OBJ, STL y GLTF usando Python"
"Diferencias estructurales entre formatos 3D: OBJ vs STL vs GLTF"
"Visualización de modelos 3D con trimesh y open3d en Python"
"Cómo cargar diferentes formatos 3D en React Three Fiber"
"Extracción de métricas de geometría 3D como vértices y caras"
"Implementación de un visualizador 3D con React Three Fiber"
```

---

## 💬 Reflexión Final

Este taller proporcionó una valiosa comprensión de las diferencias entre formatos 3D comunes y sus implicaciones prácticas. Cada formato tiene sus propias ventajas y desventajas:

- **OBJ**: Excelente para preservar materiales y texturas, pero genera muchos vértices duplicados.
- **STL**: Formato robusto y "watertight" ideal para impresión 3D, pero no soporta materiales ni texturas.
- **GLTF**: Formato moderno con buen soporte para materiales, animaciones y optimizado para web.

Las principales dificultades encontradas fueron:
- Mantener la fidelidad de materiales y texturas durante las conversiones
- Manejar modelos con geometrías complejas o no manifold
- Optimizar el rendimiento de carga en Three.js para modelos grandes

La experiencia de visualizar el mismo modelo en diferentes formatos y entornos (Python vs Web) fue particularmente reveladora, mostrando cómo cada plataforma interpreta y renderiza la geometría y los materiales de manera diferente.

Como mejoras futuras, sería interesante implementar:
- Análisis más detallado de materiales y texturas
- Optimización automática de modelos (decimation, simplificación)
- Soporte para formatos adicionales como FBX o USD
- Visualización side-by-side para comparaciones más directas
