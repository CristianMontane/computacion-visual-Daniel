"""
Configuración simplificada para la interfaz moderna de reconocimiento facial.
Solo contiene las configuraciones necesarias para la nueva interfaz.
"""
from dataclasses import dataclass
from typing import Tuple
import cv2


@dataclass
class VideoConfig:
    """Configuración de video y cámara para la interfaz moderna"""
    WIDTH: int = 1400
    HEIGHT: int = 800
    CAMERA_INDEX: int = 0
    FPS: int = 30
    
    # Configuración para cámara en ventanas de captura (interfaz moderna)
    CAPTURE_WIDTH: int = 640
    CAPTURE_HEIGHT: int = 480
    
    @property
    def geometry(self) -> str:
        return f"{self.WIDTH}x{self.HEIGHT}"
    
    @property
    def capture_geometry(self) -> str:
        return f"{self.CAPTURE_WIDTH}x{self.CAPTURE_HEIGHT}"
    
    @property
    def resolution_text(self) -> str:
        return f"{self.WIDTH}x{self.HEIGHT}"


@dataclass
class ProcessingConfig:
    """Configuración básica de procesamiento para reconocimiento facial"""
    # Configuración de reconocimiento facial
    FACE_CONFIDENCE: float = 0.6
    FACE_MODEL: str = "VGG-Face"
    CONFIDENCE_THRESHOLD: float = 0.5
    DISTANCE_THRESHOLD: float = 1.2
    
    # Configuración de captura
    CAPTURE_DELAY: int = 3
    FRAME_SKIP: int = 5
    FRAME_COUNT_THRESHOLD: int = 48
    RECOGNITION_ATTEMPTS: int = 3
    
    # Configuración de recorte de rostro
    CROP_OFFSET_X_RATIO: float = 0.1
    CROP_OFFSET_Y_RATIO: float = 0.1
    CROP_OFFSET_Y_MULTIPLIER: int = 2
    
    # Colores básicos para feedback visual
    COLOR_SUCCESS: Tuple[int, int, int] = (0, 255, 0)  # Verde
    COLOR_ERROR: Tuple[int, int, int] = (0, 0, 255)    # Rojo
    COLOR_WARNING: Tuple[int, int, int] = (0, 255, 255) # Amarillo
    COLOR_BLACK: Tuple[int, int, int] = (0, 0, 0)      # Negro
    
    # Configuración de texto en video (si se necesita)
    TEXT_FONT: int = cv2.FONT_HERSHEY_SIMPLEX
    TEXT_SCALE: float = 0.7
    TEXT_THICKNESS: int = 2
    TEXT_X_PRIMARY: int = 10
    TEXT_X_SECONDARY: int = 10
    TEXT_Y_POSITION: int = 50
    TEXT_OFFSET_Y: int = 5


@dataclass
class FileConfig:
    """Configuración de archivos para la interfaz moderna"""
    USER_FILE_EXTENSION: str = ".txt"
    VALID_IMAGE_EXTENSIONS: list = (".png", ".jpg", ".jpeg")
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_SUCCESS_PREFIX: str = "✅ Acceso exitoso: "
    LOG_FAILURE_PREFIX: str = "❌ Acceso fallido: "


# Instancias globales para uso en el sistema
VIDEO_CONFIG = VideoConfig()
PROCESSING_CONFIG = ProcessingConfig()
FILE_CONFIG = FileConfig()
