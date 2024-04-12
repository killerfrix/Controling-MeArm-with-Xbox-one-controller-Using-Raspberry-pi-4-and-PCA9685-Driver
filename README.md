> [!CAUTION]
> # With great power comes great responsibility
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
    
    a. Disconnect any kind of input cables to raspberry pi (like mouse or keyboard), otherwise you will have to change the code
   	
   > [!IMPORTANT]
   > This section of the code selects the input, in this case by default when we connect xbox controller the event is 4, but it will change depending if there is an input
   > 
   > controllerInput = evdev.InputDevice("/dev/input/event4")
>
ㅤ
ㅤc. create virtual enviroment
```
python3 -m venv .venv
source .venv/bin/activate
```
ㅤd. required installs

      pip install evdev
      pip install adafruit-circuitpython-servokit
