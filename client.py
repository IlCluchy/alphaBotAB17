import socket

IP = "192.168.1.112" 
PORT = 5555

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print("Connessione al server stabilita.")
    print("Comandi disponibili:")
    print("  W = Avanti")
    print("  S = Indietro")
    print("  A = Sinistra")
    print("  D = Destra")
    print("  X = Stop")
    print("  exit = Chiudi il programma\n")

    try:
        while True:
            comando = input("Inserisci comando (w/a/s/d/auto mode/x/exit): ").lower()

            if comando in ['w', 'a', 's', 'd', 'auto mode','x', 'exit']:
                client_socket.send(comando.encode())

                if comando == "exit":
                    print("Chiusura client...")
                    break

                risposta = client_socket.recv(1024).decode()
                print(f"Risposta dal server: {risposta}")
            else:
                print("Comando non valido! Usa solo w, a, s, d, x o exit.")

    except KeyboardInterrupt:
        print("\nInterruzione manuale.")
    finally:
        client_socket.close()
        print("Connessione chiusa.")


if __name__ == '__main__':
    main()