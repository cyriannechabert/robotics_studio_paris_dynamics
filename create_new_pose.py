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
    print(f"Servo {e._id} is not responding. Exiting...")
    print("Please check power and wiring.")
    quit()

# --- 2. Relax All Servos ---
print("Disabling torque on all servos...")
for name, servo in servos.items():
    try:
        servo.disable_torque()
    except Exception as e:
        print(f"Could not disable torque for {name}: {e}")

# --- 3. Wait for You to Pose the Robot ---
print("=====================================================")
print("✅ All servos are now relaxed.")
print("   Move the robot's legs by hand into the pose you want.")
print("\nPress ENTER when you are ready to read the angles.")
print("=====================================================")

# Wait for user to press Enter
input()

# --- 4. Read All Angles ---
print("\nReading current angles...")
captured_angles = {}

for name, servo in servos.items():
    try:
        # This is the command to read the angle
        current_angle = servo.get_physical_angle()
        
        # Round to 1 decimal place for cleaner output
        captured_angles[name] = round(current_angle, 1) 
        
        print(f"  {name} (ID {servo._id}): {captured_angles[name]}°")
    
    except Exception as e:
        print(f"  Could not read angle from {name} (ID {servo._id}): {e}")

# --- 5. Print the Final Pose ---
print("\n--- Paste This Into Your Code ---")
# This prints the dictionary in a format you can copy/paste
import json
print(json.dumps(captured_angles, indent=4))
print("---------------------------------")

print("Done.")