from libreries.AlphaBot import AlphaBot
import RPi.GPIO as GPIO
import time

#pin sensori IR
IR_L = 19  #sensore sinistro
IR_R = 16  #sensore destro

# settaggio dei sensori
GPIO.setmode(GPIO.BCM) #setta i pin
GPIO.setup(IR_L, GPIO.IN)  #setta i pin in input
GPIO.setup(IR_R, GPIO.IN) 
def main():

    robot = AlphaBot()
    '''
    Abbiamo messo la velocità minima per rendere i movimenti il più fluidi possibili ed evitare errori
    di slittamento delle ruote.
    '''
    robot.setPWMA(30)
    robot.setPWMB(30)
    robot.stop()
    
    try:
        while True:
            #legge i sensori IR
            left = GPIO.input(IR_L)
            right = GPIO.input(IR_R)

            print(f"Sensore sinistro: {left}, destro: {right}")
            
            if left == 1 and right == 1:
                #nessun ostacolo, avanti
                robot.forward()

            elif left == 0 and right == 1:
                #ostacolo a sinistra, gira a destra
                robot.backward()
                time.sleep(0.2)
                robot.rightOnSelf()
                time.sleep(0.5)
                robot.forward()

            elif left == 1 and right == 0:
                #ostacolo a destra, gira a sinistra
                robot.backward()
                time.sleep(0.2)
                robot.leftOnSelf()
                time.sleep(0.5)
                robot.forward()

            elif left == 0 and right == 0:
                #ostacolo davanti, indietreggia e gira
                robot.backward()
                time.sleep(0.3)
                robot.leftOnSelf()
                time.sleep(0.5)

            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("Programma terminato.")
        robot.stop()
        GPIO.cleanup()

if __name__  == '__main__':
    main()