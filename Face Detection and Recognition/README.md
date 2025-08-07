# 🧑‍💻 Face Detection and Recognition Web App

This Streamlit web app allows real-time **Face Detection and Recognition** using:
- Pre-trained Haar Cascade for face detection
- `face_recognition` for face matching
- Upload & Webcam support
- Match score-based logging
- Blue futuristic background theme

---

## 🚀 Features
- 📸 Upload image or use your webcam
- 🧠 Recognize faces against pre-uploaded known faces
- ✅ Logging: `"Detected: anurag (Match Score: 0.42)"`
- 🧾 Automatically tags unknown or known faces

---

## 🗂 Folder Structure

```
Face Detection and Recognition/
├── haarcascades/
│   └── haarcascade_frontalface_default.xml  # For optional OpenCV detection
├── known_faces/
│   └── [Your known face images here]
├── detection_log.txt        # Logs detection with match scores
├── face_app.py              # Main Streamlit App
├── face_detection.py        # (Optional) Standalone face detection script
├── faceimg.jpeg             # Blue background for Streamlit
├── README.md                # Project README
└── requirements.txt         # Python dependencies

```

---

## ⚙️ Requirements

Install these first:

```bash
pip install opencv-python
pip install face_recognition
pip install streamlit
```

> Make sure `dlib` is installed properly (auto-installed with `face_recognition`)  
> Use Python 3.8–3.10 for smooth compatibility with `face_recognition` + `dlib`.

---

## 🧪 How to Run

```bash
streamlit run face_app.py
```

Then select:
- “Upload Image” → to test face recognition on an image
- “Webcam Detection” → for live face detection & recognition

---

## 📷 Adding Known Faces

Put images in the `known_faces/` folder with filenames like:

```
known_faces/
├── anurag.jpg
├── gunnar.png
└── rider.jpeg
```

These are auto-loaded into the system.

---

## ✅ Output Example

When a match is found:

```
Detected: anurag (Match Score: 0.42)
```

Unknown face example:

```
Detected: Unknown (Match Score: 0.12)
```

---



---

## 👨‍💻 Credits

- Developed by **Anurag Pratap Singh**
- Tools used: Python, OpenCV, face_recognition, Streamlit

---

## 📌 Notes

- Ensure images in `known_faces/` are clear front-facing headshots
- Match score is displayed for every detection
- Performance may vary by lighting and camera quality

---
