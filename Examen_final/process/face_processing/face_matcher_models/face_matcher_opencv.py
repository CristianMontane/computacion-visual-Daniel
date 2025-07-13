import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple


class FaceMatcherModelsOpenCV:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)
        
    def face_distance(self, face_encodings, face_to_compare):
        """Calculate distance between face encodings"""
        if len(face_encodings) == 0:
            return np.empty((0))
        return np.linalg.norm(face_encodings - face_to_compare, axis=1)
    
    def face_recognition_opencv(self, known_image, unknown_image):
        """Basic face recognition using OpenCV and MediaPipe"""
        try:
            # Convert images to RGB
            known_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
            unknown_rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
            
            # Get face landmarks for both images
            known_results = self.face_mesh.process(known_rgb)
            unknown_results = self.face_mesh.process(unknown_rgb)
            
            if known_results.multi_face_landmarks and unknown_results.multi_face_landmarks:
                # Extract landmarks as features
                known_landmarks = []
                unknown_landmarks = []
                
                for landmark in known_results.multi_face_landmarks[0].landmark:
                    known_landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                for landmark in unknown_results.multi_face_landmarks[0].landmark:
                    unknown_landmarks.extend([landmark.x, landmark.y, landmark.z])
                
                # Calculate similarity
                known_features = np.array(known_landmarks)
                unknown_features = np.array(unknown_landmarks)
                
                distance = np.linalg.norm(known_features - unknown_features)
                
                # Threshold for face match (ajustado para mejor funcionamiento)
                threshold = 1.0  # Más permisivo para mejorar reconocimiento
                is_match = distance < threshold
                
                return is_match, distance
            else:
                return False, 1.0
                
        except Exception as e:
            print(f"Error in face recognition: {e}")
            return False, 1.0
    
    def face_verification_opencv(self, img1_path: str, img2_path: str) -> Tuple[bool, float]:
        """Verify if two face images belong to the same person"""
        try:
            img1 = cv2.imread(img1_path)
            img2 = cv2.imread(img2_path)
            
            if img1 is None or img2 is None:
                return False, 1.0
            
            is_match, distance = self.face_recognition_opencv(img1, img2)
            return is_match, distance
            
        except Exception as e:
            print(f"Error in face verification: {e}")
            return False, 1.0

    def face_verification(self, img1_path: str, img2_path: str, model_name: str = "opencv") -> Tuple[bool, float]:
        """Wrapper method to maintain compatibility"""
        return self.face_verification_opencv(img1_path, img2_path)

    def face_matching_sface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """SFace model compatibility method using OpenCV fallback"""
        try:
            is_match, distance = self.face_recognition_opencv(face_1, face_2)
            return is_match, distance
        except Exception as e:
            print(f"Error in SFace model fallback: {e}")
            return False, 1.0

    def face_matching_face_recognition_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """Face Recognition model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_vgg_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """VGG model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_facenet_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """FaceNet model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_facenet512_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """FaceNet512 model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_openface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """OpenFace model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_deepface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """DeepFace model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_deepid_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """DeepID model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_arcface_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """ArcFace model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_dlib_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """Dlib model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)

    def face_matching_ghostfacenet_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        """GhostFaceNet model compatibility method"""
        return self.face_matching_sface_model(face_1, face_2)
