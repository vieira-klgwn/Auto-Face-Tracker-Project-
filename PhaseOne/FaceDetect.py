#!/usr/bin/env python3
import cv2
import time

# ----------------- OpenCV Setup -----------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# ----------------- Parameters -----------------
STEP_THRESHOLD = 30       # px from center to trigger movement detection
MOVE_INTERVAL = 0.1       # seconds between motion calculations
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

    # Only consider the largest detected face
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda b: b[2]*b[3])
        cx = x + w // 2
        cy = y + h // 2

        # Draw bounding box and center dot
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        if prev_cx is not None:
            dx = cx - frame_center_x
            dy = cy - frame.shape[0] // 2

            # Detect left or right movement if face moves enough
            if abs(dx) > STEP_THRESHOLD:
                direction = "Left" if dx < 0 else "Right"
                distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                time_diff = max(0.001, time.time() - last_move_time)
                speed = distance / time_diff
                last_move_time = time.time()

        prev_cx, prev_cy = cx, cy

    # Draw reference center line
    cv2.line(frame, (frame_center_x, 0), (frame_center_x, frame.shape[0]), (255, 0, 0), 1)

    # Display info on frame
    cv2.putText(frame, f"Direction: {direction}  Speed: {speed:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Face Motion Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------- Cleanup -----------------
cap.release()
cv2.destroyAllWindows()
