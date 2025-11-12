from pylx16a.lx16a import *

print("Initializing...")
LX16A.initialize("COM7", 0.1)
print("Initialized.")

for servo_id in range(1, 9):  # 1 to 8 inclusive
    try:
        servo = LX16A(servo_id)
        print(f"✅ Servo found with ID: {servo_id}")
    except ServoTimeoutError:
        print(f"❌ No servo found with ID: {servo_id}")


