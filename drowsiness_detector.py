import mediapipe as mp
import numpy as np
from scipy.spatial import distance
import base64
import streamlit as st

# --- CONSTANTES ---
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

EAR_THRESHOLD = 0.25
CLOSED_EYES_TIME = 10
FRAME_RATE_FOR_SLEEP = 30
TIME_PER_FRAME = 1 / FRAME_RATE_FOR_SLEEP


# --- FONCTIONS UTILES ---

def calculate_ear(eye_points):
    """Calcule l'Eye Aspect Ratio (EAR)"""
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    C = distance.euclidean(eye_points[0], eye_points[3])
    ear = (A + B) / (2.0 * C)
    return ear


def get_eye_points(landmarks, eye_indices, frame_width, frame_height):
    """Extrait les coordonnées des points de l'œil"""
    points = []
    for idx in eye_indices:
        point = landmarks[idx]
        x = int(point.x * frame_width)
        y = int(point.y * frame_height)
        points.append((x, y))
    return np.array(points)


def autoplay_audio(file_path):
    """Joue automatiquement un fichier audio côté client"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay loop>
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Fichier audio '{file_path}' non trouvé. L'alerte sera visuelle uniquement.")
