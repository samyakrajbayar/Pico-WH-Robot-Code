# Omnidirectional Robot Car - Raspberry Pi Pico W

A Python program to control a 4-wheel omnidirectional robot car using a Raspberry Pi Pico W. This project enables full omnidirectional movement including forward/backward, strafing, rotation, and diagonal movements.

## Features

- ✨ **True Omnidirectional Movement** - Move in any direction without rotating
- 🎮 **Simple API** - Easy-to-use movement functions
- 🔧 **PWM Motor Control** - Smooth speed control for all motors
- 📐 **Mecanum Wheel Support** - Built-in kinematic calculations
- 🛡️ **Speed Normalization** - Automatic speed limiting to prevent motor damage
- 🎯 **Precise Control** - Combined X, Y, and rotation control

## Hardware Requirements

### Components
- 1x Raspberry Pi Pico W
- 4x DC motors (with mecanum or omni wheels)
- 1x Motor driver board (recommended: L298N, TB6612FNG, or DRV8833)
- 1x Battery pack (voltage depends on motors, typically 5-12V)
- Jumper wires
- Robot chassis with omnidirectional wheels

### Wiring Diagram

```
Pico W GPIO    →    Motor Driver    →    Motor
─────────────────────────────────────────────────
GPIO 0         →    IN1 (FL)        →    Front Left Motor (+)
GPIO 1         →    IN2 (FL)        →    Front Left Motor (-)
GPIO 2         →    IN3 (FR)        →    Front Right Motor (+)
GPIO 3         →    IN4 (FR)        →    Front Right Motor (-)
GPIO 4         →    IN5 (RL)        →    Rear Left Motor (+)
GPIO 5         →    IN6 (RL)        →    Rear Left Motor (-)
GPIO 6         →    IN7 (RR)        →    Rear Right Motor (+)
GPIO 7         →    IN8 (RR)        →    Rear Right Motor (-)

Pico W VBUS    →    Motor Driver VCC (if 5V logic)
Pico W GND     →    Motor Driver GND
Battery +      →    Motor Driver Motor Power (+)
Battery -      →    Motor Driver Motor Power (-)
```

**Note:** Adjust GPIO pin numbers in the code to match your wiring.

## Software Requirements

- MicroPython firmware installed on Raspberry Pi Pico W
- Thonny IDE or any MicroPython-compatible IDE
- USB cable for programming

## Installation

### 1. Install MicroPython on Pico W

1. Download the latest MicroPython firmware from [micropython.org](https://micropython.org/download/rp2-pico-w/)
2. Hold the BOOTSEL button while plugging in the Pico W
3. Drag and drop the `.uf2` file to the RPI-RP2 drive
4. The Pico W will reboot with MicroPython installed

### 2. Upload the Program

1. Open Thonny IDE
2. Connect to your Pico W (select the correct port)
3. Copy the `omni_robot.py` code to a new file
4. Save it to the Pico W as `main.py` (runs automatically on boot) or `omni_robot.py`

## Usage

### Basic Demo

Run the included demo to test all movement patterns:

```python
from omni_robot import demo
demo()
```

### Custom Control

```python
from omni_robot import OmniRobot

robot = OmniRobot()

# Basic movements
robot.forward(speed=60)
robot.backward(speed=60)
robot.strafe_left(speed=60)
robot.strafe_right(speed=60)
robot.rotate_cw(speed=50)
robot.rotate_ccw(speed=50)

# Diagonal movement
robot.diagonal_forward_right(speed=60)
robot.diagonal_forward_left(speed=60)

# Stop
robot.stop()
```

### Advanced Control

Use the `move()` method for precise control:

```python
# move(x, y, rotation)
# x: -100 (left) to 100 (right)
# y: -100 (backward) to 100 (forward)
# rotation: -100 (CCW) to 100 (CW)

robot.move(x=50, y=50, rotation=0)    # Move forward-right
robot.move(x=0, y=0, rotation=30)     # Rotate slowly clockwise
robot.move(x=-30, y=60, rotation=-20) # Complex movement
```

## API Reference

### OmniRobot Class

#### Methods

- **`__init__()`** - Initialize the robot with motor pins
- **`move(x, y, rotation)`** - Universal movement control
  - `x`: Sideways movement (-100 to 100)
  - `y`: Forward/backward movement (-100 to 100)
  - `rotation`: Rotation speed (-100 to 100)
- **`forward(speed=50)`** - Move forward
- **`backward(speed=50)`** - Move backward
- **`strafe_left(speed=50)`** - Strafe left
- **`strafe_right(speed=50)`** - Strafe right
- **`rotate_cw(speed=50)`** - Rotate clockwise
- **`rotate_ccw(speed=50)`** - Rotate counter-clockwise
- **`diagonal_forward_right(speed=50)`** - Move diagonally forward-right
- **`diagonal_forward_left(speed=50)`** - Move diagonally forward-left
- **`stop()`** - Stop all motors

## Configuration

### Adjusting GPIO Pins

Modify the GPIO pins in the `__init__` method:

```python
def __init__(self):
    self.fl_fwd = PWM(Pin(0))  # Change 0 to your GPIO number
    self.fl_rev = PWM(Pin(1))  # Change 1 to your GPIO number
    # ... etc
```

### Adjusting PWM Frequency

Change the motor PWM frequency (default 1000 Hz):

```python
for motor in self.motors:
    motor.freq(1000)  # Change to desired frequency
```

### Speed Limits

Adjust maximum speed by modifying speed values (0-100) in function calls.

## Troubleshooting

### Robot doesn't move
- Check all wiring connections
- Verify battery has sufficient voltage
- Ensure motor driver is powered correctly
- Test motors individually with simple code

### Robot moves in wrong direction
- Swap the forward/reverse pins for that motor in code
- Or physically swap the motor wire connections

### Uneven movement
- Check that all wheels are properly installed
- Calibrate motor speeds if needed
- Ensure battery is fully charged

### Motors too fast/slow
- Adjust speed parameters in function calls
- Check battery voltage matches motor specifications

## Safety Notes

⚠️ **Important Safety Guidelines:**
- Always test with low speed values first
- Use appropriate voltage for your motors
- Add a physical emergency stop switch
- Never run motors without proper load (wheels attached)
- Ensure proper ventilation for motor driver
- Double-check polarity before connecting power

## Future Enhancements

- [ ] Add WiFi control interface
- [ ] Implement remote control via web server
- [ ] Add sensor integration (ultrasonic, IR)
- [ ] Include PID control for precise movements
- [ ] Add autonomous navigation capabilities
- [ ] Create smartphone app control

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- Mecanum wheel kinematics calculations
- Raspberry Pi Pico W community
- MicroPython documentation

---

**Happy Building! 🤖**