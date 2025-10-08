import time
from AlphaBot import AlphaBot
import RPi.GPIO as GPIO

if __name__ == '__main__':
    robot = AlphaBot()

    try:
        print("Il robot va avanti per 2 secondi...")
        robot.forward()
        time.sleep(2)
        print("Stop!")
        robot.stop()
    except KeyboardInterrupt:
        robot.stop()
    finally:
        robot.stop()
