from libreries.AlphaBot import AlphaBot
import time

TIME_DEGREE = 0.0031 # secondi per grado (circa)

def move_forward(robot, duration=0.5, speed=40):
    robot.forward()
    robot.setPWMA(speed) #motore destro
    robot.setPWMB(speed) #motore sinistro
    time.sleep(duration)
    robot.stop()
    time.sleep(0.2)

def square(robot, direction, speed, forward_time, turn_delay):
    for _ in range(4):
        move_forward(robot, forward_time, speed)
        if direction == 'right':
            right(robot, 90, speed)
        else:
            left(robot, 90, speed)
        time.sleep(turn_delay)

def triangle(robot, direction, speed, forward_time, turn_delay):
    for _ in range(3):
        move_forward(robot, forward_time, speed)
        if direction == 'right':
            right(robot, 120, speed)
        else:
            left(robot, 120, speed)
        time.sleep(turn_delay)

def circle(robot, direction, speed, duration):

    if direction == 'right':
        #motore sinistro più veloce, motore destro più lento
        robot.setPWMA(int(speed * 0.5))  #motore destro
        robot.setPWMB(speed)              #motore sinistro
        robot.forward()
    elif direction == 'left':
        #motore destro più veloce, motore sinistro più lento
        robot.setPWMA(speed)              #motore destro
        robot.setPWMB(int(speed * 0.5))  #motore sinistro
        robot.forward()
    else:
        print("Direzione non valida! Usa 'right' o 'left'.")
        return

    time.sleep(duration)
    robot.stop()

def right(robot, degree, speed = 20):
    
    rotation_time = degree * TIME_DEGREE
    
    robot.rightOnSelf()          #gira su se stesso verso destra
    time.sleep(rotation_time)
    robot.stop()

def left(robot, degree):

    rotation_time = degree * TIME_DEGREE
    
    robot.leftOnSelf()          #gira su se stesso verso destra
    time.sleep(rotation_time)
    robot.stop()

def main():
    robot = AlphaBot()
    #right(robot, 90)
    #square(robot, 'right', 40, 0.5, 0.2)
    #triangle(robot, 'right', 40, 0.5, 0.2)
    circle(robot, 'right', 40, 3)

if __name__ == '__main__':
    main()