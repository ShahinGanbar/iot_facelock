import cv2
import numpy as np
import os
from datetime import datetime

# Create logs directory if not exist
os.makedirs('logs', exist_ok=True)

# Load Haar Cascade
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load trained recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
model_path = 'models/face_recognizer_model.xml'
label_map_path = 'models/label_map.txt'

if not os.path.exists(model_path) or not os.path.exists(label_map_path):
    print("Trained model or label map not found. Please run train_faces.py first.")
    exit()

face_recognizer.read(model_path)

# Load label map
label_map = {}
with open(label_map_path, 'r') as f:
    for line in f.readlines():
        label, name = line.strip().split(',', 1)
        label_map[int(label)] = name

def log_recognition(name, confidence):
    """Log recognition to file with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = os.path.join('logs', 'recognition_log.txt')
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - Recognized: {name} ({confidence:.2f}%)\n")

def main():
    print("=== Face Recognition Test Mode ===")
    print("Press 'q' to quit\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (100, 100))

            label, confidence = face_recognizer.predict(face_resized)
            confidence_percent = 100 - confidence

            if confidence_percent > 50:  # Confidence threshold
                name = label_map.get(label, "Unknown")
                label_text = f"{name} ({confidence_percent:.2f}%)"
                log_recognition(name, confidence_percent)
            else:
                name = "Unknown"
                label_text = f"{name} ({confidence_percent:.2f}%)"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
