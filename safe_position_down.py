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


# --- 2. Define Your "Safe Down" Angles ---
# These are your new, valid angles
down_angles = {
    "FR_hip": 70.6,
    "FL_hip": 28.3,
    "BR_hip": 36.2,
    "BL_hip": 6.5, 
    "FR_knee": 201.8,
    "FL_knee": 200.9,
    "BR_knee": 199.4,
    "BL_knee": 199.0
}

# Time (in milliseconds) for the servos to move
move_time_ms = 3000  # 1 second


# --- 3. Move All Servos to Home Position ---
print("Moving all 8 servos to their 'safe_position_down'...")

for name, servo in servos.items():
    if name in down_angles:
        angle = down_angles[name]
        
        # General safety check, just in case
        if not (0 <= angle <= 240):
            print(f"  WARNING: Clamping {name} angle from {angle}° to 0-240 range.")
            angle = max(0, min(240, angle)) # Clamps the value
        
        print(f"  Moving {name} (ID {servo._id}) to {angle}°")
        servo.move(angle, move_time_ms)
    else:
        print(f"Warning: No home angle defined for {name}")

# Wait for the servos to finish moving
print(f"Waiting {move_time_ms / 1000.0} seconds for movement to complete...")
time.sleep(move_time_ms / 1000.0 + 0.5)

print("\nRobot is now in down pose.")
print("Holding position for 2 seconds...")
time.sleep(2)

# --- 4. Relax Servos ---
print("Disabling torque (relaxing all servos)...")
for servo in servos.values():
    servo.disable_torque()

print("Done.")