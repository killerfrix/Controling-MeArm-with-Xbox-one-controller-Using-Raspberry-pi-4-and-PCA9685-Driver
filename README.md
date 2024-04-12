> [!CAUTION]
> # With great power comes great responsibility
> READ EVERYTHING BEFORE RUNNING PYTHON FILE
> 
> By using the provided code or following the instructions, you acknowledge and accept full responsibility for any consequences, including but not limited to damage to equipment, injury, or any other issues that may arise.

# Materials
- MeArm
- 4 SG90 Servo motors of 180 degrees
- PCA9685 16-channel 12-Bit PWM Driver
- Raspberry Pi 4
- SD card (at least 8gb)
- Xbox one controller
- 2 dupont type cables (male to male)
- 6 dupont type cables (female to female)
- Ethernet cable

# Procedure
1. Build MeArm using the 4 servo motors
2. Connect Raspberry Pi 4 with PCA9685 Driver
   
   a.	Check Raspberry Pi 4 GPIO and the 40-pin header (https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
   
   b.	Locate left male ports of Driver ![image](https://github.com/killerfrix/Controling-MeArm-with-Xbox-one-controller-Using-Raspberry-pi-4-and-PCA9685-Driver/assets/97371595/b5a445b0-ea3d-49e2-8872-35cafa66cb00)
   
   c.	Connect 3V3 power to VCC using cables (female to female)
   
   d.	GND to GND
   
   e.	GPIO 2 (SDA) to SDA
   
   f.	GPIO 3 (SCL) to SCL
   
   g.	5V power to V+ (using female to female and the connecting male to male cables in blue part)
   
   h.	GND (any) to GND (using female to female and the connecting male to male cables in blue part)

3. Connect Servos with PCA9685 Driver

   a.	Base servo to 0 port in driver (brown cable and red cable are GND and V)

   b.	Right servo to 1 (the one that controls the height)
   
   c.	Left servo to 2 (The one that controls Middle part)

   d.	Claw servo to 3

4.	Environment configuration

      Disconnect any kind of input cables to raspberry pi (like mouse or keyboard), otherwise you will have to change the code
   	
   > [!IMPORTANT]
   > This section of the code selects the input, in this case by default when we connect xbox controller the event is 4, but it will change depending if there is an input
   > 
   > controllerInput = evdev.InputDevice("/dev/input/event4")
>ㅤ

ㅤㅤCreate virtual enviroment:

```
   python3 -m venv .venv
   source .venv/bin/activate
```

ㅤㅤrequired installs:

```
   pip install evdev
   pip install adafruit-circuitpython-servokit
```

ㅤㅤActivate IC2 option

```
   sudo raspi-config
```

ㅤㅤgo to Interface and then activate IC2

5. Connect your xbox controller to Raspberry Pi Bluetooth
```
   bluetoothctl
```
```
   power on
```
```
   scan on
```
```
   pair [Xbox Mac Adress]
```

# Initial positions

Base = 90

Claw = 90

Left Servo (the middle part) = 90

Right Servo (the one that adjust the height) = 180

This is what they should look like:

![image](https://github.com/killerfrix/Controling-MeArm-with-Xbox-one-controller-Using-Raspberry-pi-4-and-PCA9685-Driver-For-Dummies/assets/97371595/49b45391-ec87-40dc-81fe-18f47d81885e)
![image](https://github.com/killerfrix/Controling-MeArm-with-Xbox-one-controller-Using-Raspberry-pi-4-and-PCA9685-Driver-For-Dummies/assets/97371595/9fa490ef-87d7-4b17-acb4-503e4a70b1e6)

 > [!CAUTION]
 > Make sure that MeArm pieces are not connected to servo motors before running program
 > 
 > Otherwise MeArm might break or SERVO MOTORS COULD GET BURNED OUT

# Controls

- LB and RB for controlling the Base
- Directional Pad Horizontally controls middle part (left servo)
- Directional Pad Vertically controls height (right servo)
- X and B buttons controls Claw
- Change view button to start recording user's input (press again to stop recording)
- Menu button to start reproducing the recorded inputs

# Final View of everything

![image](https://github.com/killerfrix/Controling-MeArm-with-Xbox-one-controller-Using-Raspberry-pi-4-and-PCA9685-Driver-For-Dummies/assets/97371595/0ca71747-3050-4781-8e62-1cd3b99ed5cb)

# Logic behind PWM for controlling servo motors.

A servo motor is an electromechanical device. It has an electronic board that accepts PWM (Pulse Width Modulation) signals and measures its on-time pulse width. The servo motor also has a potentiometer that helps in keeping track of the shaft position.

In this case the Raspberry Pi among with the Adafruit PCA9685 Driver help us to control servos, a servo will move depending on the time in which the pulse is generated (duty cycle), for SG90 servos 0ms would mean 0 degrees, 0.5ms 90 degrees and 1 180 degrees.

**Duty cycle**

$` D = (angle / 180.0) `$

Internally when a servo is changed to 90 degrees, we make a pulse of 0 to 5 volts in a determined time, for 90 degrees a pulse every 0.5ms so that the servo will remain static in that point, and we will not be able to move it manually because electricity is being sent every time, ensuring that it remains in 90 degrees.

In the next code we can see that servo.fraction = duty_cycle is the one in charge of giving a pulse according to duty_cycle
```python
   # duty cycle for SG90 servo
   def angle_to_duty_cycle(angle):
       return (angle / 180.0)
   
   def control_servo_incremental(servo, current_angle, step):
       new_angle = current_angle + step
       new_angle = max(min(new_angle, 180), 0)  # Limit angle to range [0, 180]
       duty_cycle = angle_to_duty_cycle(new_angle)
       servo.fraction = duty_cycle  # Pulse every duty_cycle
       print("duty cycle:", duty_cycle)
       print("Angle set to:", new_angle)
       return new_angle
```



