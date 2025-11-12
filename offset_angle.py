from pylx16a.lx16a import *
import time

# The servo ID you want to change
SERVO_ID = 7
# The new offset (30 is the max positive)
NEW_OFFSET =-30

print(f"Connecting to servo {SERVO_ID}...")
try:
    LX16A.initialize("COM7")
    servo = LX16A(SERVO_ID)
except ServoTimeoutError as e:
    print(f"Servo {e._id} is not responding. Exiting...")
    quit()

print("--- Setting Angle Offset ---")
try:
    # Read the current offset
    original_offset = servo.get_angle_offset()
    
    # Set the new offset
    # This value is added to all angle readings.
    servo.set_angle_offset(NEW_OFFSET)
    
    # Read it back to confirm
    confirmed_offset = servo.get_angle_offset()
    
    print(f"Servo ID {servo._id}: Offset changed from {original_offset} to {confirmed_offset}")

except Exception as e:
    print(f"Could not set offset for servo {servo._id}: {e}")

print(f"\nDone. Servo {SERVO_ID}'s offset is now {confirmed_offset}.")
print("You MUST re-run 'read_pose.py' to find your new angles.")