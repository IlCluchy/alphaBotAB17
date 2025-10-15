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

# ---------- Funzioni sensori IR ----------


def read_sensors(robot):
    """0 = ostacolo, 1 = libero"""
    left = robot.getLeftIrSensor()
    right = robot.getRightIrSensor()
    return left, right

def avoid_obstacle(robot):

        left, right = read_sensors(robot)
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