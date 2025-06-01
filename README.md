# Face Recognition Door Lock System

This project implements a secure door lock system using facial recognition and anti-spoofing technology. The system uses a combination of OpenCV for face detection, Silent-Face-Anti-Spoofing for liveness detection, and an Arduino-controlled servo motor for the door lock mechanism.

## Features

- Face detection and recognition using OpenCV
- Anti-spoofing protection against photo/video attacks
- Arduino-controlled servo motor for door lock
- Logging system for access attempts
- Real-time webcam monitoring
- Support for multiple authorized users

## Hardware Requirements

- Webcam
- Arduino board (Uno/Nano/etc.)
- Servo motor (for door lock mechanism)
- USB cable for Arduino connection

## Software Requirements

- Python 3.8
- OpenCV
- PyTorch
- Arduino IDE

## Project Structure

```
iot_facelock/
├── main.py                  # Main application script
├── recognize_faces.py       # Face recognition module
├── arduino_control.py       # Arduino communication module
├── data_pre.py             # Data preprocessing utilities
├── requirements.txt         # Python dependencies
├── arduino/
│   └── door_lock.ino       # Arduino servo control code
├── models/
│   ├── face_recognizer_model.xml  # Trained face recognition model
│   └── label_map.txt             # User name mappings
├── known_faces/            # Training images for face recognition
│   ├── Davka-Stavka/      # User 1's training images
│   └── Shaka/             # User 2's training images
├── logs/
│   └── recognition_log.txt # Access attempt logs
└── Silent-Face-Anti-Spoofing/  # Anti-spoofing module
```

## Installation

1. **Set up Python Environment**
   ```powershell
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # Install requirements
   pip install -r requirements.txt
   ```

2. **Arduino Setup**
   - Open `arduino/door_lock.ino` in Arduino IDE
   - Upload to your Arduino board
   - Note the COM port number assigned to Arduino

3. **Train Face Recognition Model**
   - Add photos of authorized users to `known_faces/[username]/`
   - Run the training script:
   ```powershell
   python train_faces.py
   ```

## Configuration

1. **Arduino Port**
   - The system auto-detects Arduino port
   - If needed, manually set in `arduino_control.py`:
   ```python
   ARDUINO_PORT = 'COM3'  # Change to your port
   ```

2. **Face Recognition**
   - Confidence threshold in `recognize_faces.py`
   - Default: `confidence < 70` (lower is better)

3. **Anti-Spoofing**
   - Model files in `Silent-Face-Anti-Spoofing/resources/`
   - Threshold adjustable in `main.py`

## Usage

1. Start the system:
   ```powershell
   python main.py
   ```

2. The system will:
   - Initialize webcam
   - Load face recognition model
   - Connect to Arduino
   - Start monitoring for faces

3. Controls:
   - Press 'q' to quit
   - Press 'd' for debug info

## Logging

- Access attempts are logged in `logs/recognition_log.txt`
- Includes timestamp, user name, and confidence score

## Troubleshooting

1. **Arduino Not Found**
   - Check USB connection
   - Verify correct COM port
   - Install Arduino drivers if needed

2. **Face Recognition Issues**
   - Ensure good lighting
   - Add more training images
   - Adjust confidence threshold

3. **Anti-Spoofing Too Strict**
   - Check lighting conditions
   - Ensure face is clearly visible
   - Adjust threshold if needed

## Security Notes

- The system uses both face recognition and liveness detection
- Keep model files and training data secure
- Regularly update authorized user images
- Monitor logs for unauthorized attempts
