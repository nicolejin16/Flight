import serial

ser = serial.Serial("/dev/ttyAMA0", 230400, timeout=1)

def crc8(data):
    crc = 0
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = ((crc << 1) ^ 0x4D) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
    return crc

while True:
    # Find packet header
    if ser.read(1) != b'\x54':
        continue

    if ser.read(1) != b'\
