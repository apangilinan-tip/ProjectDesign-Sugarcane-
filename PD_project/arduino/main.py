import time
from collections import deque

# Simulated functions for hardware interaction
def start_conveyor_motor():
    print("Conveyor motor started.")

def stop_conveyor_motor():
    print("Conveyor motor stopped.")

def rotate_sorter(value):
    print(f"Sorter rotated according to value: {value}")

def did_cane_pass_through_sorter():
    # Simulated check (could be replaced with actual sensor input)
    return True

# Initial state
conveyor_motor_running = False
queue = deque()  # Queue for sorter values

# Simulated signal to start conveyor motor (set to True for simulation)
signal_to_start_conveyor = True

while True:
    # Check if signal to start conveyor motor is received
    if signal_to_start_conveyor:
        if not conveyor_motor_running:
            start_conveyor_motor()
            conveyor_motor_running = True
    else:
        print("Standby")
        time.sleep(1)
        continue

    # Check if there are values in the queue
    if queue:
        # Get the first value from the queue and rotate sorter
        value = queue.popleft()
        rotate_sorter(value)
        
        # Check if the cane passed through the sorter
        while not did_cane_pass_through_sorter():
            print("Waiting for cane to pass through sorter...")
            time.sleep(1)  # Wait before checking again
        
    else:
        # No values in the queue, stop the conveyor motor and standby
        if conveyor_motor_running:
            stop_conveyor_motor()
            conveyor_motor_running = False
        print("Standby")
        time.sleep(1)