import os
import cv2
import numpy as np
import face_recognition
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

st.set_page_config(page_title="Face Recognition Dashboard", page_icon=":zap:", layout="wide")

st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(120deg, #181825 0%, #232946 55%, #123452 100%) !important;
        color: #eee !important;
    }
    .glassmorph {
        background: rgba(30,34,44,0.94) !important;
        border-radius: 23px;
        box-shadow: 0 8px 44px 0 rgba(10,24,38,0.60);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(128,221,255,0.15);
        padding:2.3rem 2.5rem 1.8rem 2.5rem; margin-bottom:2.2rem;
    }
    .stTitle {
        color: #bbeaff;
        text-shadow: 0 0 16px #0ff,0 0 6px #5efce8,0 0 1px #070a1a;
        font-family:'Segoe UI','Roboto',sans-serif;font-weight:900;font-size:2.85rem;margin-bottom:8px;
    }
    .stButton button, .stFileUploader {
        background: #218bfa !important; color:#fff; border-radius:18px !important;
        font-size:1.06rem;font-weight:700;padding:0.5em 2.4em;box-shadow: 0 0 14px 2px #08f7fe;
    }
    .stButton button:hover { background: linear-gradient(70deg,#00f2fe,#09e8eb,#218bfa); color:#222;}
    .score-highlight {font-size:1.23rem;font-weight:900;animation:glowscore 1.13s infinite alternate;
        text-shadow: 0 0 14px #09e8eb,0 0 5px #bbeaff,0 0 1px #fff;}
    @keyframes glowscore {from{color:#fcfc62;}to{color:#08f7fe;}}
    .match-msg {font-size:1.11rem;font-weight:700;letter-spacing:.7px;}
    .stProgress > div > div {
        background: linear-gradient(90deg,#ffd700 5%,#00f2fe 70%,#2481fa 100%)!important;
        height:1.43em !important;border-radius:15px;
    }
    .stMarkdown h2 {color: #77f7ff; letter-spacing:.01em;}
    .stRadio > div {color: #09e8eb; font-size:1.13rem;font-weight:800;}
    section[data-testid="stFileUploader"] label {color:#ffe492!important;}
    .glassmorph:hover { box-shadow: 0 0 50px 8px #08f7fe8f;border: 1.5px solid #ffe49273; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="stTitle" style="text-align:center;">⚡ Face Detection & Recognition Dashboard ⚡</div>', unsafe_allow_html=True)
st.markdown(
    "<div class='glassmorph' style='margin-top:1.7rem;text-align:center;'>"
    "Recognize faces from cam or upload, and now add new faces by <span style='color:#ffe492'>Upload</span> or <span style='color:#08f7fe'>Webcam</span>!"
    "<br><span style='color:#8cfafe;font-weight:650'></span></div>",
    unsafe_allow_html=True
)

known_face_encodings, known_face_names = [], []
known_faces_dir = "known_faces"
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)
for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(known_faces_dir, filename)
        img = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(img)
        if encs:
            known_face_encodings.append(encs[0])
            known_face_names.append(os.path.splitext(filename)[0])

def draw_glowing_box(image, box, color_base=(8,247,254)):
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image, "RGBA")
    top, right, bottom, left = box
    for radius in range(12, 0, -3):
        alpha = int(16 + 25*(radius/12))
        draw.rectangle(
            [left-radius, top-radius, right+radius, bottom+radius],
            outline=tuple(list(color_base)+[alpha]), width=4+radius//6)
    return np.array(pil_image)

def detect_faces(image_np):
    face_locations = face_recognition.face_locations(image_np)
    face_encodings = face_recognition.face_encodings(image_np, face_locations)
    pil_image = Image.fromarray(image_np)
    draw = ImageDraw.Draw(pil_image, "RGBA")
    result_names, result_scores = [], []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        color = (255, 228, 146)  # faint gold for unknown
        score = 0.0
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            score = float((1-face_distances[best_match_index]))
            score = max(0.0, min(1.0, score))
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                color = (8,247,254)  # neon cyan
        glowing_img = draw_glowing_box(np.array(pil_image), (top, right, bottom, left), color)
        pil_image = Image.fromarray(glowing_img)
        draw = ImageDraw.Draw(pil_image, "RGBA")
        draw.rectangle([left, top, right, bottom], outline=color+(220,), width=4)
        label = f"{name} ({int(score*100)}%)"
        draw.rectangle([left, bottom+8, right, bottom+36], fill=color+(80,))
        try: 
            font = ImageFont.truetype("arial.ttf", size=21)
        except: 
            font = None
        draw.text((left+6, bottom+12), label, fill="white", font=font)
        result_names.append(name)
        result_scores.append(score)
    return np.array(pil_image), face_locations, face_encodings, result_names, result_scores

st.markdown("## ➕ Add a Known Face")
with st.expander("Add new known face (upload OR webcam, single face):", expanded=False):
    c1, c2 = st.columns([1.4,1.4])
    with c1:
        add_face_file = st.file_uploader("Upload Face Image", type=['jpg','jpeg','png'], key="known_upload")
        add_face_name = st.text_input("Name for Upload:", max_chars=32, key="known_nameU")
        addbtn = st.button("Add by Upload", key="add_face_btn")
    with c2:
        st.markdown("#### ...or <span style='color:#09e8eb'>Webcam</span>", unsafe_allow_html=True)
        webcam_face_name = st.text_input("Name for Webcam:", key="webcam_face_name", max_chars=32)
        start_webcam = st.button("Capture from Webcam", key="start_webcam_btn")
        cam_display = st.empty()
        webcam_save = st.empty()

        if start_webcam and webcam_face_name:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("🚫 Webcam could not be opened. Please ensure it is connected and accessible.")
            else:
                st.info("Position your face, look at the cam, brightly lit background!", icon="📸")
                captured = False
                try:
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            st.warning("Webcam frame not accessible. Closing webcam.")
                            break
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        cam_display.image(rgb_frame, caption="Live webcam (press button to save)", channels="RGB", use_container_width=True)
                        save = webcam_save.button("Save This Shot!", key="save_btn")
                        if save and not captured:
                            camimg = Image.fromarray(rgb_frame)
                            encs = face_recognition.face_encodings(rgb_frame)
                            if len(encs) != 1:
                                st.error("Please ensure ONLY ONE clear face is visible in frame.")
                            else:
                                file_path = os.path.join(known_faces_dir, webcam_face_name.replace(" ","_")+".jpg")
                                camimg.save(file_path)
                                st.balloons()
                                st.success("🟦 Face captured & added! Rerun app to use for recognition.")
                                captured = True
                                break
                finally:
                    cap.release()
                    cam_display.empty()
                    webcam_save.empty()

    if addbtn:
        if add_face_file and add_face_name:
            img = Image.open(add_face_file).convert("RGB")
            img_np = np.array(img)
            encs = face_recognition.face_encodings(img_np)
            if len(encs) != 1:
                st.error("⚠️ Image must have EXACTLY ONE face (clear face, portrait preferred).")
            else:
                file_path = os.path.join(known_faces_dir, add_face_name.replace(" ","_")+".jpg")
                img.save(file_path)
                st.balloons()
                st.success("★ Face added to known faces! Rerun app to recognize it.")
        else:
            st.warning("Please provide a name and a face image.")

def show_match_feedback(names, scores):
    feedback_container = st.container()
    with feedback_container:
        for i, (name, score) in enumerate(zip(names, scores)):
            glow = f"<span class='score-highlight'>{int(score*100)}%</span>"
            timestamp = datetime.now().isoformat(sep=' ', timespec='milliseconds')
            label_color = "#08f7fe" if name != "Unknown" and score >= 0.55 else "#ffe492"
            if name != "Unknown" and score>=0.55:
                msg = (f"Detected: <b>{name}</b> (Match Score: {score:.2f}) at {timestamp}")
                st.markdown(f"<p style='color:{label_color};font-weight:bold;'>{msg}</p>", unsafe_allow_html=True)
                if score >= 0.85:
                    st.success(f"💠 High confidence: {name}")
            else:
                msg = (f"Detected: Unknown (Match Score: {score:.2f}) at {timestamp}")
                st.markdown(f"<p style='color:{label_color};font-weight:bold;'>{msg}</p>", unsafe_allow_html=True)
            st.progress(score, text=f"Confidence: {int(score*100)}%")

st.markdown('<div class="glassmorph">', unsafe_allow_html=True)
st.markdown("<h2>🔎 Recognize Faces</h2>", unsafe_allow_html=True)
option = st.radio("Choose an option:", ["Upload Image", "Webcam Detection"], horizontal=True)

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload image for recognition", type=["jpg","jpeg","png"], key="recog_upload")
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)
        with st.spinner("Detecting & recognizing..."):
            result_img, locations, encodings, names, scores = detect_faces(image_np)
        st.image(result_img, caption="Neon Dark Recognition Result", channels="RGB", use_container_width=True)
        if locations:
            st.success(f"{len(locations)} face(s) detected!")
            show_match_feedback(names, scores)
            if any(n!="Unknown" and s>=0.7 for n,s in zip(names,scores)):
                st.snow()
        else:
            st.warning("No faces detected! Try another shot or more lighting.")

elif option == "Webcam Detection":
    st.markdown("**Allow webcam. Best in bright face/clean dark BG, face forward.**")
    run = st.checkbox("Start Webcam")
    FRAME_WINDOW = st.image([])
    feedback_display = st.empty()
    cap = None
    if run:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("🚫 Webcam could not be opened. Please ensure permission is granted and no other app is using the camera.")
        else:
            prev_faces = 0
            try:
                while run:
                    ret, frame = cap.read()
                    if not ret:
                        st.warning("Webcam frame not accessible. Stopping webcam.")
                        break
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    res_frame, locations, encodings, names, scores = detect_faces(rgb_frame)
                    FRAME_WINDOW.image(res_frame, channels="RGB", use_container_width=True)
                    feedback_display.empty()
                    with feedback_display.container():
                        show_match_feedback(names, scores)
                    face_cnt = len(locations)
                    if face_cnt > prev_faces: st.snow()
                    elif face_cnt < prev_faces: st.balloons()
                    prev_faces = face_cnt
            finally:
                cap.release()
                st.success("Webcam stopped.")
    else:
        if cap is not None:
            cap.release()
        FRAME_WINDOW.empty()
        feedback_display.empty()

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color: #8cfafe;'>"
    "<i>All work is local & safe. Only your added faces are stored, nothing else.<br></i>"
    "</div>", unsafe_allow_html=True
)
