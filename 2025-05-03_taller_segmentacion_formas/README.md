# 🧪 Taller - Segmentando el Mundo: Binarización y Reconocimiento de Formas

## 📅 Fecha
`2025-05-03` 

---

## 🎯 Objetivo del Taller

Aplicar técnicas básicas de segmentación en imágenes mediante umbralización y detección de formas simples. El objetivo es comprender cómo identificar regiones de interés en imágenes mediante procesos de binarización y análisis de contornos.

---

## 🧠 Conceptos Aprendidos


- [ ] Segmentación binaria por umbral fijo (`cv2.threshold`)
- [ ] Segmentación binaria por umbral adaptativo (`cv2.adaptiveThreshold`)
- [ ] Detección de contornos con `cv2.findContours()`
- [ ] Cálculo del centro de masa de cada forma (`cv2.moments()`)
- [ ] Dibujado de bounding boxes (`cv2.boundingRect()`)
- [ ] Cálculo de métricas: número de formas, área y perímetro promedio
- [ ] Procesamiento en tiempo real de webcam y segmentación adaptativa

---

## 🔧 Herramientas y Entornos

- Python (`opencv-python`, `numpy`, `matplotlib`)
- Jupyter Notebook o Google Colab
- OpenCV para procesamiento de imágenes y video

---

## 📁 Estructura del Proyecto

```plaintext
2025-05-03_taller_segmentacion_formas/
├── python/                 # Script principal de segmentación (reconocimiento.py)
├── Capturas/               # Imágenes y GIFs resultantes de la segmentación
├── README.md               # Documentación del taller
```  

---

## 🧪 Implementación

### 🔹 Etapas realizadas
1. Lectura de la imagen en escala de grises.
2. Aplicación de un **umbral fijo** (valor 127) para segmentación binaria.
3. Aplicación de un **umbral adaptativo** (método Gaussiano) para comparación.
4. Detección de contornos externos con `cv2.findContours()`.
5. Cálculo y marcado del **centro de masa** de cada contorno usando momentos.
6. Dibujado de **bounding boxes** alrededor de cada forma detectada.
7. Cálculo de métricas: número de formas, área promedio y perímetro promedio.
8. Procesamiento de vídeo en tiempo real desde la webcam con segmentación adaptativa y dibujo de cajas en vivo.

### 🔹 Código relevante

```python
import cv2
import numpy as np

# Carga y binarización
gris = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
_, bin_fijo = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
bin_adap = cv2.adaptiveThreshold(
    gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)

# Detección de contornos
contornos, _ = cv2.findContours(bin_adap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Cálculo de métricas y dibujo
dest = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
for c in contornos:
    M = cv2.moments(c)
    if M['m00']:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(dest, (cx, cy), 4, (0,0,255), -1)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(dest, (x,y), (x+w,y+h), (255,0,0), 2)
```

---

## 📊 Resultados Visuales

Se incluyen a continuación los resultados mostrando la imagen original en gris, binarización fija y adaptativa, y resultado final con contornos, bounding boxes y prueba de camara en vivo:

![Segmentación](./Capturas/segmentacion_estatica.gif)


---

## 🧩 Prompts Usados

```text
"Cómo aplicar detección de contornos externos usando OpenCV en Python?"
"Como usar el procesamiento de vídeo en tiempo real con segmentación adaptativa y dibujo de cajas en vivo?"
"Como calcular y marcar el centro de masa de cada contorno usando momentos"
```

---

## 💬 Reflexión Final

Este taller reforzó mi entendimiento de las técnicas de segmentación básicas mediante umbralización y análisis de contornos, y cómo estos pasos permiten extraer características geométricas de formas en una imagen. La parte más interesante fue contrastar los resultados entre umbral fijo y adaptativo, observando cómo el método adaptativo se ajusta mejor a variaciones locales de iluminación.

El mayor desafío fue asegurar que los contornos externos recolectados correspondieran a formas relevantes y evitar ruido, así como calcular correctamente los momentos para el centro de masa. Para futuros proyectos, me gustaría explorar técnicas de segmentación más avanzadas, como contornos jerárquicos y segmentación semántica.
