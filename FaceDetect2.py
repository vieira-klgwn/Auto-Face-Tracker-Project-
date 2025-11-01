#!/usr/bin/env python3
import cv2
import time
import serial

# ----------------- Arduino Setup -----------------
# Use your Kali Linux port
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # wait for Arduino to initialize

# ----------------- OpenCV Setup -----------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# ----------------- Parameters -----------------
STEP_THRESHOLD = 30       # px from center to trigger motor movement
MOVE_INTERVAL = 0.1       # seconds between motor commands
STEP_SIZE = 50            # steps per command (matches Arduino)
prev_cx = None
prev_cy = None
last_move_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    frame_center_x = frame.shape[1] // 2
    direction = ""
    speed = 0.0

    # Only consider the largest face
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda b: b[2]*b[3])
        cx = x + w // 2
        cy = y + h // 2

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        if prev_cx is not None:
            dx = cx - frame_center_x
            dy = cy - frame.shape[0]//2

            # Only move if face is far enough from center
            if abs(dx) > STEP_THRESHOLD:
                direction = "Left" if dx < 0 else "Right"
                distance = ((dx**2) + (dy**2))**0.5
                time_diff = max(0.001, time.time() - last_move_time)
                speed = distance / time_diff

                # Send command to Arduino with interval
                if (time.time() - last_move_time) > MOVE_INTERVAL:
                    if direction == "Left":
                        arduino.write(b'L')
                    else:
                        arduino.write(b'R')
                    last_move_time = time.time()

        prev_cx, prev_cy = cx, cy

    # Draw center line
    cv2.line(frame, (frame_center_x, 0), (frame_center_x, frame.shape[0]), (255, 0, 0), 1)

    # Display info
    cv2.putText(frame, f"Direction: {direction}  Speed: {speed:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Face Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
