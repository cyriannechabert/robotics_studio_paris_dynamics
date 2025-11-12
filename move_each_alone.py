from pylx16a.lx16a import *
import time
import json

LX16A.initialize("COM7")  # replace with your COM port

# --- Only define the one servo you want to test ---
name = "BL_hip"
servo = LX16A(7)

# Start with a neutral guess
current_angle = 120  # Start at 120 degrees
step = 5  # increment for adjustment (in degrees)

print(f"Testing servo {name} (ID 7) by itself.")
print("Use '+' or '-' to adjust, 'q' to quit (this will not save).")

while True:
    print(f"{name}: current_angle = {current_angle}")
    
    # This will now send a valid angle (like 120, 125, etc.)
    servo.move(current_angle, 500)

    cmd = input("Command (+/-/q): ").strip()
    if cmd == '+':
        current_angle += step
    elif cmd == '-':
        current_angle -= step
    elif cmd == 'q':
        print(f"Quitting test. Last position was {current_angle}")
        break
    else:
        print("Invalid input. Use '+', '-', or 'q'.")

    # Safety check to prevent out-of-bounds commands
    if not (0 <= current_angle <= 240):
        print(f"Error: Angle {current_angle} is out of 0-240 range. Stopping.")
        current_angle = max(0, min(240, current_angle)) # Clamp value
        print(f"Setting to nearest valid angle: {current_angle}")


# Relax the servo when done
servo.disable_torque()
print("Test done. Servo relaxed.")