from pylx16a.lx16a import *
import time

# --- 1. Define All Servos ---
try:
    LX16A.initialize("COM7")  # replace with your COM port
    
    # Create an object for all 8 servos
    servos = {
        "FR_hip": LX16A(1), "FL_hip": LX16A(3), "BR_hip": LX16A(5), "BL_hip": LX16A(7),
        "FR_knee": LX16A(2), "FL_knee": LX16A(4), "BR_knee": LX16A(6), "BL_knee": LX16A(8)
    }

except ServoTimeoutError as e:
    print(f"Servo {e._id} is not responding. Exiting...")
    print("Please check power and wiring.")
    quit()


# --- 2. Define Your "Ready to Walk" Angles ---
# These are the values you just captured
walk_angles1 = {
    "FR_hip": 193.2,
    "FL_hip": 149.8,
    "BR_hip": 86.6,
    "BL_hip": 56.2,
    "FR_knee": 44.9,
    "FL_knee": 49.0,
    "BR_knee": 182.6,
    "BL_knee": 180.0
}

walk_angles = {
    "FR_hip": 200.4, "FL_hip": 123.8, "BR_hip": 102.5, "BL_hip": 46.8,
    "FR_knee": 62.4, "FL_knee": 55.0, "BR_knee": 180.0, "BL_knee": 156.5
}

# Time (in milliseconds) for the servos to move
move_time_ms = 1500  # 1.5 seconds


# --- 3. Move All Servos to Walk Position ---
print("Moving all 8 servos to their 'Ready to Walk' position...")

for name, servo in servos.items():
    if name in walk_angles:
        angle = walk_angles[name]
        
        # General safety check, just in case
        if not (0 <= angle <= 240):
            print(f"  WARNING: Clamping {name} angle from {angle}° to 0-240 range.")
            angle = max(0, min(240, angle)) # Clamps the value
        
        print(f"  Moving {name} (ID {servo._id}) to {angle}°")
        servo.move(angle, move_time_ms)
    else:
        print(f"Warning: No walk angle defined for {name}")

# Wait for the servos to finish moving
wait_time_s = move_time_ms / 1000.0
print(f"Moving... waiting {wait_time_s + 0.5} seconds...")
time.sleep(wait_time_s + 0.5)

print("\nRobot is now in 'Ready to Walk' pose.")
print("Holding for 1 seconds...")
time.sleep(1)

# --- 4. Relax Servos ---
print("Disabling torque (relaxing all servos)...")
for servo in servos.values():
    servo.disable_torque()

print("Done.")