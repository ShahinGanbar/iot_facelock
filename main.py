import os
import sys
import cv2
import numpy as np
import time
from data_pre import crop_to_3_4
import recognize_faces
from arduino_control import ArduinoController
import serial.tools.list_ports
import warnings
warnings.filterwarnings('ignore')

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
spoof_dir = os.path.join(current_dir, "Silent-Face-Anti-Spoofing")
sys.path.insert(0, spoof_dir)

def find_arduino_port():
    """Find the first available Arduino port"""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description or "USB Serial" in port.description:
            return port.device
    return None

def process_frame_for_liveness(frame):
    """Process a frame and test for liveness using a simplified approach"""
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Basic liveness check (this is a placeholder - you should implement proper liveness detection)
        # For now, we'll consider any clear face image as "real"
        std_dev = np.std(gray)
        brightness = np.mean(gray)
        
        # If image is too blurry or too dark/bright, consider it suspicious
        is_real = std_dev > 30 and 50 < brightness < 200
        score = std_dev / 100  # Normalize score
        
        return 1 if is_real else 0, min(max(score, 0), 1)
        
    except Exception as e:
        print(f"Error during liveness detection: {str(e)}")
        return 0, 0.0

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    # Initialize Arduino controller
    arduino_port = find_arduino_port()
    if arduino_port:
        print(f"Found Arduino on port {arduino_port}")
        arduino = ArduinoController(port=arduino_port)
    else:
        print("Warning: No Arduino found. Door control will be simulated.")
        arduino = None

    # Initialize face detector
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Track door state and last unlock time
    door_locked = True
    last_unlock_time = 0
    unlock_cooldown = 5  # Seconds to wait before allowing another unlock
    
    print("Starting webcam feed. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
            
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Extract face region with padding
            padding = 40
            face_region = frame[max(0, y-padding):min(frame.shape[0], y+h+padding), 
                              max(0, x-padding):min(frame.shape[1], x+w+padding)]
            if face_region.size == 0:
                continue
                
            # Ensure face region has correct aspect ratio
            face_region = crop_to_3_4(face_region)
              # Check liveness
            label, score = process_frame_for_liveness(face_region)
            
            if label == 1:  # Real face detected
                # Perform face recognition
                recognized_name = recognize_faces.recognize_face_from_frame(face_region)
                current_time = time.time()
                
                if recognized_name:
                    # Draw name and "REAL" on frame
                    cv2.putText(frame, f"{recognized_name} (REAL {score:.2f})", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    # Check if enough time has passed since last unlock
                    if current_time - last_unlock_time >= unlock_cooldown:
                        if door_locked and arduino:
                            if arduino.unlock_door():
                                print(f"Door unlocked for {recognized_name}")
                                door_locked = False
                                last_unlock_time = current_time
                        elif arduino is None:
                            print(f"[SIMULATION] Door would unlock for {recognized_name}")
                    
                    # If door is unlocked and cooldown has passed, lock it
                    elif not door_locked and current_time - last_unlock_time >= unlock_cooldown:
                        if arduino and arduino.lock_door():
                            print("Door locked after timeout")
                            door_locked = True
                    
                    # Show door status
                    status = "LOCKED" if door_locked else "UNLOCKED"
                    cv2.putText(frame, f"Door: {status}", (10, frame.shape[0] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if door_locked else (0, 255, 0), 2)
                else:
                    cv2.putText(frame, f"Unknown (REAL {score:.2f})", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # Draw "FAKE" on frame
                cv2.putText(frame, f"FAKE ({score:.2f})", (x, y-10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow('Face Recognition System', frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    if arduino:
        arduino.close()

if __name__ == "__main__":
    main()

