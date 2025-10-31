from libreries.AlphaBot import AlphaBot
import RPi.GPIO as GPIO
import time

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

    try:
        for lato in range(4):
            print(f"Lato {lato + 1} del quadrato")

            while True:
                left = GPIO.input(IR_L)
                right = GPIO.input(IR_R)

                if left == 1 and right == 1:
                    print("Gira a sinistra.")
                    robot.stop()
                    time.sleep(0.2)
                    robot.leftOnSelf()
                    time.sleep(0.3)
                    robot.stop()
                    time.sleep(0.2)
                    break

                elif left == 0 and right == 1: #muro a destra --> continua
                    robot.forward()

                elif left == 0 and right == 0: #troppo vicino al muro --> gira leggermente
                    robot.right()
                    time.sleep(0.1)

                elif left == 1 and right == 0: #se perde il muro gira leggermente
                    print("Perso il muro → gira leggermente a sinistra")
                    robot.left()
                    time.sleep(0.1)

                time.sleep(0.05)

        robot.stop()

    except KeyboardInterrupt:
        print("Programma interrotto.")
        robot.stop()
        GPIO.cleanup()

    GPIO.cleanup()

if __name__ == "__main__":
    main()
