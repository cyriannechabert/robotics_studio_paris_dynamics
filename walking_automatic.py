from pylx16a.lx16a import *
import time
import msvcrt  # Used for non-blocking key presses on Windows
import sys

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


# --- 2. Define Your Poses ---

# Your "Ready to Walk" (Neutral) Pose
pose_neutral = {
    "FR_hip": 193.2, "FL_hip": 149.8, "BR_hip": 86.6, "BL_hip": 56.2,
    "FR_knee": 44.9, "FL_knee": 49.0, "BR_knee": 182.6, "BL_knee": 180.0
}

# Pose B: (Your "step_2")
pose_B = {
    "FR_hip": 200.4, "FL_hip": 123.8, "BR_hip": 102.5, "BL_hip": 46.8,
    "FR_knee": 62.4, "FL_knee": 55.0, "BR_knee": 180.0, "BL_knee": 156.5
}

# Pose C (Your new pose)
pose_C = {
    "FR_hip": 166.6, "FL_hip": 157.4, "BR_hip": 88.6, "BL_hip": 78.0,
    "FR_knee": 49.2, "FL_knee": 66.7, "BR_knee": 153.8, "BL_knee": 174.5
}

# This is the list of poses to cycle through
# We start with a step, not neutral
walk_cycle = [pose_B, pose_neutral, pose_C, pose_neutral]
walk_cycle_names = ["Step B", "Neutral", "Step C", "Neutral"]


# How long each step takes (in milliseconds)
step_time_ms = 400  # 1 second per step (as you had it)


# --- 3. Helper Function to Move ---
def move_to_pose(target_pose, move_time_ms):
    """Moves all 8 servos to their target angles safely."""
    for name, servo in servos.items():
        if name in target_pose:
            angle = target_pose[name]
            
            # Safety check to prevent errors!
            if not (0 <= angle <= 240):
                print(f"  WARNING: Clamping {name} angle from {angle}° to 0-240 range.")
                angle = max(0, min(240, angle)) # Clamps the value
                
            servo.move(angle, move_time_ms)
    
    # Wait for move to finish before starting the next one
    time.sleep(move_time_ms / 1000.0 + 0.05) # Small buffer


# --- 4. Main Interactive Loop ---
def main_loop():
    print("Moving to neutral 'Ready to Walk' pose...")
    move_to_pose(pose_neutral, 1500)
    
    current_step_index = 0
    is_walking = True       # Start walking immediately
    is_in_neutral = False   # Flag to ensure we return to neutral
    
    print("\n--- Controls ---")
    print("  Robot is WALKING.")
    print("  's' = STOP walking")
    print("  'q' = QUIT")
    print("----------------")

    try:
        while True:
            # --- 1. Check for a key press ---
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
            
                # --- 2. Handle Input ---
                if key == 'q':
                    print("Quitting...")
                    break # Exit the main while loop
                    
                elif key == 's':
                    if is_walking:
                        print("Stopping walk...")
                        is_walking = False
            
            # --- 3. Handle Robot State ---
            if is_walking:
                # Get the pose to move to
                pose = walk_cycle[current_step_index]
                pose_name = walk_cycle_names[current_step_index]
                
                print(f"Taking step {current_step_index + 1}/4: {pose_name}")
                move_to_pose(pose, step_time_ms)
                
                # Update the index for the *next* loop
                current_step_index = (current_step_index + 1) % len(walk_cycle)
                
            elif not is_in_neutral:
                # This runs ONCE after 's' is pressed
                print("Returning to neutral...")
                move_to_pose(pose_neutral, 1000)
                current_step_index = 0  # Reset the walk cycle
                is_in_neutral = True
                print("Robot stopped. Press 'q' to quit.")
            
            # Sleep briefly so the loop doesn't use 100% CPU
            if not is_walking:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nCaught Ctrl+C. Stopping.")
    
    finally:
        # --- 5. Cleanup ---
        print("Returning to neutral and disabling torque.")
        move_to_pose(pose_neutral, 1000)
        
        for servo in servos.values():
            servo.disable_torque()
        print("Done.")

# Run the main loop
main_loop()