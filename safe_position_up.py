from pylx16a.lx16a import *
import time

# --- 1. Define All Servos ---
try:
    LX16A.initialize("COM7")  # replace with your COM port
    
    # Create an object for all 8 servos
    servos = {
        # Hip Servos
        "FR_hip": LX16A(1),
        "FL_hip": LX16A(3),
        "BR_hip": LX16A(5),
        "BL_hip": LX16A(7),
        
        # Knee Servos
        "FR_knee": LX16A(2),
        "FL_knee": LX16A(4),
        "BR_knee": LX16A(6),
        "BL_knee": LX16A(8)
    }

except ServoTimeoutError as e:
    print(f"Servo {e.id} is not responding. Exiting...") # Also fixed here
    print("Please check power and wiring.")
    quit()


# --- 2. Define Your "Safe Home" Angles ---
# These are the exact values you just found.
home_angles = {
    # Hip Angles
    "FR_hip": 160,
    "FL_hip": 115,
    "BR_hip": 125,
    "BL_hip": 91,
    
    # Knee Angles
    "FR_knee": 110,
    "FL_knee": 115,
    "BR_knee": 115,
    "BL_knee": 115
}

# Time (in milliseconds) for the servos to move to their home position
move_time_ms = 3000  # 1 second


# --- 3. Move All Servos to Home Position ---
print("Moving all 8 servos to their 'home' position...")

for name, servo in servos.items():
    if name in home_angles:
        angle = home_angles[name]
        
        # --- THIS IS THE CORRECTED LINE ---
        print(f"  Moving {name} (ID {servo._id}) to {angle}°")
        # ----------------------------------
        
        # Send the move command to this servo
        servo.move(angle, move_time_ms)
    else:
        print(f"Warning: No home angle defined for {name}")

# Wait for the servos to finish moving
print(f"Waiting {move_time_ms / 1000.0} seconds for movement to complete...")
time.sleep(move_time_ms / 1000.0 + 0.5)  # Wait for move time + 0.5s buffer

print("\nRobot is now in home pose.")
print("Holding position for 1 seconds...")
time.sleep(1)

# --- 4. Relax Servos ---
print("Disabling torque (relaxing all servos)...")
for servo in servos.values():
    servo.disable_torque()

print("Done.")