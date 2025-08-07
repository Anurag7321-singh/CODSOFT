import cv2
import os
import face_recognition
import numpy as np

# Paths
HAAR_CASCADE_PATH = "haarcascades/haarcascade_frontalface_default.xml"
KNOWN_FACES_DIR = "known_faces"  # Optional: Add images of known people here

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

# Load known faces (if any) for recognition
known_encodings = []
known_names = []

if os.path.exists(KNOWN_FACES_DIR):
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])

def detect_and_recognize(image):
    """
    Detect and recognize faces in an image.
    Returns the image with bounding boxes and names (if recognized).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)

    for (x, y, w, h) in faces:
        name = "Unknown"
        face_roi = rgb_img[y:y+h, x:x+w]
        face_encoding = face_recognition.face_encodings(face_roi)

        if face_encoding and known_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding[0])
            face_distances = face_recognition.face_distance(known_encodings, face_encoding[0])
            best_match = np.argmin(face_distances)
            if matches[best_match]:
                name = known_names[best_match]

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return image

def main():
    print("[INFO] Starting Face Detection & Recognition...")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = detect_and_recognize(frame)
        cv2.imshow("Face Detection and Recognition", processed_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):  # Press 'q' to quit
            break
        elif key == ord('s'):  # Press 's' to save frame
            cv2.imwrite("detected_frame.jpg", processed_frame)
            print("[INFO] Frame saved as detected_frame.jpg")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
