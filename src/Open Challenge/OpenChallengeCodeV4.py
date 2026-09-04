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

corner_start_time = 0
MIN_CORNER_TIME = 2

# IMU heading tracking
last_heading_time = time.time()
HEADING_INTERVAL = 1.0 # request heading from Arduino every 1 second
imu_heading = 0.0

# Handle debug mode
n = len(sys.argv)
debugMode = 1
if n > 1 and sys.argv[1] == "Debug":
    debugMode = 1

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1, write_timeout = 0.05)
time.sleep(2)


# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (700, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure("preview")
picam2.start()
#time.sleep(1)

center_servo = 90
min_servo = 60
max_servo = 120

# Proportional gain constant 
Kp = 0.009
Kd = 0

counter = 0

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 100])

lower_orange = np.array([88, 56, 107])
upper_orange = np.array([116, 224, 255])

lower_blue = np.array([0, 97, 88])
upper_blue = np.array([19, 255, 255])
# Regions of interest
roiLeft = (20, 220, 200, 80)
roiRight = (500, 220, 200, 80)
roiOrange = (220, 300, 240, 50)
roiBlue = (220, 300, 240, 50)
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

cooldown_seconds = 3

while True:
    now = time.monotonic()
    
    frame = picam2.capture_array()

        # Periodically request IMU heading from Arduino
    if time.time() - last_heading_time >= HEADING_INTERVAL:
        send(b'@H\n')
        last_heading_time = time.time()
        time.sleep(0.02) # brief wait so response arrives before we read
    # Read and process all incoming serial data
    if arduino.in_waiting > 0:
        try:
            raw = arduino.read(arduino.in_waiting).decode('utf-8', errors='ignore')
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    imu_heading = float(line)
                    #print(f'[IMU Heading] {imu_heading:.2f}°')
                except ValueError:
                    pass # ignore any non-numeric lines
        except Exception:
            pass # silently ignore malformed or partial data
    
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
        hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower_black, upper_black)
        #full_mask = cv2.inRange(frame, lower_black, upper_black)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        total_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 50:
                offset_cnt = cnt + [x, y]
                cv2.drawContours(frame, [offset_cnt], -1, (0, 255, 0), 2)
                total_area += area

        if idx == "Left":
            left_area = total_area
        else:
            right_area = total_area

    # === STATE MACHINE DRIVING ===

    left_trigger = left_area < 100
    right_trigger = right_area < 100

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
            corner_start_time = now
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
        elapsed = now - (corner_start_time if corner_start_time is not None else now)
        
        if trigger_count_right and trigger_count_left >= 5:
            send(b'@S90\n')
        
        if trigger_count_right >= 5:
            # turn RIGHT
            #arduino.write(b'@M1550\n')
            send(b'@S70\n')
            turning_angle = 70
            cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255)) 
            #print("turn right")
            if left_area and right_area <= 50:
                send(b'@S90\n')
        
        if trigger_count_left >= 5:
            # turn LEFT
            #arduino.write('@M1550\n')
            send(b'@S110\n')
            turning_angle = 110
            cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255)) 
            #print("turn left")
            if left_area and right_area <= 50:
                send(b'@S90\n')
                
        if left_area and right_area <= 50:
                send(b'@S110\n')
            
        
        
        # --- EXIT CONDITIONS ---
        recovered = False
        time_ok = elapsed >= MIN_CORNER_TIME

        if trigger_count_left >= 5 and time_ok:
            recovered = left_area > 1000
            
        if trigger_count_right >= 5 and time_ok:
            recovered = right_area > 1000
            
        if left_area and right_area <= 50:
                send(b'@S90\n')

        if recovered:
            state = State.WALL_FOLLOW
            prev_error = 0
            trigger_side = None
            trigger_count_right = 0
            trigger_count_left = 0
            #print("WALL_FOLLOW")
            send(b'@M1630\n')

        
        # === Orange Line Detection ===
    cv2.rectangle(frame, (roiOrange[0], roiOrange[1]), (roiOrange[0]+roiOrange[2], roiOrange[1]+roiOrange[3]), (0, 255, 255), 2)
    roi2 = frame[roiOrange[1]:roiOrange[1]+roiOrange[3], roiOrange[0]:roiOrange[0]+roiOrange[2]]
    roi_orange = frame[roiOrange[1]:roiOrange[1]+roiOrange[3], roiOrange[0]:roiOrange[0]+roiOrange[2]]
    hsv_orange = cv2.cvtColor(roi_orange, cv2.COLOR_RGB2HSV)
    orange_mask = cv2.inRange(hsv_orange, lower_orange, upper_orange)
    orange_pixels = cv2.countNonZero(orange_mask)

    if orange_pixels > 500:
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
    roi_blue = frame[roiBlue[1]:roiBlue[1]+roiBlue[3], roiBlue[0]:roiBlue[0]+roiBlue[2]]
    hsv_blue = cv2.cvtColor(roi_blue, cv2.COLOR_RGB2HSV)
    blue_mask = cv2.inRange(hsv_blue, lower_blue, upper_blue)
    blue_pixels = cv2.countNonZero(blue_mask)

    if blue_pixels > 400:
       if not blue_line_detected and (time.time() - last_blue_time) > cooldown_seconds:
            blue += 1
            last_blue_time = time.time()
            print(f'{blue} blue lines detected.')
            blue_line_detected = True
    else:
        blue_line_detected = False
    if blue >= 12:
        counter += 1
        if counter >= 275:
            send(b"M1500")
            break
        
        
    
    # === Debug Output ===
    cv2.imshow("Contours", frame)
    #cv2.imshow("orange", orange_mask)
    #cv2.imshow("blue", blue_mask)
    cv2.putText(frame, f"{turning_angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 20, (0, 255, 255)) 
        
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    
    time.sleep(0.03)
# Cleanup
send(b'@M1500\n')
picam2.stop()