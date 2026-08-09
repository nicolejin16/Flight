import sys
import time
import cv2
import numpy as np
import serial

from enum import Enum
from picamera2 import Picamera2

# ============================================================
# SERIAL COMMUNICATION
# ============================================================

def send(cmd):
    try:
        arduino.write(cmd)
    except serial.SerialTimeoutException:
        arduino.reset_output_buffer()
        try:
            arduino.write(cmd)
        except serial.SerialTimeoutException:
            print("Arduino timeout")

# STATES

class State(Enum):
    WALL_FOLLOW = 1
    CORNER_TURN = 2
    OBSTACLE_AVOID = 3

state = State.WALL_FOLLOW

# ARDUINO

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1, write_timeout=0.05)
time.sleep(2)

# CAMERA

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure("preview")
picam2.start()

# STEERING

CENTER_SERVO = 90
MIN_SERVO = 70
MAX_SERVO = 140

KP = 0.003
KD = 0

prev_error = 0

# WALL FOLLOWING

WALL_THRESHOLD = 550
TRIGGER_FRAMES = 5
trigger_count_left = 0
trigger_count_right = 0

# LAP COUNTING

orange_count = 0
blue_count = 0

orange_line_detected = False
blue_line_detected = False

last_orange_time = time.time()
last_blue_time = time.time()

cooldown_seconds = 1.5

finish_counter = 0

# OBSTACLE VARIABLES

current_pillar_color = None

OBSTACLE_TRIGGER_AREA = 2500

pillar_lost_counter = 0

# COLOR THRESHOLDS

# walls

lower_black = np.array([0, 0, 0])
upper_black = np.array([140, 130, 140])

# lap lines

lower_orange = np.array([0, 40, 130])
upper_orange = np.array([60, 160, 255])

lower_blue = np.array([100, 0, 0])
upper_blue = np.array([255, 80, 80])

# HSV pillars

LOWER_RED = np.array([116, 162, 79])
UPPER_RED = np.array([131, 241, 234])

LOWER_GREEN = np.array([30, 145, 0])
UPPER_GREEN = np.array([74, 255, 255])

# ROIS

roiLeft = (0, 250, 200, 80)
roiRight = (440, 250, 200, 80)

roiOrange = (220, 240, 240, 50)
roiBlue = (220, 240, 240, 50)

#roiPillar = (0, 0, 640, 300)

# START MOTOR

send(b'@M1630\n')
send(b'@S90\n')

# FUNCTIONS

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def find_pillar(mask):

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best_box = None
    largest_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 300:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        if area > largest_area:
            largest_area = area
            best_box = (x, y, w, h)
    return best_box, largest_area

# MAIN LOOP

while True:

    frame = picam2.capture_array()

    # ========================================================
    # WALL DETECTION
    # ========================================================

    left_area = 0
    right_area = 0

    for name, (x, y, w, h) in zip(["Left", "Right"], [roiLeft, roiRight]):
        roi = frame[y:y+h, x:x+w]
        mask = cv2.inRange(roi, lower_black, upper_black)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 600:
                total_area += area
        if name == "Left":
            left_area = total_area
        else:
            right_area = total_area

    # ========================================================
    # PILLAR DETECTION
    # ========================================================

    #px, py, pw, ph = roiPillar
    #pillar_roi = frame[py:py+ph, px:px+pw]
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    red_mask = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
    green_mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
    red_box, red_area = find_pillar(red_mask)
    green_box, green_area = find_pillar(green_mask)

    pillar_box = None
    pillar_area = 0
    pillar_color = None

    if red_area > green_area and red_box is not None:

        pillar_box = red_box
        pillar_area = red_area
        pillar_color = "RED"

    elif green_box is not None:

        pillar_box = green_box
        pillar_area = green_area
        pillar_color = "GREEN"
        
    #if pillar_box is not None:
        #x, y, w, h = pillar_box
        #pillar_box = (x + px, y + py, w, h)

    # ========================================================
    # OBSTACLE PRIORITY
    # ========================================================

    if (state != State.OBSTACLE_AVOID and pillar_box is not None and pillar_area > OBSTACLE_TRIGGER_AREA):
        state = State.OBSTACLE_AVOID
        current_pillar_color = pillar_color
        pillar_lost_counter = 0

    # ========================================================
    # WALL FOLLOW
    # ========================================================
    if state == State.OBSTACLE_AVOID and pillar_box is not None:
        x, y, w, h = pillar_box
        pillar_center = x + w // 2
        frame_center = frame.shape[1] // 2
        offset = pillar_center - frame_center
        if current_pillar_color == "RED":
            #target_center = 150
            if pillar_center <= 150:
                state = State.WALL_FOLLOW
                avoid_heading_target = None
                current_pillar_color = None
        if current_pillar_color == "GREEN":
            #target_center = 530
            if pillar_center >= 530:
                state = State.WALL_FOLLOW
                avoid_heading_target = None
                current_pillar_color = None
    if state == State.WALL_FOLLOW:
        left_trigger = left_area < WALL_THRESHOLD
        right_trigger = right_area < WALL_THRESHOLD
        if left_trigger:
            trigger_count_left += 1
            trigger_count_right = 0
        elif right_trigger:
            trigger_count_right += 1
            trigger_count_left = 0
        else:
            trigger_count_left = 0
            trigger_count_right = 0
        if (trigger_count_left >= TRIGGER_FRAMES or trigger_count_right >= TRIGGER_FRAMES):
            state = State.CORNER_TURN
        else:

            error = left_area - right_area
            correction = KP * error + KD * (error - prev_error)
            servo = int(CENTER_SERVO - correction)
            servo = clamp(servo, MIN_SERVO, MAX_SERVO)
            prev_error = error
            send(f'@S{servo}\n'.encode())

    # ========================================================
    # CORNER TURN
    # ========================================================

    elif state == State.CORNER_TURN:
        if trigger_count_left >= TRIGGER_FRAMES:
            send(b'@S140\n')
            recovered = left_area > 1000
        else:
            send(b'@S60\n')
            recovered = right_area > 1000
        if recovered:
            state = State.WALL_FOLLOW
            trigger_count_left = 0
            trigger_count_right = 0
            prev_error = 0

    # ========================================================
    # OBSTACLE AVOID
    # ========================================================

    elif state == State.OBSTACLE_AVOID:
        if pillar_box is None:
            pillar_lost_counter += 1
        else:
            pillar_lost_counter = 0
            x, y, w, h = pillar_box
            pillar_center = x + w // 2
            frame_center = frame.shape[1] // 2
            offset = pillar_center - frame_center
            if current_pillar_color == "RED":
                target_center = 150
                '''if pillar_center <= 150:
                    state = State.WALL_FOLLOW
                    avoid_heading_target = None
                    current_pillar_color = None'''
            if current_pillar_color == "GREEN":
                target_center = 580
                '''if pillar_center >= 530:
                    state = State.WALL_FOLLOW
                    avoid_heading_target = None
                    current_pillar_color = None'''
            steering = int(CENTER_SERVO - 0.5 * (pillar_center - target_center))
            steering = clamp(steering, MIN_SERVO, MAX_SERVO)
            send(f'@S{steering}\n'.encode())
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            print(steering, pillar_center)
        if pillar_lost_counter > 8:
            state = State.WALL_FOLLOW
            avoid_heading_target = None
            current_pillar_color = None
            
    # ========================================================
    # LAP COUNTING
    # ========================================================

    roi_orange = frame[roiOrange[1]:roiOrange[1]+roiOrange[3], roiOrange[0]:roiOrange[0]+roiOrange[2]]
    orange_mask = cv2.inRange(roi_orange, lower_orange, upper_orange)
    orange_pixels = cv2.countNonZero(orange_mask)
    if orange_pixels > 100:
        if (not orange_line_detected and time.time() - last_orange_time > cooldown_seconds):
            orange_count += 1
            last_orange_time = time.time()
            orange_line_detected = True
            print("Orange:", orange_count)
    else:
        orange_line_detected = False
    roi_blue = frame[roiBlue[1]:roiBlue[1]+roiBlue[3], roiBlue[0]:roiBlue[0]+roiBlue[2]]
    blue_mask = cv2.inRange(roi_blue, lower_blue, upper_blue)
    blue_pixels = cv2.countNonZero(blue_mask)
    if blue_pixels > 80:
        if (not blue_line_detected and time.time() - last_blue_time > cooldown_seconds):
            blue_count += 1
            last_blue_time = time.time()
            blue_line_detected = True
            print("Blue:", blue_count)
    else:
        blue_line_detected = False

    # ========================================================
    # FINISH
    # ========================================================

    if orange_count >= 13 or blue_count >= 13:
        finish_counter += 1
        if finish_counter > 200:
            send(b'@M1500\n')
            break

    # ========================================================
    # DEBUG
    # ========================================================

    cv2.rectangle(frame, (roiLeft[0], roiLeft[1]), (roiLeft[0]+roiLeft[2], roiLeft[1]+roiLeft[3]), (0, 255, 255), 2)
    cv2.rectangle(frame, (roiRight[0], roiRight[1]), (roiRight[0]+roiRight[2], roiRight[1]+roiRight[3]), (0, 255, 255), 2)
    #qqqqcv2.rectangle(frame, (roiPillar[0], roiPillar[1]), (roiPillar[0]+roiPillar[2], roiPillar[1]+roiPillar[3]), (0, 255, 255), 2)
    cv2.putText(frame, f"{state.name}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow( "frame", frame)
    #cv2.imshow("red mask", red_mask)
    cv2.imshow("greenmask", green_mask)
    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(0.03)

# ============================================================
# CLEANUP
# ============================================================

send(b'@M1500\n')
picam2.stop()
cv2.destroyAllWindows()
