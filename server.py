import socket
from libreries.AlphaBot2 import AlphaBot
from libreries import movement
import threading

IP = "0.0.0.0"
PORT = 55555

def reax_exit(exit):
    exit_input = input('Per uscire scrivi exit: ')
    
    if(exit_input.lower() == 'exit'):
        exit = False

def auto_mode(robot):
    exit = True

    while exit:
        threading.Thread(target=reax_exit, daemon=True, args=(exit, )).start()
        movement.avoid_obstacle(robot)

def main():
    robot = AlphaBot()
    robot.stop()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)

    print(f"Server in ascolto su {IP}:{PORT}...")
    
    conn, addr = server_socket.accept()
    print(f"Connessione accettata da {addr}")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"Comando ricevuto: {data}")

            if data.lower() == "w":
                robot.forward()
                conn.send(b"Avanti")
            elif data.lower() == "s":
                robot.backward()
                conn.send(b"Indietro")
            elif data.lower() == "a":
                robot.left()
                conn.send(b"Sinistra")
            elif data.lower() == "d":
                robot.right()
                conn.send(b"Destra")
            elif data.lower() == 'auto mode':
                auto_mode(robot)
                conn.send(b"auto mode attivata")
            elif data.lower() == "x":
                robot.stop()
                conn.send(b"Stop")
            elif data.lower() == "exit":
                robot.stop()
                conn.send(b"Chiusura server")
                break
            else:
                conn.send(b"Comando non riconosciuto")

    except KeyboardInterrupt:
        print("Interruzione manuale.")
        robot.stop()
    finally:
        robot.stop()
        conn.close()
        server_socket.close()
        print("Server chiuso.")

if __name__ == '__main__':
    main()
