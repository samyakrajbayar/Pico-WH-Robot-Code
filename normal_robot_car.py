from machine import Pin, PWM
import time

class DifferentialRobot:
    def __init__(self):
        # Motor pins - adjust GPIO numbers based on your wiring
        # Left Motor
        self.left_fwd = PWM(Pin(0))
        self.left_rev = PWM(Pin(1))
        
        # Right Motor
        self.right_fwd = PWM(Pin(2))
        self.right_rev = PWM(Pin(3))
        
        # Set PWM frequency (1kHz is typical for DC motors)
        self.motors = [
            self.left_fwd, self.left_rev,
            self.right_fwd, self.right_rev
        ]
        
        for motor in self.motors:
            motor.freq(1000)
        
        self.max_speed = 65535  # 16-bit PWM resolution
        self.stop()
    
    def set_motor(self, fwd_pin, rev_pin, speed):
        """Set individual motor speed (-100 to 100)"""
        speed = max(-100, min(100, speed))  # Clamp speed
        duty = int(abs(speed) * self.max_speed / 100)
        
        if speed > 0:
            fwd_pin.duty_u16(duty)
            rev_pin.duty_u16(0)
        elif speed < 0:
            fwd_pin.duty_u16(0)
            rev_pin.duty_u16(duty)
        else:
            fwd_pin.duty_u16(0)
            rev_pin.duty_u16(0)
    
    def move(self, left_speed, right_speed):
        """
        Move robot with differential drive control
        left_speed: left motor speed (-100 to 100)
        right_speed: right motor speed (-100 to 100)
        """
        self.set_motor(self.left_fwd, self.left_rev, left_speed)
        self.set_motor(self.right_fwd, self.right_rev, right_speed)
    
    def forward(self, speed=50):
        """Move forward"""
        self.move(speed, speed)
    
    def backward(self, speed=50):
        """Move backward"""
        self.move(-speed, -speed)
    
    def turn_left(self, speed=50):
        """Turn left (forward)"""
        self.move(0, speed)
    
    def turn_right(self, speed=50):
        """Turn right (forward)"""
        self.move(speed, 0)
    
    def spin_left(self, speed=50):
        """Spin left in place (counter-clockwise)"""
        self.move(-speed, speed)
    
    def spin_right(self, speed=50):
        """Spin right in place (clockwise)"""
        self.move(speed, -speed)
    
    def arc_left(self, speed=50, turn_ratio=0.5):
        """
        Arc left while moving forward
        turn_ratio: 0 (sharp turn) to 1 (gentle turn)
        """
        right_speed = speed
        left_speed = int(speed * turn_ratio)
        self.move(left_speed, right_speed)
    
    def arc_right(self, speed=50, turn_ratio=0.5):
        """
        Arc right while moving forward
        turn_ratio: 0 (sharp turn) to 1 (gentle turn)
        """
        left_speed = speed
        right_speed = int(speed * turn_ratio)
        self.move(left_speed, right_speed)
    
    def stop(self):
        """Stop all motors"""
        for motor in self.motors:
            motor.duty_u16(0)

class FourWheelRobot(DifferentialRobot):
    """
    Extended class for 4-wheel robot (2 motors controlling 4 wheels)
    Left motor controls both left wheels, right motor controls both right wheels
    Inherits all methods from DifferentialRobot
    """
    def __init__(self):
        super().__init__()
        print("4-Wheel Robot initialized (differential drive)")

# Demo program
def demo():
    # Use DifferentialRobot for 2-wheel robot
    # Use FourWheelRobot for 4-wheel robot with 2 motors
    robot = DifferentialRobot()
    
    print("Differential Drive Robot Demo")
    print("Testing movement patterns...")
    
    try:
        # Forward
        print("Moving forward...")
        robot.forward(60)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        # Backward
        print("Moving backward...")
        robot.backward(60)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        # Turn left
        print("Turning left...")
        robot.turn_left(60)
        time.sleep(1.5)
        robot.stop()
        time.sleep(1)
        
        # Turn right
        print("Turning right...")
        robot.turn_right(60)
        time.sleep(1.5)
        robot.stop()
        time.sleep(1)
        
        # Spin left
        print("Spinning left...")
        robot.spin_left(50)
        time.sleep(1.5)
        robot.stop()
        time.sleep(1)
        
        # Spin right
        print("Spinning right...")
        robot.spin_right(50)
        time.sleep(1.5)
        robot.stop()
        time.sleep(1)
        
        # Arc movements
        print("Arc left...")
        robot.arc_left(60, turn_ratio=0.3)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        print("Arc right...")
        robot.arc_right(60, turn_ratio=0.3)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        print("Demo complete!")
        
    except KeyboardInterrupt:
        print("\nStopping robot...")
        robot.stop()

# Advanced demo with patterns
def pattern_demo():
    robot = DifferentialRobot()
    
    print("Pattern Demo: Square")
    try:
        for i in range(4):
            # Move forward
            robot.forward(60)
            time.sleep(1)
            
            # Stop briefly
            robot.stop()
            time.sleep(0.3)
            
            # Turn 90 degrees (adjust time as needed)
            robot.spin_right(50)
            time.sleep(0.65)  # Adjust this value for exact 90° turn
            
            robot.stop()
            time.sleep(0.3)
        
        print("Square pattern complete!")
        
    except KeyboardInterrupt:
        print("\nStopping robot...")
        robot.stop()

# Remote control simulation
def remote_control():
    """
    Example of how you might implement remote control
    This is a simulation - replace with actual input method
    """
    robot = DifferentialRobot()
    
    commands = {
        'w': ('forward', 60),
        's': ('backward', 60),
        'a': ('spin_left', 50),
        'd': ('spin_right', 50),
        'q': ('arc_left', 60),
        'e': ('arc_right', 60),
        'x': ('stop', 0)
    }
    
    print("Remote Control Mode")
    print("Commands: w=forward, s=backward, a=spin left, d=spin right")
    print("          q=arc left, e=arc right, x=stop")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # In real implementation, get input from WiFi, Bluetooth, or serial
            cmd = input("Enter command: ").lower()
            
            if cmd in commands:
                action, speed = commands[cmd]
                if action == 'stop':
                    robot.stop()
                else:
                    getattr(robot, action)(speed)
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        print("\nExiting remote control...")
        robot.stop()

# Run the demo
if __name__ == "__main__":
    demo()
    # Uncomment to run pattern demo:
    # pattern_demo()
    # Uncomment to run remote control:
    # remote_control()
