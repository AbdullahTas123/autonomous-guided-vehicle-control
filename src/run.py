from pynput.keyboard import Key, Listener
from src.car.motor import Motor


#############(ena,in1,in2,enb,in3,in4)
motor = Motor(25,24,23,17,27,22)
#############


class ManualControl:
    def __init__(self) -> None:
        # Collect events until released
        listener = Listener(
                on_press=self.on_press,
                on_release=self.on_release)
        listener.start()
    
    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            if key.char == 'w':
                motor.move(0.4,0,0.1)
            elif key.char == 'a':
                motor.move(0.5,-0.3,0.1)
            elif key.char == 's':
                motor.move(-0.4,0,0.1)
            elif key.char == 'd':
                motor.move(0.5,0.3,0.1)
        except AttributeError:
            print('special key {0} pressed'.format(key))
            if key == Key.up:
                motor.move(0.5,0,0.1)
            elif key == Key.left:
                motor.move(0.5,0.3,0.1)
            elif key == Key.down:
                motor.move(-0.5,0,0.1)
            elif key == Key.right:
                motor.move(0.5,-0.3,0.1)
    
    def on_release(self, key):
        #print('{0} released'.format(key))
        if key == Key.esc:
            # Stop listener
            motor.stop(0.1)
            return False


class AutonomousControl:
    def __init__(self) -> None:
        pass
