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
from enum import Enum

def send(cmd):
    try:
        arduino.write(cmd)
        #print(cmd)
    except serial.SerialTimeoutException:
        arduino.reset_output_buffer()
        try:
            arduino.write(cmd)
        except serial.SerialTimeoutException:
            print("not working")
            
        

class State(Enum):
    WALL_FOLLOW = 1
    CORNER_TURN = 2

state = State.WALL_FOLLOW

prev_error = 0

# Debounce
trigger_count_left = 0
trigger_count_right = 0
TRIGGER_FRAMES = 5

# Trigger memory
#trigger_side = None  # "left", "right"

# Timing

#corner_start_time = 0
#MIN_CORNER_TIME = 5

# Handle debug mode
n = len(sys.argv)
debugMode = 1
if n > 1 and sys.argv[1] == "Debug":
    debugMode = 1

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1, write_timeout = 0.05)
time.sleep(2)


# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure("preview")
picam2.start()
#time.sleep(1)

center_servo = 90
min_servo = 60
max_servo = 140

# Proportional gain constant (tune this)
Kp = 0.0075
Kd = 0

counter = 0

# Color thresholds
lower_black = np.array([0, 0, 0])
upper_black = np.array([100, 100, 100])

lower_orange = np.array([0, 40, 130])
upper_orange = np.array([60, 160, 255])

lower_blue = np.array([100, 0, 0])
upper_blue = np.array([255, 80, 80])
# Regions of interest
roiLeft = (20, 205, 200, 100)
roiRight = (420, 205, 200, 100)
roiOrange = (220, 240, 240, 50)
roiBlue = (220, 240, 240, 50)
# Start motor
send(b'@M1630\n')
send(b'@S90\n')

orange = 0
orange_line_detected = False
last_orange_time = time.time()
blue = 0
blue_line_detected = False
last_blue_time = time.time()

turning_angle = 0

cooldown_seconds = 2.5

while True:
    frame = picam2.capture_array()
    
    if arduino.in_waiting > 0:
        arduino.read(arduino.in_waiting)
    
    left_area = 0
    right_area = 0
    
    # Draw ROI rectangles
    cv2.rectangle(frame, (roiLeft[0], roiLeft[1]), (roiLeft[0]+roiLeft[2], roiLeft[1]+roiLeft[3]), (0, 255, 255), 2)
    cv2.rectangle(frame, (roiRight[0], roiRight[1]), (roiRight[0]+roiRight[2], roiRight[1]+roiRight[3]), (0, 255, 255), 2)
    full_mask = cv2.inRange(frame, lower_black, upper_black)
    # Process Left and Right ROIs
    for idx, (x, y, w, h) in zip(["Left", "Right"], [roiLeft, roiRight]):
        roi = frame[y:y+h, x:x+w]
        mask = cv2.inRange(roi, lower_black, upper_black)
        #full_mask = cv2.inRange(frame, lower_black, upper_black)

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

    # === STATE MACHINE DRIVING ===

    left_trigger = left_area < 550
    right_trigger = right_area < 550

    # ==========================
    # STATE: WALL_FOLLOW
    # ==========================
    if state == State.WALL_FOLLOW:
        # Debounce logic
        if left_trigger:
            trigger_count_left += 1
            trigger_count_right = 0
        elif right_trigger:
            trigger_count_right += 1
            trigger_count_left = 0
        else:
            trigger_count_left = 0
            trigger_count_right = 0

        # Enter CORNER_TURN_:
        if trigger_count_left >= TRIGGER_FRAMES or trigger_count_right >= TRIGGER_FRAMES:
            state = State.CORNER_TURN
            #corner_start_time = time.time()
            send(b'@M1630\n')
        else:
            # Normal wall following (Pd-control)
            error = left_area - right_area
            correction = int(Kp * error + Kd * (error - prev_error))
            new_servo_pw = center_servo - correction
            new_servo_pw = max(min_servo, min(max_servo, new_servo_pw))  # Clamp
            prev_error = error
            turning_angle = new_servo_pw
            cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255)) 
            try:
                send(f'@S{new_servo_pw}\n'.encode())
                #print(new_servo_pw)
            except serial.SerialTimeoutException:
                pass


    # =========================
    # STATE: CORNER_TURN
    # =========================
    elif state == State.CORNER_TURN:
        #elapsed = time.time() - corner_start_time
        
        # --- TURNING BEHAVIOR (you can tune this) ---
        if trigger_count_left >= 5:
            # turn LEFT
            #arduino.write('@M1550\n')
            send(b'@S140\n')
            turning_angle = 145
            cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255)) 
            #print("turn left")

        elif trigger_count_right >= 5:
            # turn RIGHT
            #arduino.write(b'@M1550\n')
            send(b'@S60\n')
            turning_angle = 60
            cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255)) 
            #print("turn right")
        
        # --- EXIT CONDITIONS ---
        recovered = False

        if trigger_count_left >= 5:
            recovered = left_area > 1000
            
        if trigger_count_right >= 5:
            recovered = right_area > 1000

        if recovered:
            state = State.WALL_FOLLOW
            prev_error = 0
            trigger_side = None
            trigger_count_right = 0
            trigger_count_left = 0
            #print("Exiting CORNER_TURN → WALL_FOLLOW")
            send(b'@M1630\n')

        
        # === Orange Line Detection ===
    cv2.rectangle(frame, (roiOrange[0], roiOrange[1]), (roiOrange[0]+roiOrange[2], roiOrange[1]+roiOrange[3]), (0, 255, 255), 2)
    roi2 = frame[roiOrange[1]:roiOrange[1]+roiOrange[3], roiOrange[0]:roiOrange[0]+roiOrange[2]]
    orange_mask = cv2.inRange(roi2, lower_orange, upper_orange)
    #contours_orange, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    orange_pixels = cv2.countNonZero(orange_mask)

    if orange_pixels > 100:
        if not orange_line_detected and (time.time() - last_orange_time) > cooldown_seconds:
            orange += 1
            last_orange_time = time.time()
            print(f'{orange} orange lines detected.')
            orange_line_detected = True
    else:
        orange_line_detected = False  # reset when line leaves the ROI
    if orange >= 12:
        counter += 1
        print(counter)
        if counter >= 250:
            send(b"M1500")
            break

        
    cv2.rectangle(frame, (roiBlue[0], roiBlue[1]), (roiBlue[0]+roiBlue[2], roiBlue[1]+roiBlue[3]), (0, 255, 255), 2)
    roi2 = frame[roiBlue[1]:roiBlue[1]+roiBlue[3], roiBlue[0]:roiBlue[0]+roiBlue[2]]
    blue_mask = cv2.inRange(roi2, lower_blue, upper_blue)
    #contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_pixels = cv2.countNonZero(blue_mask)

    if blue_pixels > 80:
       if not blue_line_detected and (time.time() - last_blue_time) > cooldown_seconds:
            blue += 1
            last_blue_time = time.time()
            print(f'{blue} blue lines detected.')
            blue_line_detected = True
    else:
        blue_line_detected = False
    if blue >= 12:
        counter += 1
        if counter >= 250:
            send(b"M1500")
            break
        
        
    
    # === Debug Output ===
    cv2.imshow("Contours", frame)
    cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 20, (0, 255, 255)) 
        
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    time.sleep(0.03)
# Cleanup
send(b'@M1500\n')
picam2.stop()

