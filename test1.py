from pylx16a.lx16a import *
import time

LX16A.initialize("COM7", 0.1)

servo = LX16A(1)

# Move to 0°, then 90°, then 180°
for angle in [0, 90, 180]:
    print(f"Moving to {angle}°")
    servo.move(angle)
    time.sleep(1)
    