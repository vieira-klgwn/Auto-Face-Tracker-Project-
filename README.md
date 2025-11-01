🧠 Face Tracker with OpenCV, Python & Arduino
📘 Overview

This project demonstrates how to build a face-tracking camera system using Python (OpenCV) and Arduino.
The camera (or stepper motor simulating camera movement) automatically follows a person’s face — rotating left or right depending on the direction of movement detected by OpenCV.

The setup uses:

OpenCV for real-time face detection.

Python for communication logic and decision-making.

Arduino (with a stepper motor) to physically move in the direction of the detected face.

💡 Even without a specific motorized camera, this setup shows how facial movement can control hardware direction through serial communication.

🧩 Features

✅ Real-time face detection using OpenCV.
✅ Face tracking using a stepper motor (via Arduino).
✅ Serial communication between Python and Arduino.
✅ Adjustable thresholds for movement sensitivity and speed.
✅ Works on Kali Linux and other Linux distributions.

⚙️ Requirements
Hardware

Arduino (e.g., Arduino Uno)

Stepper motor (28BYJ-48 or similar)

ULN2003 stepper motor driver

USB cable (to connect Arduino to PC)

Software

Python 3

OpenCV (cv2)

pySerial (serial)

Arduino IDE






🧰 Installation
1. Install Python dependencies

sudo apt update
sudo apt install python3-opencv python3-pip
pip install pyserial



2. Connect Arduino

Connect the Arduino to your computer and note its serial port:
arduino = serial.Serial('/dev/ttyACM0', 9600)

🔌 How It Works

OpenCV captures video frames from your camera.

It detects faces using the Haar Cascade model.

The program checks the position of the detected face relative to the frame’s center.

If the face moves left or right beyond a threshold, Python sends either an 'L' or 'R' command to the Arduino via serial.

The Arduino moves the stepper motor in the corresponding direction.

🧠 Possible Improvements

Add vertical tracking (up/down movement).

Implement PID control for smoother tracking.

Use Pan-Tilt servo mechanisms for better accuracy.

Integrate with ESP32 for wireless tracking.

🎥 Demo (Optional)

<img width="634" height="474" alt="image" src="https://github.com/user-attachments/assets/43cbf4b0-7fb3-46ae-8563-931811ba4b51" />


👨‍💻 Author

Ntwali Isimbi Vieira
📍 Kigali, Rwanda
🧠 Passionate about AI, Robotics, and Embedded Systems
