"""
Utilidades modernas para el sistema de reconocimiento facial.
Solo contiene las utilidades necesarias para la nueva interfaz moderna.
"""
import cv2
import imutils
from PIL import Image, ImageTk
from tkinter import messagebox
from typing import Tuple
import numpy as np
import os

from process.config_modern import VIDEO_CONFIG


class VideoProcessor:
    """Procesador de video reutilizable para la interfaz moderna"""
    
    @staticmethod
    def setup_camera(camera_index: int = VIDEO_CONFIG.CAMERA_INDEX) -> cv2.VideoCapture:
        """Configura y retorna la cámara con las configuraciones predeterminadas"""
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_CONFIG.WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_CONFIG.HEIGHT)
        return cap
    
    @staticmethod
    def process_frame_large(frame_bgr: np.ndarray, target_width: int = 720) -> Tuple[np.ndarray, ImageTk.PhotoImage]:
        """Procesa un frame de BGR a RGB para ventanas más grandes"""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_resized = imutils.resize(frame_rgb, width=target_width)
        pil_image = Image.fromarray(frame_resized)
        tk_image = ImageTk.PhotoImage(image=pil_image)
        return frame_resized, tk_image


class WindowManager:
    """Gestor de ventanas para la interfaz moderna"""
    
    @staticmethod
    def create_window(title: str, parent=None):
        """Crea una ventana moderna estandarizada"""
        from tkinter import Toplevel
        
        if parent:
            window = Toplevel(parent)
        else:
            window = Toplevel()
        
        window.title(title)
        window.geometry("900x750")  # Tamaño moderno más grande
        return window
    
    @staticmethod
    def create_video_label(parent):
        """Crea un label para mostrar video en la interfaz moderna"""
        from tkinter import Label
        video_label = Label(parent)
        video_label.place(x=0, y=0)
        return video_label


class MessageHandler:
    """Manejador de mensajes del sistema moderno"""
    
    @staticmethod
    def print_startup_messages():
        """Imprime mensajes de inicio del sistema moderno"""
        print("🚀 Sistema de Reconocimiento Facial Moderno - Iniciando...")
        print("🎯 Modo: Interfaz Moderna con Cámara en Tiempo Real")
        print(f"📹 Configurando cámara en resolución {VIDEO_CONFIG.resolution_text}...")
    
    @staticmethod
    def print_identity_verified():
        """Imprime mensaje de identidad verificada"""
        print("✅ IDENTIDAD VERIFICADA - Usuario reconocido exitosamente")
        print("👤 Coincidencia facial confirmada")
    
    @staticmethod
    def print_identity_not_verified():
        """Imprime mensaje de identidad no verificada"""
        print("❌ IDENTIDAD NO VERIFICADA - Usuario no reconocido")
        print("🔍 No se encontró coincidencia facial")
    
    @staticmethod
    def print_registration_success():
        """Imprime mensaje de registro exitoso"""
        print("✅ REGISTRO EXITOSO - Rostro capturado y guardado")
        print("👤 Usuario registrado correctamente en la base de datos")
    
    @staticmethod
    def print_window_closing(window_type: str):
        """Imprime mensaje de cierre de ventana"""
        print(f"🔒 Cerrando ventana de {window_type}...")
    
    @staticmethod
    def print_registration_start(name: str, user_code: str):
        """Imprime mensaje de inicio de registro"""
        print(f"📝 Registrando nuevo usuario: {name} (Código: {user_code})")
    
    @staticmethod
    def show_info(message: str, title: str = "Información"):
        """Muestra un mensaje de información"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(message: str, title: str = "Advertencia"):
        """Muestra un mensaje de advertencia"""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_error(message: str, title: str = "Error"):
        """Muestra un mensaje de error"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_confirmation(message: str, title: str = "Confirmación") -> bool:
        """Muestra un diálogo de confirmación y retorna la respuesta"""
        return messagebox.askyesno(title, message)


class DatabaseUtils:
    """Utilidades para manejo de base de datos simplificadas"""
    
    @staticmethod
    def get_registered_users(database_path: str) -> list:
        """Obtiene la lista de usuarios registrados"""
        user_codes = []
        try:
            user_list = os.listdir(database_path)
            for user_file in user_list:
                if user_file.endswith('.txt'):
                    user_code = user_file.split('.')[0]
                    user_codes.append(user_code)
        except FileNotFoundError:
            print(f"⚠️ Directorio de base de datos no encontrado: {database_path}")
        return user_codes


class FileUtils:
    """Utilidades básicas para manejo de archivos"""
    
    @staticmethod
    def ensure_directory_exists(path: str) -> None:
        """Asegura que un directorio exista, creándolo si es necesario"""
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            print(f"❌ Error al crear directorio {path}: {e}")
    
    @staticmethod
    def get_valid_image_files(directory: str) -> list:
        """Obtiene una lista de archivos de imagen válidos en un directorio"""
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
        image_files = []
        
        try:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        file_extension = os.path.splitext(file)[1].lower()
                        if file_extension in valid_extensions:
                            image_files.append(file)
            else:
                print(f"⚠️ Directorio no encontrado: {directory}")
        except Exception as e:
            print(f"❌ Error al leer archivos de imagen en {directory}: {e}")
        
        return image_files
