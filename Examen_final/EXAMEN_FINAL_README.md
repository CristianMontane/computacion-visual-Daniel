# 🎓 Examen Final – Computación Visual
## 🔐 Sistema de Reconocimiento Facial para Control de Acceso



## 👤 Datos del Estudiante

- **Nombre completo:** Cristian Daniel Montañez Pineda 
- **Número de documento:** 1001185275
- **Correo institucional:** cmontanez@unal.edu.co

---

## 📌 Definición del Problema

### 🎯 Problema Identificado
El **control de acceso tradicional** en edificios, oficinas y espacios seguros depende de sistemas físicos como tarjetas, códigos PIN o llaves, que presentan múltiples vulnerabilidades:

- **Pérdida o robo** de credenciales físicas
- **Compartición no autorizada** de códigos de acceso
- **Costos elevados** de reposición y mantenimiento
- **Falta de trazabilidad** detallada de accesos
- **Vulnerabilidad a suplantación** de identidad

### 🚀 Relevancia desde Computación Visual
Este problema es **altamente relevante** para computación visual porque:

- Requiere **procesamiento de imágenes en tiempo real** para detección facial
- Aplica **algoritmos de reconocimiento de patrones** para identificación biométrica
- Integra **visión por computadora** con sistemas de seguridad práticos
- Demuestra **aplicación directa de IA** en soluciones empresariales
- Combina **múltiples técnicas de computación visual** en un sistema cohesivo

---

## 🧠 Selección de Talleres Integrados

### **1. 🤖 Taller Gestos con MediaPipe**
**Integración:** Sistema de detección facial y extracción de landmarks
- **Técnicas aplicadas:**
  - MediaPipe Face Detection para localización de rostros
  - Extracción de 468 puntos de referencia faciales (face mesh)
  - Análisis geométrico de características faciales
  - Validación de centrado y calidad del rostro

**Código implementado:**
```python
# En face_utils.py
def face_mesh(self, face_image: np.ndarray) -> Tuple[bool, Any]:
    check_face_mesh, face_mesh_info = self.mesh_detector.face_mesh_mediapipe(face_image)
    return check_face_mesh, face_mesh_info
```

### **2. 🔍 Taller YOLO + SAM + MiDaS (Pipeline de Procesamiento)**
**Integración:** Pipeline secuencial de procesamiento de imágenes
- **Técnicas aplicadas:**
  - Detección de objetos (rostros) → Segmentación → Análisis de características
  - Procesamiento en pipeline: `Detección → Validación → Extracción → Comparación`
  - Manejo de múltiples modelos de IA integrados
  - Optimización de rendimiento para tiempo real

**Pipeline implementado:**
```python
# En face_signup.py
def process(self, face_image: np.ndarray, user_code: str):
    # 1. Detección (equivalente a YOLO)
    check_face_detect, face_info, face_save = self.face_utilities.check_face(face_image)
    # 2. Análisis de malla (equivalente a SAM)
    check_face_mesh, face_mesh_info = self.face_utilities.face_mesh(face_image)
    # 3. Procesamiento de características (equivalente a MiDaS)
    face_mesh_points_list = self.face_utilities.extract_face_mesh(face_image, face_mesh_info)
```

### **3. 🎨 Taller Interfaces Multimodales (Voz + Gestos)**
**Integración:** Sistema de interacción multimodal completo
- **Técnicas aplicadas:**
  - Fusión de modalidades: Interfaz gráfica + Cámara + Base de datos
  - Arquitectura de 4 clases principales (GUI, SignUp, Login, Database)
  - Threading concurrente para procesamiento paralelo
  - Feedback multimodal: Visual, textual y de estado

**Arquitectura implementada:**
```python
# En simple_modern.py
class SimpleModernGUI:
    def __init__(self, root):
        # Módulos del sistema (arquitectura multimodal)
        self.face_sign_up = FaceSignUp()
        self.face_login = FaceLogIn()
        self.database = DataBasePaths()
```

### **4. 🧠 Taller BCI Simulado (Procesamiento en Tiempo Real)**
**Integración:** Procesamiento de señales visuales en tiempo real
- **Técnicas aplicadas:**
  - Latencia < 100ms para procesamiento facial
  - Clasificación de estados (identidad reconocida/no reconocida)
  - Threading para separación de adquisición, procesamiento y UI
  - Sistema de retroalimentación inmediata

**Sistema de tiempo real:**
```python
# En face_login.py
def process(self, face_image: np.ndarray):
    # Procesamiento de señal visual (imagen facial)
    check_face_detect, face_info, face_save = self.face_utilities.check_face(face_image)
    # Clasificación de identidad
    self.matcher = self.face_utilities.match_faces(face_crop, faces_database)
    # Respuesta inmediata
    return face_image, self.matcher, message
```

### **5. 🎤 Taller Reconocimiento de Voz Local**
**Integración:** Sistema de interacción y control del sistema
- **Técnicas aplicadas:**
  - Menú interactivo con verificaciones automáticas
  - Sistema de feedback auditivo y textual
  - Arquitectura modular con separación de responsabilidades
  - Manejo de errores robusto y recuperación automática

**Sistema implementado:**
```python
# En start.py
def main():
    """Sistema de control con verificaciones automáticas"""
    while True:
        show_menu()
        choice = input("Selecciona una opción (1-3): ").strip()
        
        if choice == '1':
            if check_dependencies() and check_project_structure():
                setup_directories()
                run_modern_interface()
```

---

## 🏗️ Arquitectura de Solución

### 📊 Diagrama de Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLUJO DE TRABAJO                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

Registro de Usuario:
Cámara → Detección Facial → Validación Mesh → Centrado → Recorte → Guardar

Verificación de Acceso:
Cámara → Detección Facial → Extracción Features → Comparación DB → Decisión

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          SISTEMA DE RECONOCIMIENTO FACIAL                       │
│                                 Access Control                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────┐
│     CÁMARA      │─── │    PROCESAMIENTO │─── │    ANÁLISIS     │─── │   CONTROL    │
│                 │    │     DE IMAGEN    │    │     FACIAL      │    │   DE ACCESO  │
│ • Captura video │    │                  │    │                 │    │              │
│ • OpenCV        │    │ • MediaPipe      │    │ • Face Detection│    │ • Validación │
│ • Tiempo real   │    │ • Face Mesh      │    │ • Landmarks     │    │ • Logging    │
│ • 640x480 px    │    │ • Preprocesado   │    │ • Comparación   │    │ • Database   │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────┘
          │                     │                        │                     │
          ▼                     ▼                        ▼                     ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│     INTERFAZ    │    │     BASE DE      │    │    UTILIDADES   │    │     SISTEMA      │
│     GRÁFICA     │    │     DATOS        │    │                 │    │  DE INICIO       │
│                 │    │                  │    │                 │    │                  │
│ • Tkinter GUI   │    │ • Imágenes PNG   │    │ • VideoProcessor│    │ • start.py       │
│ • Navegación    │    │ • Archivos TXT   │    │ • WindowManager │    │ • Verificador    │
│ • Dashboard     │    │ • Historial      │    │ • MessageHandler│    │ • Dependencias   │
│ • Control       │    │ • Usuarios       │    │ • FileUtils     │    │ • Configuración  │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘



┌─────────────────────────────────────────────────────────────────────────────────┐
│                          COMPONENTES Y TECNOLOGÍAS                              │
└─────────────────────────────────────────────────────────────────────────────────┘

🤖 IA y Procesamiento:           🎨 Interfaz y UX:              🛠️ Herramientas:
• MediaPipe (Face Detection)     • Tkinter (GUI moderna)       • OpenCV (Video)
• Face Recognition Models        • Dashboard estadísticas      • NumPy (Cálculos)
• DeepFace (Comparación)         • Navegación por pestañas     • Pillow (Imágenes)
• TensorFlow (Backend)           • Feedback visual/textual     • Threading (Concurrencia)

💾 Base de Datos:               ⚡ Rendimiento:                🔧 Desarrollo:
• Archivos PNG (Rostros)        • Tiempo real (<100ms)        • Python 3.8+
• Archivos TXT (Usuarios)       • Threading optimizado        • Arquitectura modular
• Historial de accesos          • Carga lazy de modelos       • Manejo de errores
• Configuración persistente     • Cache de resultados         • Testing automatizado
```

### 🔧 Relación entre Módulos

**1. Módulo de Captura (VideoProcessor)**
- Interfaz con cámara web
- Preprocesamiento de frames
- Optimización de resolución

**2. Módulo de Procesamiento Facial (FaceUtils)**
- Integración con MediaPipe
- Extracción de características
- Validación de calidad

**3. Módulo de Base de Datos (DataBasePaths)**
- Gestión de archivos
- Persistencia de datos
- Historial de accesos

**4. Módulo de Interfaz (SimpleModernGUI)**
- Control de usuario
- Visualización de resultados
- Gestión de estados

**5. Sistema de Inicio (start.py)**
- Verificación de dependencias
- Configuración automática
- Menú de control

---

## 🎬 Video de Demostración

**Enlace al video:** https://drive.google.com/file/d/1IMb7EdsJozmVwaEZAI6cqllOvCc8OvMP/view?usp=sharing

El video demuestra:
- ✅ Funcionamiento completo del sistema de reconocimiento facial
- ✅ Proceso de registro de nuevos usuarios
- ✅ Verificación exitosa de identidad
- ✅ Interfaz gráfica moderna y navegación
- ✅ Integración de los 5 talleres seleccionados

---

## 📊 Evidencia de Funcionamiento

### 📌 GIF 1: Proceso de Registro de Usuario
![Registro de usuario](./evidencias/registro_usuario.gif)

**Demuestra:**
- Detección facial en tiempo real con MediaPipe
- Análisis de mesh facial para validación
- Interface de registro con feedback visual
- Guardado automático en base de datos

### 📌 GIF 2: Verificación de Acceso Exitosa
![Verificación exitosa](./evidencias/verificacion_exitosa.gif)

**Demuestra:**
- Reconocimiento facial instantáneo
- Comparación con base de datos
- Mensaje de acceso concedido
- Logging automático con timestamp

### 📌 GIF 3: Interface Principal y Dashboard
![Dashboard principal](./evidencias/dashboard_principal.gif)

**Demuestra:**
- Navegación por pestañas del sistema
- Dashboard con estadísticas en tiempo real
- Gestión de usuarios registrados
- Configuración del sistema

### 📌 GIF 4: Sistema de Inicio y Verificaciones
![Sistema de inicio](./evidencias/sistema_inicio.gif)

**Demuestra:**
- Script de inicio inteligente (start.py)
- Verificación automática de dependencias
- Configuración del entorno
- Menú interactivo de opciones

---

## 🔧 Explicación Técnica del Funcionamiento

### **1. Arquitectura Multimodal Integrada**

El sistema implementa una **arquitectura multimodal** basada en el taller de interfaces que combina:

```python
# Integración de modalidades
Modalidad Visual: Cámara + OpenCV + MediaPipe
Modalidad Datos: Base de datos local + Historial
Modalidad Interface: Tkinter GUI + Dashboard
Modalidad Control: Threading + Menú interactivo
```

### **2. Pipeline de Procesamiento Inspirado en YOLO+SAM+MiDaS**

```python
# Pipeline secuencial optimizado
def procesar_rostro(imagen):
    # Fase 1: Detección (inspirado en YOLO)
    rostro_detectado = detectar_rostro_mediapipe(imagen)
    
    # Fase 2: Análisis detallado (inspirado en SAM)
    mesh_facial = extraer_mesh_468_puntos(rostro_detectado)
    
    # Fase 3: Extracción de características (inspirado en MiDaS)
    caracteristicas = extraer_features_para_matching(mesh_facial)
    
    return caracteristicas
```

### **3. Procesamiento en Tiempo Real (Inspirado en BCI)**

```python
# Arquitectura de tiempo real con threading
class SistemaReconocimiento:
    def __init__(self):
        self.hilo_camara = threading.Thread(target=self.capturar_video)
        self.hilo_procesamiento = threading.Thread(target=self.procesar_frames)
        self.hilo_interface = threading.Thread(target=self.actualizar_gui)
        
    def procesar_en_tiempo_real(self):
        latencia_objetivo = 100  # ms (como en el taller BCI)
        while self.activo:
            frame = self.capturar_frame()
            resultado = self.reconocer_rostro(frame)  # <100ms
            self.actualizar_interface(resultado)
```

### **4. Sistema de Landmarks Faciales (MediaPipe)**

```python
# Detección y análisis de landmarks como en taller de gestos
def analizar_rostro_mediapipe(imagen):
    # Extracción de 468 puntos de referencia
    landmarks = mediapipe_face_mesh.process(imagen)
    
    # Validación de centrado (similar a clasificación de gestos)
    centrado = validar_posicion_rostro(landmarks)
    
    # Extracción de región de interés
    bbox = extraer_bounding_box(landmarks)
    rostro_recortado = recortar_rostro(imagen, bbox)
    
    return rostro_recortado, centrado
```

### **5. Sistema de Control Interactivo (Inspirado en Reconocimiento de Voz)**

```python
# Menú interactivo con verificaciones automáticas
def sistema_control_inteligente():
    # Verificación de dependencias (como en taller de voz)
    verificar_dependencias_automaticamente()
    
    # Configuración del entorno
    configurar_directorios_automaticamente()
    
    # Menú de opciones
    while True:
        mostrar_menu_opciones()
        opcion = input("Selecciona opción: ")
        procesar_comando(opcion)
```

### **6. Base de Datos y Persistencia**

El sistema utiliza una base de datos local optimizada:

```python
# Estructura de datos persistente
├── process/database/faces/          # Imágenes PNG de rostros
│   └── {codigo_usuario}.png        # Una imagen por usuario
├── process/database/users/          # Datos de usuarios
│   └── {codigo_usuario}.txt        # Historial de accesos
└── __pycache__/                    # Cache de modelos compilados
```

### **7. Optimizaciones de Rendimiento**

- **Carga lazy de modelos**: Los modelos de IA se cargan solo cuando se necesitan
- **Cache de resultados**: Resultados de comparación se almacenan temporalmente
- **Threading optimizado**: Separación de hilos para evitar bloqueos
- **Resolución adaptativa**: Ajuste automático según capacidad del hardware


---

## 🎯 Conclusiones y Reflexiones Personales

### **💡 Aprendizajes Técnicos Clave**

**1. Integración Multimodal Compleja**
La experiencia de integrar 5 talleres diferentes me enseñó que la **arquitectura modular** es fundamental para sistemas complejos. Cada taller aportó una perspectiva única:
- MediaPipe me enseñó precisión en detección de landmarks
- El pipeline YOLO+SAM+MiDaS mostró cómo encadenar modelos de IA
- Las interfaces multimodales demostraron la importancia del threading
- El BCI reforzó la necesidad de optimización para tiempo real
- El reconocimiento de voz aportó técnicas de control robusto

**2. Desafíos de Rendimiento en Tiempo Real**
Implementar un sistema que funcione en <100ms requirió optimizaciones cuidadosas:
- Separación de hilos para evitar bloqueos de UI
- Carga lazy de modelos pesados para reducir tiempo de inicio
- Cache inteligente de resultados para evitar recomputación
- Ajuste dinámico de resolución según capacidad del hardware

**3. Importancia de la Experiencia de Usuario**
El sistema debe ser técnicamente sólido pero también **usable**. La integración del menú interactivo (inspirado en reconocimiento de voz) y la interfaz gráfica moderna (inspirada en interfaces multimodales) fueron cruciales para crear una experiencia completa.

### **🚀 Aplicaciones Futuras**

**1. Escalabilidad Empresarial**
- Integración con sistemas de gestión empresarial (ERP)
- Soporte para múltiples puntos de acceso simultáneos
- Base de datos distribuida para organizaciones grandes
- APIs REST para integración con otros sistemas

**2. Mejoras de Seguridad**
- Detección de ataques de spoofing con análisis de profundidad
- Autenticación de doble factor (facial + PIN)
- Encriptación de datos biométricos almacenados
- Auditoría avanzada con análisis de patrones de acceso

**3. Tecnologías Emergentes**
- Integración con hardware especializado (cámaras IR, sensores de profundidad)
- Optimización para edge computing con TensorRT
- Soporte para reconocimiento con mascarillas
- Análisis de emociones para detección de estrés

### **🎓 Valor Académico del Proyecto**

Este proyecto demuestra cómo los **conceptos teóricos** de computación visual se materializan en **aplicaciones prácticas reales**. La integración de múltiples talleres no fue simplemente yuxtaposición, sino **síntesis creativa** que resultó en capacidades emergentes:

- **Sinergia técnica**: Cada taller complementó a los otros
- **Validación práctica**: Los conceptos académicos funcionan en aplicaciones reales
- **Arquitectura escalable**: Base sólida para desarrollos futuros
- **Impacto social**: Solución a problemas de seguridad reales
---

## 📚 Referencias y Dependencias


### **Tecnologías Principales:**
- **Python 3.8+**: Lenguaje de programación principal
- **MediaPipe 0.10.14**: Detección facial y landmarks
- **OpenCV 4.9.0**: Procesamiento de video e imágenes
- **TensorFlow 2.12.0**: Backend para modelos de IA
- **DeepFace 0.0.91**: Reconocimiento facial avanzado
- **Tkinter**: Interfaz gráfica nativa
- **NumPy 1.23.5**: Operaciones numéricas

### **Arquitectura del Proyecto:**
```
Access_control/
├── start.py (196 líneas) - Sistema de inicio inteligente
├── simple_modern.py (1,187 líneas) - Interfaz gráfica principal  
├── process/ - Módulos core del sistema
│   ├── face_processing/ - Algoritmos de reconocimiento facial
│   ├── database/ - Gestión de datos persistentes
│   └── gui/ - Componentes de interfaz adicionales
├── examples/ - Ejemplos de uso y demostraciones
├── test/ - Suite de pruebas automatizadas (735 líneas)
└── requirements.txt (91 dependencias) - Gestión de dependencias
```
### **Referencias:**
- **RECONOCIMIENTO FACIAL usando Face Recognition | Python - OpenCV**: [YouTube](https://www.youtube.com/watch?v=51J_bYYMO2k)
- **Build Your Own Face Recognition Tool With Python**: [realpython](https://realpython.com/face-recognition-with-python/)
- **CONTROL DE ACCESO FACIAL CON INTELIGENCIA ARTIFICIAL | Face recognition OpenCV Python**: [YouTube](https://www.youtube.com/watch?v=jxiCDufWop8&t=159s)
- **¿CUÁL ES EL MEJOR MODELO DE RECONOCIMIENTO FACIAL? | Python test**: [YouTube](https://www.youtube.com/watch?v=DCn05o4_pFI)



