import os
import numpy as np
import cv2
import datetime
from typing import List, Tuple, Any
from process.face_processing.face_detect_models.face_detect import FaceDetectMediapipe
from process.face_processing.face_mesh_models.face_mesh import FaceMeshMediapipe
from process.config_modern import PROCESSING_CONFIG, FILE_CONFIG
from process.utils import FileUtils
try:
    from process.face_processing.face_matcher_models.face_matcher import FaceMatcherModels
    print("✅ Usando modelos de IA completos (DeepFace, TensorFlow)")
except ImportError:
    from process.face_processing.face_matcher_models.face_matcher_opencv import FaceMatcherModelsOpenCV as FaceMatcherModels


class FaceUtils:
    def __init__(self):
        # face detect
        self.face_detector = FaceDetectMediapipe()
        # face mesh
        self.mesh_detector = FaceMeshMediapipe()
        # face matcher
        self.face_matcher = FaceMatcherModels()

        # variables
        self.angle = None
        self.face_db = []
        self.face_names = []
        self.distance: float = 0.0
        self.matching: bool = False
        self.user_registered: bool = False
        # Nuevas variables para mejorar reconocimiento
        self.recognition_attempts = 0
        self.successful_recognitions = []
        self.min_confidence_threshold = PROCESSING_CONFIG.CONFIDENCE_THRESHOLD

    # detect
    def check_face(self, face_image: np.ndarray) -> Tuple[bool, Any, np.ndarray]:
        face_save = face_image.copy()
        check_face, face_info = self.face_detector.face_detect_mediapipe(face_image)
        return check_face, face_info, face_save

    def extract_face_bbox(self, face_image: np.ndarray, face_info: Any):
        h_img, w_img, _ = face_image.shape
        bbox = self.face_detector.extract_face_bbox_mediapipe(w_img, h_img, face_info)
        return bbox

    def extract_face_points(self, face_image: np.ndarray, face_info: Any):
        h_img, w_img, _ = face_image.shape
        face_points = self.face_detector.extract_face_points_mediapipe(h_img, w_img, face_info)
        return face_points

    # face mesh
    def face_mesh(self, face_image: np.ndarray) -> Tuple[bool, Any]:
        check_face_mesh, face_mesh_info = self.mesh_detector.face_mesh_mediapipe(face_image)
        return check_face_mesh, face_mesh_info

    def extract_face_mesh(self, face_image: np.ndarray, face_mesh_info: Any) -> List[List[int]]:
        face_mesh_points_list = self.mesh_detector.extract_face_mesh_points(face_image, face_mesh_info, viz=True)
        return face_mesh_points_list

    def check_face_center(self, face_points: List[List[int]]) -> bool:
        check_face_center = self.mesh_detector.check_face_center(face_points)
        return check_face_center

    # crop
    def face_crop(self, face_image: np.ndarray, face_bbox: List[int]) -> np.ndarray:
        h, w, _ = face_image.shape
        offset_x, offset_y = int(w * PROCESSING_CONFIG.CROP_OFFSET_X_RATIO), int(h * PROCESSING_CONFIG.CROP_OFFSET_Y_RATIO)
        xi, yi, xf, yf = face_bbox
        xi, yi, xf, yf = xi - offset_x, yi - (offset_y * PROCESSING_CONFIG.CROP_OFFSET_Y_MULTIPLIER), xf + offset_x, yf
        return face_image[yi:yf, xi:xf]

    # save
    def save_face(self, face_crop: np.ndarray, user_code: str, path: str):
        if len(face_crop) != 0:
            face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"{path}/{user_code}.png", face_crop)
            return True

        else:
            return False

    # draw
    def show_state_signup(self, face_image: np.ndarray, state: bool):
        # Renderizado de texto simplificado para registro
        if state:
            text = "Guardando rostro..."
            color = PROCESSING_CONFIG.COLOR_SUCCESS
        else:
            text = "Procesando rostro..."
            color = PROCESSING_CONFIG.COLOR_ERROR
        
        # Dibujar texto directamente
        cv2.putText(face_image, text, (10, 50), 
                   PROCESSING_CONFIG.TEXT_FONT, PROCESSING_CONFIG.TEXT_SCALE, 
                   color, PROCESSING_CONFIG.TEXT_THICKNESS)
        
        # Configurar color del mesh según el estado
        self.mesh_detector.config_color(color)

    def show_state_login(self, face_image: np.ndarray, state: bool):
        # Renderizado de texto simplificado para verificación
        if state is True:
            text = "Rostro aprobado"
            color = PROCESSING_CONFIG.COLOR_SUCCESS
        elif state is None:
            text = "Comparando rostro..."
            color = PROCESSING_CONFIG.COLOR_WARNING
        elif state is False:
            text = "Rostro no aprobado"
            color = PROCESSING_CONFIG.COLOR_ERROR
        else:
            text = "Analizando..."
            color = PROCESSING_CONFIG.COLOR_WARNING
        
        # Dibujar texto directamente
        cv2.putText(face_image, text, (10, 50), 
                   PROCESSING_CONFIG.TEXT_FONT, PROCESSING_CONFIG.TEXT_SCALE, 
                   color, PROCESSING_CONFIG.TEXT_THICKNESS)
        
        # Configurar color del mesh según el estado
        self.mesh_detector.config_color(color)

    def read_face_database(self, database_path: str) -> Tuple[List[np.ndarray], List[str], str]:
        self.face_db: List[np.ndarray] = []
        self.face_names: List[str] = []

        # Usar utilidades para obtener archivos válidos
        valid_files = FileUtils.get_valid_image_files(database_path)
        
        for file in valid_files:
            img_path = os.path.join(database_path, file)
            img_read = cv2.imread(img_path)
            if img_read is not None:
                self.face_db.append(img_read)
                self.face_names.append(os.path.splitext(file)[0])

        return self.face_db, self.face_names, f'Comparando {len(self.face_db)} rostros!'

    def face_matching(self, current_face: np.ndarray, face_db: List[np.ndarray], name_db: List[str]) -> Tuple[bool, str]:
        user_name: str = ''
        current_face = cv2.cvtColor(current_face, cv2.COLOR_RGB2BGR)
        
        best_match = False
        best_distance = float('inf')
        best_user = ''
        
        for idx, face_img in enumerate(face_db):
            # Realizar múltiples comparaciones para mayor precisión
            distances = []
            for attempt in range(PROCESSING_CONFIG.RECOGNITION_ATTEMPTS):
                try:
                    matching, distance = self.face_matcher.face_matching_deepface_model(current_face, face_img)
                except:
                    matching, distance = self.face_matcher.face_matching_sface_model(current_face, face_img)
                distances.append(distance)
            
            # Usar la distancia promedio
            avg_distance = sum(distances) / len(distances)
            self.distance = avg_distance
            
            # Usar umbral configurado
            self.matching = avg_distance < PROCESSING_CONFIG.DISTANCE_THRESHOLD
            
            print(f'Verificando rostro de: {name_db[idx]}')
            print(f'Coincidencia: {self.matching} | Distancia: {self.distance:.4f} (promedio de {distances})')
            
            if self.matching and avg_distance < best_distance:
                best_match = True
                best_distance = avg_distance
                best_user = name_db[idx]
        
        if best_match:
            self.successful_recognitions.append(best_distance)
            return True, best_user
            
        return False, 'Rostro desconocido'

    def user_check_in(self, user_name: str, user_path: str):
        if not self.user_registered:
            now = datetime.datetime.now()
            date_time = now.strftime(FILE_CONFIG.DATETIME_FORMAT)
            user_file_path = os.path.join(user_path, f"{user_name}{FILE_CONFIG.USER_FILE_EXTENSION}")
            with open(user_file_path, "a", encoding='utf-8') as user_file:
                user_file.write(f'\n{FILE_CONFIG.LOG_SUCCESS_PREFIX}{date_time}\n')

            self.user_registered = True
