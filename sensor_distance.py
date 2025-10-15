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
    robot.setPWMA(50)
    robot.setPWMB(50)
    robot.stop()
    
    try:
        while True:
            # Legge i sensori IR
            left = GPIO.input(IR_L)
            right = GPIO.input(IR_R)

            print(f"Sensore sinistro: {left}, destro: {right}")
            
            if left == 1 and right == 1:
                # Nessun ostacolo, avanti
                robot.forward()

            elif left == 0 and right == 1:
                # Ostacolo a sinistra, gira a destra
                robot.rightOnSelf()
                time.sleep(0.2)
                robot.forward()

            elif left == 1 and right == 0:
                # Ostacolo a destra, gira a sinistra
                robot.leftOnSelf()
                time.sleep(0.2)
                robot.forward()

            elif left == 0 and right == 0:
                # Ostacolo davanti, indietreggia e gira
                robot.backward()
                time.sleep(0.3)
                robot.leftOnSelf()
                time.sleep(0.4)

            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("Programma terminato.")
        robot.stop()
        GPIO.cleanup()

if __name__  == '__main__':
    main()