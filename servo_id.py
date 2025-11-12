from pylx16a.lx16a import *

# Initialize with your COM port
LX16A.initialize("COM7", 0.1)

for servo_id in range(1, 255):
    try:
        s = LX16A(servo_id)
        print(f"Servo found with ID: {servo_id}")
        
        # Change its ID to 2
        s.set_id(8)
        print(f"Servo ID {servo_id} changed to 2")
        
        s = LX16A(servo_id)
        print(f"Servo found with ID: {servo_id}")
        break  # stop after finding and renaming one
    except:
        pass
