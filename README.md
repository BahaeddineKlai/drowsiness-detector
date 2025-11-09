# 🚗 Système de Détection de Somnolence

Application web en temps réel permettant de détecter la somnolence du conducteur à l’aide de la webcam. Elle surveille l’ouverture des yeux grâce à **MediaPipe Face Mesh**, et déclenche une alerte sonore si les yeux restent fermés trop longtemps.

---

## 📌 Fonctionnalités

* ✅ Surveillance en temps réel via la caméra (WebRTC)
* ✅ Détection des yeux via MediaPipe
* ✅ Calcul dynamique du EAR (Eye Aspect Ratio)
* ✅ Alerte sonore automatique en cas de somnolence
* ✅ Interface simple avec indicateurs visuels

---

## 📁 Structure du projet

```
📂 projet/
├── app.py                     # Application Streamlit principale
├── generate_alert_sound.py    # Script permettant de générer alert.wav
├── alert.wav                  # Fichier sonore d'alerte
├── pyproject.toml / requirements.txt
├── .streamlit/
│   └── config.toml            # Configuration visuelle Streamlit
└── README.md
```

---

## 🛠 Installation

### ✅ Prérequis

* Python **3.8 – 3.11**
* Webcam fonctionnelle

### 📥 Cloner le dépôt

```bash
git clone https://github.com/BahaeddineKlai/drowsiness-detector.git
cd VOTRE-REPO
```

## ✅ (Optionnel mais recommandé)
### Créer et activer un environnement virtuel


```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```
### 📦 Installer les dépendances

```bash
 pip install opencv-python mediapipe streamlit numpy
```

> Si le fichier `alert.wav` n’est pas présent, générez-le :

```bash
python generate_alert_sound.py
```

---

## ▶️ Exécuter l’application

```bash
streamlit run app.py
```

Une page web s’ouvrira automatiquement ✅
➡️ Autorisez l’accès à la caméra dans votre navigateur.

---

## ⚙ Paramètres (modifiables dans `app.py`)

```python
EAR_THRESHOLD = 0.25   # Seuil d'ouverture/fermeture des yeux
CLOSED_EYES_TIME = 10  # Durée avant alerte (en secondes)
```

Vous pouvez adapter selon le niveau de vigilance désiré.


WebRTC est déjà configuré ✅

---

## 🧠 Comment ça marche ?

1. Détection du visage avec MediaPipe
2. Suivi permanent des yeux
3. Calcul du EAR (Eye Aspect Ratio)
4. Détection de fermeture prolongée
5. Alerte sonore automatique

---