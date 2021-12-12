import RPİ.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor:
    def __init__(self,enA,in1,in2,enB,in3,in4):
        self.enA = enA
        self.in1 = in1
        self.in2 = in2
        self.enB = enB
        self.in3 = in3
        self.in4 = in4
        GPIO.setup(self.enA,GPIO.OUT)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.enB,GPIO.OUT)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.enA,1000)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.enB,1000)  
        self.pwmB.start(0)
        
    def move(self, speed=0.5, turn=0, t=0):
        # for positive and negative values of speed variable
        if turn == 0 and abs(speed) > 0.8:
            speed = 0.8 * (speed / abs(speed))
        
        if (abs(speed) + abs(turn)) > 0.8:
            if (speed > 0 and turn > 0 ) or (speed < 0 and turn < 0 ):
                rightSpeed = 80.0
                leftSpeed = rightSpeed * ((speed - turn) * 100) / ((speed + turn) * 100)
            if (speed > 0 and turn < 0 ) or (speed < 0 and turn > 0 ):
                leftSpeed = 80.0
                rightSpeed = leftSpeed * ((speed + turn) * 100) / ((speed - turn) * 100)
        else:
            leftSpeed = (speed - turn) * 100
            rightSpeed = (speed + turn) * 100
        
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        
        if leftSpeed > 0:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)
            
        if rightSpeed > 0:
            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
        else:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
            
        sleep(t)
        """       
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        sleep(t)
        """
    """
    def moveBackward(self,speed=50,t=0):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
        sleep(t)
    """  
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)
      
        
    
        
        