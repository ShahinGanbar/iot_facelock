import cv2
import os
import numpy as np

# Create directories if not exist
os.makedirs('known_faces', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Initialize face detector and recognizer
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

def capture_faces(name, max_images=20):
    """Capture face images manually with live preview"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    person_dir = os.path.join('known_faces', name)
    os.makedirs(person_dir, exist_ok=True)

    print("\n--- Face Capture Started ---")
    print("Press 's' to save a face image")
    print("Press 'q' to finish capturing\n")

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.putText(frame, f"Images saved: {count}/{max_images}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow('Face Capture', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and faces != ():
            file_path = os.path.join(person_dir, f"{name}_{count + 1}.jpg")
            cv2.imwrite(file_path, face)
            print(f"Saved: {file_path}")
            count += 1
            if count >= max_images:
                print("Max images reached.")
                break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def train_recognizer():
    """Train the face recognizer on collected data"""
    faces = []
    labels = []
    label_map = {}
    current_id = 0

    for person_name in os.listdir('known_faces'):
        person_dir = os.path.join('known_faces', person_name)
        if not os.path.isdir(person_dir):
            continue

        label_map[current_id] = person_name

        for filename in os.listdir(person_dir):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                img_path = os.path.join(person_dir, filename)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    faces.append(img)
                    labels.append(current_id)
        current_id += 1

    if len(faces) == 0:
        print("No faces to train on. Please add faces first.")
        return

    face_recognizer.train(faces, np.array(labels))
    face_recognizer.write('models/face_recognizer_model.xml')

    with open('models/label_map.txt', 'w') as f:
        for idx, name in label_map.items():
            f.write(f"{idx},{name}\n")

    print(f"\n✅ Trained recognizer with {len(faces)} faces from {len(label_map)} people.")
    print("Model saved to 'models/face_recognizer_model.xml'")
    print("Label map saved to 'models/label_map.txt'")

def main():
    print("=== Face Trainer ===")
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    capture_faces(name)
    train_recognizer()

if __name__ == "__main__":
    main()
