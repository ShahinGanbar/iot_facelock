import serial
import time

class ArduinoController:
    def __init__(self, port='COM7', baudrate=9600):
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
        except Exception as e:
            print(f"Error initializing Arduino connection: {e}")
            self.arduino = None

    def unlock_door(self):
        if self.arduino:
            try:
                self.arduino.write(f"90\n".encode())  # 90 degrees to unlock
                time.sleep(1)  # Give servo time to move
                return True
            except Exception as e:
                print(f"Error sending unlock command: {e}")
                return False
        return False

    def lock_door(self):
        if self.arduino:
            try:
                self.arduino.write(f"0\n".encode())  # 0 degrees to lock
                time.sleep(1)  # Give servo time to move
                return True
            except Exception as e:
                print(f"Error sending lock command: {e}")
                return False
        return False

    def close(self):
        if self.arduino:
            self.arduino.close()