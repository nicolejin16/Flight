import sys
import time
import threading
import subprocess
import cv2
import numpy as np
from picamera2 import Picamera2
import os
import signal
import serial

# Handle debug mode
n = len(sys.argv)
debugMode = 0
if n > 1 and sys.argv[1] == "Debug":
    debugMode = 1

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)


# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(1)


# Proportional gain constant (tune this)
Kp = 0.075

# Color thresholds
lower_black = np.array([0, 0, 0])
upper_black = np.array([90, 60, 60])

lower_orange = np.array([0, 40, 130])
upper_orange = np.array([60, 160, 255])

lower_blue = np.array([100, 0, 0])
upper_blue = np.array([255, 80, 80])
# Regions of interest
roiLeft = (20, 260, 200, 50)
roiRight = (440, 260, 200, 50)
roiOrange = (220, 240, 240, 50)
roiBlue = (220, 240, 240, 50)
# Start motors
arduino.write(b'@M1600')
arduino.write(b'@S1500')

orange = 0
orange_line_detected = False
last_orange_time = time.time()

blue = 0
blue_line_detected = False
last_blue_time = time.time()

cooldown_seconds = 1.5

while True:
    frame = picam2.capture_array()

    left_area = 0
    right_area = 0

    # Draw ROI rectangles
    cv2.rectangle(frame, (roiLeft[0], roiLeft[1]), (roiLeft[0]+roiLeft[2], roiLeft[1]+roiLeft[3]), (0, 255, 255), 2)
    cv2.rectangle(frame, (roiRight[0], roiRight[1]), (roiRight[0]+roiRight[2], roiRight[1]+roiRight[3]), (0, 255, 255), 2)

    # Process Left and Right ROIs
    for idx, (x, y, w, h) in zip(["Left", "Right"], [roiLeft, roiRight]):
        roi = frame[y:y+h, x:x+w]
        mask = cv2.inRange(roi, lower_black, upper_black)
        full_mask = cv2.inRange(frame, lower_black, upper_black)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        total_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                offset_cnt = cnt + [x, y]
                cv2.drawContours(frame, [offset_cnt], -1, (0, 255, 0), 2)
                total_area += area

        if idx == "Left":
            left_area = total_area
        else:
            right_area = total_area

    # === Proportional Control ===
    error = left_area - right_area
    correction = int(Kp * error)
    new_servo_pw = center_servo + correction
    new_servo_pw = max(min_servo, min(max_servo, new_servo_pw))  # Clamp

    if left_area + right_area > 0:
        #print(f"P-Control: error={error}, correction={correction}, servo={new_servo_pw}")
        arduino.write(b'@M1600')
        arduino.write(f'@S{new_servo_pw}'.encode())
    else:
        arduino.write(b'@M1500')

    # === Orange Line Detection ===
    cv2.rectangle(frame, (roiOrange[0], roiOrange[1]), (roiOrange[0]+roiOrange[2], roiOrange[1]+roiOrange[3]), (0, 255, 255), 2)
    roi2 = frame[roiOrange[1]:roiOrange[1]+roiOrange[3], roiOrange[0]:roiOrange[0]+roiOrange[2]]
    orange_mask = cv2.inRange(roi2, lower_orange, upper_orange)
    contours_orange, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    orange_pixels = cv2.countNonZero(orange_mask)

    if orange_pixels > 100:
        if not orange_line_detected and (time.time() - last_orange_time) > cooldown_seconds:
            orange += 1
            last_orange_time = time.time()
            print(f'{orange} orange lines detected.')
            orange_line_detected = True
    else:
        orange_line_detected = False  # reset when line leaves the ROI

        
    cv2.rectangle(frame, (roiBlue[0], roiBlue[1]), (roiBlue[0]+roiBlue[2], roiBlue[1]+roiBlue[3]), (0, 255, 255), 2)
    roi2 = frame[roiBlue[1]:roiBlue[1]+roiBlue[3], roiBlue[0]:roiBlue[0]+roiBlue[2]]
    blue_mask = cv2.inRange(roi2, lower_blue, upper_blue)
    contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_pixels = cv2.countNonZero(blue_mask)

    if blue_pixels > 80:
        if not blue_line_detected and (time.time() - last_blue_time) > cooldown_seconds:
            blue += 1
            last_blue_time = time.time()
            print(f'{blue} blue lines detected.')
            blue_line_detected = True
        else:
            blue_line_detected = False


    # === Debug Output ===
    if debugMode == 1:
        cv2.imshow("Contours", frame)
        cv2.imshow("Full Mask", full_mask)
        cv2.imshow("Orange Mask", orange_mask)
        cv2.imshow("Blue Mask", blue_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

# Cleanup
arduino.write(b'@M1500')
picam2.stop()

