from machine import Pin, PWM
import time

class OmniRobot:
    def __init__(self):
        # Motor pins - adjust GPIO numbers based on your wiring
        # Front Left Motor
        self.fl_fwd = PWM(Pin(0))
        self.fl_rev = PWM(Pin(1))
        
        # Front Right Motor
        self.fr_fwd = PWM(Pin(2))
        self.fr_rev = PWM(Pin(3))
        
        # Rear Left Motor
        self.rl_fwd = PWM(Pin(4))
        self.rl_rev = PWM(Pin(5))
        
        # Rear Right Motor
        self.rr_fwd = PWM(Pin(6))
        self.rr_rev = PWM(Pin(7))
        
        # Set PWM frequency (1kHz is typical for DC motors)
        self.motors = [
            self.fl_fwd, self.fl_rev,
            self.fr_fwd, self.fr_rev,
            self.rl_fwd, self.rl_rev,
            self.rr_fwd, self.rr_rev
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
    
    def move(self, x, y, rotation):
        """
        Move robot with omnidirectional control
        x: sideways movement (-100 to 100, left to right)
        y: forward/backward movement (-100 to 100, backward to forward)
        rotation: rotation (-100 to 100, CCW to CW)
        """
        # Mecanum wheel kinematic equations
        fl_speed = y + x + rotation
        fr_speed = y - x - rotation
        rl_speed = y - x + rotation
        rr_speed = y + x - rotation
        
        # Normalize speeds to stay within -100 to 100
        speeds = [fl_speed, fr_speed, rl_speed, rr_speed]
        max_val = max(abs(s) for s in speeds)
        if max_val > 100:
            scale = 100.0 / max_val
            fl_speed *= scale
            fr_speed *= scale
            rl_speed *= scale
            rr_speed *= scale
        
        # Set motor speeds
        self.set_motor(self.fl_fwd, self.fl_rev, fl_speed)
        self.set_motor(self.fr_fwd, self.fr_rev, fr_speed)
        self.set_motor(self.rl_fwd, self.rl_rev, rl_speed)
        self.set_motor(self.rr_fwd, self.rr_rev, rr_speed)
    
    def forward(self, speed=50):
        """Move forward"""
        self.move(0, speed, 0)
    
    def backward(self, speed=50):
        """Move backward"""
        self.move(0, -speed, 0)
    
    def strafe_left(self, speed=50):
        """Move left (sideways)"""
        self.move(-speed, 0, 0)
    
    def strafe_right(self, speed=50):
        """Move right (sideways)"""
        self.move(speed, 0, 0)
    
    def rotate_cw(self, speed=50):
        """Rotate clockwise"""
        self.move(0, 0, speed)
    
    def rotate_ccw(self, speed=50):
        """Rotate counter-clockwise"""
        self.move(0, 0, -speed)
    
    def diagonal_forward_right(self, speed=50):
        """Move diagonally forward-right"""
        self.move(speed, speed, 0)
    
    def diagonal_forward_left(self, speed=50):
        """Move diagonally forward-left"""
        self.move(-speed, speed, 0)
    
    def stop(self):
        """Stop all motors"""
        for motor in self.motors:
            motor.duty_u16(0)

# Demo program
def demo():
    robot = OmniRobot()
    
    print("Omnidirectional Robot Demo")
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
        
        # Strafe left
        print("Strafing left...")
        robot.strafe_left(60)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        # Strafe right
        print("Strafing right...")
        robot.strafe_right(60)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        # Rotate clockwise
        print("Rotating clockwise...")
        robot.rotate_cw(50)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        # Rotate counter-clockwise
        print("Rotating counter-clockwise...")
        robot.rotate_ccw(50)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        # Diagonal movement
        print("Moving diagonally...")
        robot.diagonal_forward_right(60)
        time.sleep(2)
        robot.stop()
        time.sleep(1)
        
        print("Demo complete!")
        
    except KeyboardInterrupt:
        print("\nStopping robot...")
        robot.stop()

# Run the demo
if __name__ == "__main__":
    demo()
