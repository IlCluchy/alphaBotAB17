import RPi.GPIO as GPIO
import time

class AlphaBot:
    def __init__(self, in1=12, in2=13, ena=6, in3=20, in4=21, enb=26, ir_l=19, ir_r=16):
        # Pin motori
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb

        # Pin sensori IR
        self.IR_L = ir_l
        self.IR_R = ir_r

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Motori
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        # Sensori IR
        GPIO.setup(self.IR_L, GPIO.IN)
        GPIO.setup(self.IR_R, GPIO.IN)

        # PWM motori
        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(30)
        self.PWMB.start(30)

        # Avvio in avanti
        self.forward()

    # ---------------------
    #   Movimento base 
    # ---------------------
    def forward(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def backward(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def right(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def leftOnSelf(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def rightOnSelf(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    # ---------------------
    #   Controllo PWM 
    # ---------------------

    def setPWMA(self, value):
        self.PWMA.ChangeDutyCycle(value)

    def setPWMB(self, value):
        self.PWMB.ChangeDutyCycle(value)

    # Imposta velocità dei motori (-100 a 100)
    def setMotor(self, left, right):
        # Motore destro
        if 0 <= right <= 100:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif -100 <= right < 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(-right)

        # Motore sinistro
        if 0 <= left <= 100:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif -100 <= left < 0:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(-left)

    # -------------------------
    #   Lettura sensori IR 
    # -------------------------

    def getLeftIrSensor(self):
        return GPIO.input(self.IR_L)

    def getRightIrSensor(self):
        return GPIO.input(self.IR_R)

    def getIrSensors(self):
        left = GPIO.input(self.IR_L)
        right = GPIO.input(self.IR_R)
        return left, right
