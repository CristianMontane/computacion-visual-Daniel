import os
import sys
from tkinter import *
import logging as log

log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Usar la nueva interfaz moderna
from simple_modern import SimpleModernGUI

# Crear y ejecutar la aplicación moderna
if __name__ == "__main__":
    root = Tk()
    root.title("Sistema de Reconocimiento Facial Moderno - Ejemplo")
    
    app = SimpleModernGUI(root)
    root.mainloop()
