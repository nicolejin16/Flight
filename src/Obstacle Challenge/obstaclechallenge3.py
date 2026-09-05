import sys
import time
import cv2
import numpy as np
import serial
from gpiozero import DigitalOutputDevice
import struct

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
picam2.preview_configuration.main.size = (700, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure("preview")
picam2.start()

# LIDAR

PORT = "/dev/ttyAMA0"
BAUD = 230400
PACKET_HEADER = 0x54
PACKET_LEN = 47
'''
# GPIO setup
LIDAR_POWER_PIN = 15  # BCM numbering
lidar_power = DigitalOutputDevice(LIDAR_POWER_PIN)

def find_packet_start(buffer):
    for i in range(len(buffer) - 1):
        if buffer[i] == 0x54 and (buffer[i+1] & 0xFF) == 0x2C:
            return i
    return -1

def parse_packet(packet):
    if len(packet) != PACKET_LEN:
        return None
    speed = struct.unpack_from('<H', packet, 2)[0] / 64.0
    start_angle = struct.unpack_from('<H', packet, 4)[0] / 100.0
    measurements = []
    for i in range(12):
        offset = 6 + i * 3
        dist = struct.unpack_from('<H', packet, offset)[0]
        confidence = packet[offset + 2]
        measurements.append((dist, confidence))
    end_angle = struct.unpack_from('<H', packet, 42)[0] / 100.0
    timestamp = struct.unpack_from('<H', packet, 44)[0]
    crc = packet[46]
    return {
        "speed": speed,
        "start_angle": start_angle,
        "end_angle": end_angle,
        "timestamp": timestamp,
        "crc": crc,
        "points": measurements
    }
'''
# STEERING

CENTER_SERVO = 90
MIN_SERVO = 70
MAX_SERVO = 140

KP = 0.009
KD = 0

prev_error = 0

# WALL FOLLOWING

WALL_THRESHOLD = 100
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

cooldown_seconds = 5

finish_counter = 0

# OBSTACLE VARIABLES

current_pillar_color = None

OBSTACLE_TRIGGER_AREA = 900

pillar_lost_counter = 0

# COLOR THRESHOLDS

    # walls

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 100])

    # lap lines

lower_orange = np.array([88, 56, 107])
upper_orange = np.array([116, 224, 255])

lower_blue = np.array([0, 97, 88])
upper_blue = np.array([19, 255, 255])

    # HSV pillars

LOWER_RED = np.array([116, 162, 79])
UPPER_RED = np.array([131, 241, 234])

LOWER_GREEN = np.array([27, 116, 64])
UPPER_GREEN = np.array([74, 255, 141])

# ROIS

roiLeft = (20, 200, 150, 80)
roiRight = (550, 200, 150, 80)

roiOrange = (180, 280, 280, 70)
roiBlue = (180, 280, 280, 70)

#roiPillar = (0, 0, 640, 300)
'''
# START LiDAR SCAN

def interpolate_angles(start, end, count):
    angle_range = (end - start + 360) % 360
    step = angle_range / (count - 1)
    return [(start + i * step) % 360 for i in range(count)]

def main():
    try:
        # Power on the LD19
        lidar_power.on()
        print("LD19 powered ON via GPIO 15.")
        time.sleep(1.5)

        ser = serial.Serial(PORT, BAUD, timeout=0.1)
        buffer = bytearray()
        print("Listening for LD19 data...")

        while True:
            data = ser.read(256)
            if data:
                buffer += data
                while True:
                    idx = find_packet_start(buffer)
                    if idx == -1 or len(buffer) - idx < PACKET_LEN:
                        break
                    packet = buffer[idx:idx+PACKET_LEN]
                    buffer = buffer[idx+PACKET_LEN:]
                    parsed = parse_packet(packet)
                    if parsed:
                        angles = interpolate_angles(parsed["start_angle"], parsed["end_angle"], 12)
                        #print(f"\nSpeed: {parsed['speed']:.2f} RPM | Timestamp: {parsed['timestamp']} ms")
                        for i, ((dist, conf), angle) in enumerate(zip(parsed["points"], angles)):
                            #if abs(angle - 0.0) < 5:  # angles near 0° 
                            print(f"  Pt {i+1:02d}: {angle:.2f}°  {dist} mm  (conf: {conf})")
                    else:
                        print("Invalid packet")
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        lidar_power.off()
        print("LD19 powered OFF.")

if __name__ == "__main__":
    main()
'''
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
        if area < 900:
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
        hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower_black, upper_black)
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
            if pillar_center <= 150 and y > 250:
                state = State.WALL_FOLLOW
                avoid_heading_target = None
                current_pillar_color = None
        if current_pillar_color == "GREEN":
            #target_center = 530
            if pillar_center >= 530 and y > 250:
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
            send(b'@S110\n')
            recovered = left_area > 1000
        else:
            send(b'@S70\n')
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
                target_center = 130
                '''if pillar_center <= 150:
                    state = State.WALL_FOLLOW
                    avoid_heading_target = None
                    current_pillar_color = None'''
            if current_pillar_color == "GREEN":
                target_center = 550
                '''if pillar_center >= 530:
                    state = State.WALL_FOLLOW
                    avoid_heading_target = None
                    current_pillar_color = None'''
            steering = int(CENTER_SERVO - 0.3 * (pillar_center - target_center))
            steering = clamp(steering, MIN_SERVO, MAX_SERVO)
            send(f'@S{steering}\n'.encode())
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            #print(steering, pillar_center)
        if pillar_lost_counter > 8:
            state = State.WALL_FOLLOW
            avoid_heading_target = None
            current_pillar_color = None
            
    # ========================================================
    # LAP COUNTING
    # ========================================================

    roi_orange = frame[roiOrange[1]:roiOrange[1]+roiOrange[3], roiOrange[0]:roiOrange[0]+roiOrange[2]]
    hsv_orange = cv2.cvtColor(roi_orange, cv2.COLOR_RGB2HSV)
    orange_mask = cv2.inRange(hsv_orange, lower_orange, upper_orange)
    orange_pixels = cv2.countNonZero(orange_mask)
    #print(orange_pixels)
    if orange_pixels > 500:
        if (not orange_line_detected and time.time() - last_orange_time > cooldown_seconds):
            orange_count += 1
            last_orange_time = time.time()
            orange_line_detected = True
            print("Orange:", orange_count)
    else:
        orange_line_detected = False
    roi_blue = frame[roiBlue[1]:roiBlue[1]+roiBlue[3], roiBlue[0]:roiBlue[0]+roiBlue[2]]
    hsv_blue = cv2.cvtColor(roi_blue, cv2.COLOR_RGB2HSV)
    blue_mask = cv2.inRange(hsv_blue, lower_blue, upper_blue)
    blue_pixels = cv2.countNonZero(blue_mask)
    #print(blue_pixels)
    if blue_pixels > 500:
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

    if orange_count >= 12 or blue_count >= 12:
        finish_counter += 1
        if finish_counter > 150:
            send(b'@M1500\n')
            break

    # ========================================================
    # DEBUG
    # ========================================================

    cv2.rectangle(frame, (roiLeft[0], roiLeft[1]), (roiLeft[0]+roiLeft[2], roiLeft[1]+roiLeft[3]), (0, 255, 255), 2)
    cv2.rectangle(frame, (roiRight[0], roiRight[1]), (roiRight[0]+roiRight[2], roiRight[1]+roiRight[3]), (0, 255, 255), 2)
    cv2.rectangle(frame, (roiOrange[0], roiOrange[1]), (roiOrange[0]+roiOrange[2], roiOrange[1]+roiOrange[3]), (0, 255, 255), 2)
    #qqqqcv2.rectangle(frame, (roiPillar[0], roiPillar[1]), (roiPillar[0]+roiPillar[2], roiPillar[1]+roiPillar[3]), (0, 255, 255), 2)
    cv2.putText(frame, f"{state.name}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow( "frame", frame)
    #cv2.imshow("orange mask", orange_mask)
    #cv2.imshow("blue mask", blue_mask)
    #cv2.imshow("red mask", red_mask)
    #cv2.imshow("greenmask", green_mask)
    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(0.03)

# ============================================================
# CLEANUP
# ============================================================

send(b'@M1500\n')
picam2.stop()
cv2.destroyAllWindows()