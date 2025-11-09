import streamlit as st
import cv2
import time
from drowsiness_detector import (
    calculate_ear, get_eye_points, autoplay_audio,
    mp_face_mesh, mp_drawing,
    LEFT_EYE, RIGHT_EYE,
    EAR_THRESHOLD, CLOSED_EYES_TIME, TIME_PER_FRAME
)

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Détection de Somnolence",
    page_icon="🚗",
    layout="wide"
)


def main():
    st.title("🚗 Système de Détection de Somnolence (Mode Local)")
    st.markdown("### Surveillance de l'état du conducteur via `cv2.VideoCapture`")

    if 'alert_state' not in st.session_state:
        st.session_state.alert_state = False
    if 'eyes_closed_start' not in st.session_state:
        st.session_state.eyes_closed_start = None
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False

    if st.button("Démarrer la Surveillance") and not st.session_state.camera_active:
        st.session_state.camera_active = True
        st.session_state.eyes_closed_start = None
        st.rerun()

    if st.session_state.camera_active and st.button("Arrêter la Surveillance"):
        st.session_state.camera_active = False
        st.session_state.eyes_closed_start = None
        st.rerun()

    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown("### 📊 État actuel")
        status_placeholder = st.empty()
        ear_placeholder = st.empty()
        timer_placeholder = st.empty()
        alert_placeholder = st.empty()
        audio_placeholder = st.empty()

    with col1:
        st.markdown("### 📹 Flux Caméra")
        frame_placeholder = st.empty()

    if st.session_state.camera_active:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5
        )

        status_placeholder.info("Démarrage de la caméra...")

        while st.session_state.camera_active:
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                status_placeholder.error("Erreur de lecture de la caméra.")
                st.session_state.camera_active = False
                st.rerun()
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_height, frame_width = frame.shape[:2]

            results = face_mesh.process(frame_rgb)
            current_ear = 0.0
            elapsed_time = 0.0
            face_detected = False

            if results.multi_face_landmarks:
                face_detected = True
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame, landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                    )

                    left_eye_points = get_eye_points(face_landmarks.landmark, LEFT_EYE, frame_width, frame_height)
                    right_eye_points = get_eye_points(face_landmarks.landmark, RIGHT_EYE, frame_width, frame_height)
                    avg_ear = (calculate_ear(left_eye_points) + calculate_ear(right_eye_points)) / 2.0
                    current_ear = avg_ear

                    cv2.polylines(frame, [left_eye_points], True, (255, 0, 0), 2)
                    cv2.polylines(frame, [right_eye_points], True, (255, 0, 0), 2)

                    if avg_ear < EAR_THRESHOLD:
                        if st.session_state.eyes_closed_start is None:
                            st.session_state.eyes_closed_start = time.time()

                        elapsed_time = time.time() - st.session_state.eyes_closed_start
                        cv2.putText(frame, "YEUX FERMES!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        if elapsed_time >= CLOSED_EYES_TIME:
                            st.session_state.alert_state = True
                            cv2.putText(frame, "!!! ALERTE !!!", (50, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                        else:
                            st.session_state.alert_state = False
                    else:
                        st.session_state.eyes_closed_start = None
                        st.session_state.alert_state = False
                        elapsed_time = 0.0
                        cv2.putText(frame, "YEUX OUVERTS", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    break

            if face_detected:
                if elapsed_time > 0:
                    status_placeholder.error("👁️ YEUX FERMÉS")
                    timer_placeholder.warning(f"Durée: {elapsed_time:.1f}s / {CLOSED_EYES_TIME}s")
                else:
                    status_placeholder.success("✅ YEUX OUVERTS")
                    timer_placeholder.info(f"Durée: 0.0s / {CLOSED_EYES_TIME}s")

                ear_placeholder.metric("EAR", f"{current_ear:.3f}")

                if st.session_state.alert_state:
                    alert_placeholder.error("🚨 ALERTE! RÉVEILLEZ-VOUS! 🚨")
                    with audio_placeholder.container():
                        autoplay_audio("alert.wav")
                else:
                    alert_placeholder.empty()
                    audio_placeholder.empty()
            else:
                status_placeholder.warning("⚠️ Aucun visage détecté")
                ear_placeholder.empty()
                timer_placeholder.empty()
                alert_placeholder.empty()
                audio_placeholder.empty()

            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

            end_time = time.time()
            processing_time = end_time - start_time
            sleep_time = max(0, TIME_PER_FRAME - processing_time)
            time.sleep(sleep_time)

        cap.release()
        face_mesh.close()

    else:
        status_placeholder.info("⏸️ Appuyez sur 'Démarrer la Surveillance' pour commencer.")
        ear_placeholder.empty()
        timer_placeholder.empty()
        alert_placeholder.empty()

    st.markdown("---")
    st.markdown(f"""
    ### 📋 Note Importante : Mode Local
    Cette version utilise **OpenCV (`cv2.VideoCapture`)** et ne fonctionne que sur la machine locale.

    ### ⚙️ Paramètres:
    - **Seuil EAR**: {EAR_THRESHOLD:.2f}
    - **Temps d'alerte**: {CLOSED_EYES_TIME} secondes
    """)


if __name__ == "__main__":
    main()
