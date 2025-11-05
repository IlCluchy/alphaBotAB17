from libreries.AlphaBot import AlphaBot
import RPi.GPIO as GPIO
import time

def forward_first(robot, total_time):
    #settiamo la velocità per essere sicuri della velocità delle ruote
    robot.setPWMA(30) #sinistra
    robot.setPWMB(30) #destra
    
    while total_time > 0:
        if total_time == 5:
            '''
            Gli abbiamo fatto fare un curva a destra per correggere la traettoria
            '''
            robot.rightOnSelf()
            time.sleep(0.2)
        
        if total_time >= 1:
            robot.forward()
            time.sleep(1)
            total_time -= 1

            robot.stop()
            time.sleep(0.5)
        else:
            '''
            Se il total time è minore di 1 fa solo quello rimasto ed esce dalla funzione
            '''
            robot.forward()
            time.sleep(total_time)
            total_time = 0
            robot.stop()
            time.sleep(0.5)

    robot.stop()


def main():
    robot = AlphaBot()
    robot.setPWMA(30) #sinistra
    robot.setPWMB(30) #destra
    robot.stop()

    forward_first(robot, 15.3)

    robot.leftOnSelf()
    time.sleep(1.1)
    robot.stop()

    robot.forward()
    time.sleep(2)
    robot.stop()
    time.sleep(1)

    #settiamo la velocità per essere sicuri della velocità delle ruote
    robot.setPWMA(30)
    robot.setPWMB(30)

    robot.leftOnSelf()
    time.sleep(0.6)
    robot.stop()

    forward_first(robot, 15.5)
    robot.stop()

if __name__  == '__main__':
    main()