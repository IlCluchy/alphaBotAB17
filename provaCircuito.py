from libreries.AlphaBot import AlphaBot
import RPi.GPIO as GPIO
import time
import threading

# Pin sensori IR
IR_L = 19  # Sensore sinistro
IR_R = 16  # Sensore destro

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IR_L, GPIO.IN)
GPIO.setup(IR_R, GPIO.IN)

def main():

    robot = AlphaBot()
    robot.setPWMA(30)
    robot.setPWMB(30)
    robot.stop()

    robot.forward()
    time.sleep(7.8)

    robot.stop()

    robot.leftOnSelf()
    time.sleep(0.3)

    robot.stop()

    robot.forward()
    time.sleep(2.5)

    robot.stop()
    time.sleep(1)

    robot.setPWMA(30)
    robot.setPWMB(30)

    robot.leftOnSelf()
    time.sleep(0.25)

    robot.stop()

    robot.forward()
    time.sleep(1)

    robot.stop()

    robot.setPWMA(50)
    robot.setPWMB(50)
    robot.stop()

    robot.forward()
    time.sleep(5.5)

    robot.stop()
if __name__  == '__main__':
    main()