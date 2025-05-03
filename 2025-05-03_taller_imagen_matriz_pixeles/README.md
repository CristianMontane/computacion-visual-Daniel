# 🧪 Taller - De Pixels a Coordenadas: Explorando la Imagen como Matriz

## 📅 Fecha
`2025-05-03` 

---

## 🎯 Objetivo del Taller

Comprender cómo se representa una imagen digital como una matriz numérica y manipular sus componentes a nivel de píxel. Se abordó cómo trabajar con los valores de color y brillo directamente, accediendo a regiones específicas de la imagen para su análisis o modificación.

---

## 🧠 Conceptos Aprendidos

- [ ] Representación matricial de imágenes digitales
- [ ] Acceso y manipulación de canales RGB y HSV
- [ ] Modificación de regiones específicas mediante slicing de matrices
- [ ] Análisis de histogramas de intensidad de color
- [ ] Ajustes manuales y automatizados de brillo y contraste
- [ ] Implementación de interfaces interactivas con sliders

---

## 🔧 Herramientas y Entornos

- Python con bibliotecas:
  - `opencv-python`: Procesamiento de imágenes
  - `numpy`: Manipulación de matrices
  - `matplotlib`: Visualización de imágenes e histogramas
  - `tkinter` y `PIL`: Interfaz gráfica interactiva

---

## 📁 Estructura del Proyecto

```
2025-05-03_taller_imagen_matriz_pixeles/
├── Capturas/                # Carpeta con imágenes de entrada (J.jpg)
├── python/                  # Código fuente
│   └── matrix_pixeles.ipynb # Notebook con el codigo principal
├── README.md                # Documentación del taller
``` 

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Carga y visualización de imagen utilizando OpenCV
2. Separación y visualización de canales RGB y HSV
3. Manipulación de regiones específicas mediante slicing:
   - Cambio de color en un área rectangular
   - Copia de una región a otra ubicación
4. Cálculo y visualización de histogramas RGB y de escala de grises
5. Aplicación de ajustes de brillo y contraste:
   - Implementación manual mediante ecuación
   - Uso de funciones nativas de OpenCV como `convertScaleAbs`
6. Creación de una herramienta interactiva con sliders para modificar brillo y contraste en tiempo real

### 🔹 Código relevante

```python
# Función para modificar regiones específicas de la imagen
def modify_image_regions(img):
    # Make a copy to avoid modifying the original
    img_modified = img.copy()
    
    height, width = img_modified.shape[:2]
    
    # 1. Change the color of a rectangular area
    x1, y1 = width // 4, height // 4
    x2, y2 = 3 * width // 4, height // 2
    
    # Set the region to a specific color (bright red in BGR)
    img_modified[y1:y2, x1:x2] = [0, 0, 255]  # BGR color
    
    # 2. Copy a region to another location
    src_x1, src_y1 = 0, 0
    src_x2, src_y2 = width // 4, height // 4
    
    # Get exact dimensions
    src_height = src_y2 - src_y1
    src_width = src_x2 - src_x1
    
    # Define destination
    dst_x1, dst_y1 = 3 * width // 4, 3 * height // 4
    dst_x2, dst_y2 = dst_x1 + src_width, dst_y1 + src_height
    
    # Copy the region
    region_to_copy = img_modified[src_y1:src_y2, src_x1:src_x2].copy()
    img_modified[dst_y1:dst_y2, dst_x1:dst_x2] = region_to_copy
    
    return img_modified
```

---

## 📊 Resultados Visuales

### 📌 Canales de Color, manipulación de Regiones y ajustes de Brillo y Contraste

La imagen muestra cómo se pueden modificar áreas específicas de la imagen usando slicing de matrices.Visualización de los canales RGB y HSV separados, permitiendo entender la composición de la imagen en términos de sus componentes de color. Demostración de cómo los cambios en brillo y contraste afectan la apariencia de la imagen, con múltiples combinaciones de parámetros visualizadas simultáneamente.

![Manipulación de Regiones](./Capturas/funcionalidad.gif)


---

## 🧩 Prompts Usados

```text
"Cómo representar una imagen como matriz numérica en Python"
"Técnicas para manipular regiones específicas de una imagen usando slicing de numpy"
"Cómo crear una interfaz con sliders para ajustar brillo y contraste en tiempo real"
```

---

## 💬 Reflexión Final

Este taller me permitió comprender profundamente cómo las imágenes digitales son realmente matrices numéricas que pueden manipularse matemáticamente. La capacidad de acceder a píxeles específicos y modificar valores o regiones enteras abre numerosas posibilidades para el procesamiento de imágenes.

El aspecto más interesante fue la visualización de los canales de color por separado, lo que demuestra cómo se compone cada tono en una imagen. También fue revelador entender que los ajustes de brillo y contraste son simplemente transformaciones matemáticas aplicadas a los valores numéricos de la matriz.

El mayor desafío fue entender las diferencias entre los espacios de color BGR (usado por OpenCV) y RGB (usado por matplotlib), así como asegurar que las dimensiones de las regiones coincidieran exactamente al copiar áreas de una imagen.

Para futuros proyectos, me gustaría explorar operaciones más complejas como transformaciones geométricas, aplicación de filtros convolucionales, y análisis de componentes principales en imágenes. 