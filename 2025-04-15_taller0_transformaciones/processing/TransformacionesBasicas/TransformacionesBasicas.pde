void setup() {
  size(800, 600, P3D); // Configuramos el tamaño y modo 3D
  smooth(); // Activamos el suavizado
}

void draw() {
  background(0); // Fondo negro
  
  // Configuramos una luz para mejor visualización 3D
  lights();
  
  // Trasladamos todo al centro de la pantalla
  translate(width/2, height/2, 0);
  
  // Creamos un movimiento ondulatorio horizontal basado en el tiempo
  float xOffset = sin(frameCount * 0.02) * 150;
  
  // Guardamos la transformación actual
  pushMatrix();
  
  // Aplicamos la traslación ondulada
  translate(xOffset, 0, 0);
  
  // Aplicamos rotación en varios ejes, variando con el tiempo
  rotateX(frameCount * 0.01);
  rotateY(frameCount * 0.02);
  rotateZ(frameCount * 0.005);
  
  // Calculamos un factor de escala que varía con el tiempo
  float scaleFactor = map(sin(frameCount * 0.03), -1, 1, 0.5, 1.5);
  
  // Aplicamos la escala
  scale(scaleFactor);
  
  // Configuramos el color de la esfera, variando con el tiempo
  float r = map(sin(frameCount * 0.02), -1, 1, 100, 255);
  float g = map(cos(frameCount * 0.03), -1, 1, 50, 200);
  float b = map(sin(frameCount * 0.01), -1, 1, 150, 255);
  
  fill(r, g, b);
  stroke(255);
  strokeWeight(1);
  
  // Dibujamos la esfera
  sphere(100);
  
  // Restauramos la transformación anterior
  popMatrix();
  
  // Añadimos información en pantalla
  fill(255);
  textAlign(LEFT);
  textSize(14);
  text("Esfera 3D con transformaciones animadas", -width/2 + 20, -height/2 + 30);
  text("Traslación X: " + nf(xOffset, 0, 2), -width/2 + 20, -height/2 + 70);
  text("Escala: " + nf(scaleFactor, 0, 2), -width/2 + 20, -height/2 + 90);
}
