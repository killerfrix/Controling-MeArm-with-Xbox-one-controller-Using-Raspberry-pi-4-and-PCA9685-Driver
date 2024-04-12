from time import sleep
import evdev 
from adafruit_servokit import ServoKit

# Initialize Adafruit ServoKit with PCA9685 and set PWM frequency
kit = ServoKit(channels=16, address=0x40, frequency=60)  # Set PWM frequency to 60 Hz

# Define duty cycle range corresponding to servo angles (for SG90 servo)
MIN_DUTY_CYCLE = 2.5  # 2.5%
MAX_DUTY_CYCLE = 12.5  # 12.5%

# duty cycle for SG90 servo
def angle_to_duty_cycle(angle):
    return (angle / 180.0) 

def control_servo_incremental(servo, current_angle, step):
    new_angle = current_angle + step
    new_angle = max(min(new_angle, 180), 0)  # Limit angle to range [0, 180]
    duty_cycle = angle_to_duty_cycle(new_angle)
    servo.fraction = duty_cycle  # period of time in which pulse is sent to servo
    print("duty cycle:", duty_cycle)
    print("Angle set to:", new_angle)
    return new_angle



def control_servo_with_dpad(servo, current_angle, dpad_value):
    if dpad_value == -1:  # Dpad left button pressed
        current_angle = control_servo_incremental(servo, current_angle, -ANGLE_STEP)
    elif dpad_value == 1:  # Dpad right button pressed
        current_angle = control_servo_incremental(servo, current_angle, ANGLE_STEP)
    return current_angle

# Initialize current angles
current_angle_22 = 90
current_angle_18 = 90
current_angle_40 = 90
current_angle_16 = 180

controllerInput = evdev.InputDevice("/dev/input/event4")

# angle step size
ANGLE_STEP = 10  # Adjust as needed

# event codes for buttons and D-pad
BTN_TL_BUTTON_CODE = evdev.ecodes.BTN_TL
BTN_TR_BUTTON_CODE = evdev.ecodes.BTN_TR
X_BUTTON_CODE = evdev.ecodes.BTN_X
B_BUTTON_CODE = evdev.ecodes.BTN_B
BTN_DPADX_BUTTON_CODE = evdev.ecodes.ABS_HAT0X
BTN_DPADY_BUTTON_CODE = evdev.ecodes.ABS_HAT0Y
SELECT_BUTTON_CODE = evdev.ecodes.BTN_SELECT
START_BUTTON_CODE = evdev.ecodes.BTN_START

# store recorded angles
recorded_angles = []
is_recording = False

# Initialize a counter to keep track of the order of recorded angles
recorded_angle_counter = 1

# Main loop to read controller events
for event in controllerInput.read_loop():
    if event.code == BTN_TL_BUTTON_CODE:  # BTL button pressed
        if event.value == 1:  # Button pressed and current angle is not 0
            print("BTL button pressed")
            current_angle_22 = control_servo_incremental(kit.servo[0], current_angle_22, ANGLE_STEP)
            if is_recording:
                if current_angle_22 != 0 and current_angle_22 != 180:  # Check if current angle is not 0 before appending
                    recorded_angles.append((recorded_angle_counter, "BTN_TL", current_angle_22))
                    recorded_angle_counter += 1
    elif event.code == BTN_TR_BUTTON_CODE:  # BRG button pressed
        if event.value == 1 :  # Button pressed and current angle is not 180
            print("BRG button pressed")
            current_angle_22 = control_servo_incremental(kit.servo[0], current_angle_22, -ANGLE_STEP)
            if is_recording:
                if current_angle_22 != 0 and current_angle_22 != 180:  # Check if current angle is not 180 before appending
                    recorded_angles.append((recorded_angle_counter, "BTN_TR", current_angle_22))
                    recorded_angle_counter += 1
    elif event.code == X_BUTTON_CODE:  # X button pressed
        if event.value == 1 :  # Button pressed and current angle is not 0
            print("X button pressed")
            current_angle_18 = control_servo_incremental(kit.servo[3], current_angle_18, -ANGLE_STEP)
            if is_recording:
                if current_angle_18 != 0 and current_angle_18 != 180:  # Check if current angle is not 0 before appending
                    recorded_angles.append((recorded_angle_counter, "X_BUTTON", current_angle_18))
                    recorded_angle_counter += 1
    elif event.code == B_BUTTON_CODE:  # B button pressed
        if event.value == 1 :  # Button pressed and current angle is not 180
            print("B button pressed")
            current_angle_18 = control_servo_incremental(kit.servo[3], current_angle_18, ANGLE_STEP)
            if is_recording:
                if current_angle_18 != 0 and current_angle_18 != 180:  # Check if current angle is not 180 before appending
                    recorded_angles.append((recorded_angle_counter, "B_BUTTON", current_angle_18))
                    recorded_angle_counter += 1
    elif event.code == BTN_DPADX_BUTTON_CODE and event.value != 0:  
        if current_angle_40 != 0 :  # Current angle is not 0 or 180
            current_angle_40 = control_servo_with_dpad(kit.servo[2], current_angle_40, event.value)
            if is_recording:
                if current_angle_40 != 0 and current_angle_40 != 180:  # Check if current angle is not 0 or 180 before appending
                    recorded_angles.append((recorded_angle_counter, "BTN_DPADX", current_angle_40, event.value))
                    recorded_angle_counter += 1
    elif event.code == BTN_DPADY_BUTTON_CODE and event.value != 0:  
        if current_angle_16 != 0 :  # Current angle is not 0 or 180
            current_angle_16 = control_servo_with_dpad(kit.servo[1], current_angle_16, event.value)
            if is_recording:
                if current_angle_16 != 0 and current_angle_16 != 180:  # Check if current angle is not 0 or 180 before appending
                    recorded_angles.append((recorded_angle_counter, "BTN_DPADY", current_angle_16, event.value))
                    recorded_angle_counter += 1




    elif event.code == SELECT_BUTTON_CODE and is_recording == True:
        if event.value == 1:  # Button pressed
            print(" recorded angles: ", recorded_angles)
            # Replay recorded angles backward
            for input_id, *args in reversed(recorded_angles):
                button_code, angle = args[0], args[1]
                angle = int(angle)
                if button_code == "BTN_TL" or button_code == "BTN_TR":
                    kit.servo[0].angle = angle
                elif button_code == "X_BUTTON" or button_code == "B_BUTTON":
                    kit.servo[3].angle = angle
                elif button_code == "BTN_DPADY":
                    kit.servo[1].angle = angle
                elif button_code == "BTN_DPADX":
                    kit.servo[2].angle = angle
                sleep(0.2)
            is_recording = False

    elif event.code == SELECT_BUTTON_CODE: 
        if event.value == 1:  # Button pressed
            print("Recording started")
            recorded_angles = []  # Clear any previously recorded angles
            recorded_angle_counter = 1
            is_recording = True
    
    elif event.code == START_BUTTON_CODE and event.value == 1:  # Replay action
        print("Replaying recorded angles:")
        
        # Sort recorded angles based on sequence
        recorded_angles.sort(key=lambda x: x[0])
        
        # Replay recorded angles forward
        for input_id, *args in recorded_angles:
            button_code, angle = args[0], args[1]
            angle = int(angle)
            if button_code == "BTN_TL" or button_code == "BTN_TR":
                kit.servo[0].angle = angle
            elif button_code == "X_BUTTON" or button_code == "B_BUTTON":
                kit.servo[3].angle = angle
            elif button_code == "BTN_DPADY":
                kit.servo[1].angle = angle
            elif button_code == "BTN_DPADX":
                kit.servo[2].angle = angle
            sleep(0.2)
        
        # Replay recorded angles backward
        for input_id, *args in reversed(recorded_angles):
            button_code, angle = args[0], args[1]
            angle = int(angle)
            if button_code == "BTN_TL" or button_code == "BTN_TR":
                kit.servo[0].angle = angle
            elif button_code == "X_BUTTON" or button_code == "B_BUTTON":
                kit.servo[3].angle = angle
            elif button_code == "BTN_DPADY":
                kit.servo[1].angle = angle
            elif button_code == "BTN_DPADX":
                kit.servo[2].angle = angle
            sleep(0.2)
