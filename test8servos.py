from pylx16a.lx16a import *
import time, math

# -------------------- setup --------------------
PORT = "COM7"
LX16A.initialize(PORT, 0.1)

# Servo IDs (adjust if needed)
servo_ids = [1, 2, 3, 4, 5, 6, 7, 8]

servos = []
for sid in servo_ids:
    try:
        s = LX16A(sid)
        s.set_angle_limits(0, 240)
        s.enable_torque()
        servos.append((sid, s))  # store (id, servo)
        print(f"✅ Servo {sid} connected")
    except ServoTimeoutError:
        print(f"❌ Servo {sid} not responding")

if not servos:
    print("No servos detected, exiting.")
    quit()

# -------------------- individual test --------------------
print("\nTesting each servo individually...")
for sid, s in servos:
    center = 120
    low = center - 15
    high = center + 15
    print(f"→ Testing servo {sid}")
    s.move(low)
    time.sleep(0.5)
    s.move(high)
    time.sleep(0.5)
    s.move(center)
    time.sleep(0.5)

# -------------------- synchronized motion --------------------
print("\nAll servos moving together... (Ctrl+C to stop)")
t = 0
try:
    while True:
        angle = 120 + 15 * math.sin(t)
        for sid, s in servos:
            s.move(angle)
        t += 0.1
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nStopped.")
    for sid, s in servos:
        s.move(120)
    LX16A.close()
