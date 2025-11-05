import socket
import threading
import time
from libreries.AlphaBot2 import AlphaBot
from libreries import movement

IP = "0.0.0.0"
PORT = 55555


def auto_mode(robot):
    """
    Modalità automatica: esegue movement.avoid_obstacle(robot)
    finché l'utente non digita 'exit' o 'x' in console.
    """
    control = {"running": True}  # dizionario mutabile, usato come flag condiviso

    def read_exit():
        while control["running"]:
            exit_input = input("Per uscire dalla modalità automatica scrivi 'exit' o 'x': ").strip().lower()
            if exit_input in ["exit", "x"]:
                control["running"] = False

    # Avvio thread per ascoltare input da tastiera
    threading.Thread(target=read_exit, daemon=True).start()

    print("Modalità automatica attivata. Digita 'exit' per interrompere.")

    while control["running"]:
        movement.avoid_obstacle(robot)

    robot.stop()
    print("Uscita dalla modalità automatica.")


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
            data = conn.recv(1024).decode().strip()
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

            elif data.lower() == "x":
                robot.stop()
                conn.send(b"Stop")

            elif data.lower() == "auto mode":
                conn.send(b"Modalita' automatica attivata")
                auto_mode(robot)
                conn.send(b"Modalita' automatica terminata")

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
