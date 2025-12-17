import socket
import threading
import datetime

BROADCAST_IP = '10.42.214.255'  # Cambiar según tu red
PORT = 12345
MAX_LEN = 100  # Longitud máxima del mensaje

def recibir_mensajes(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            mensaje = data.decode('utf-8')
            # Esperamos mensaje en formato "usuario|mensaje"
            if "|" in mensaje:
                usuario, texto = mensaje.split("|", 1)
            else:
                usuario, texto = "Desconocido", mensaje
            hora = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n[{hora}] {usuario}: {texto}")
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

def enviar_mensajes(sock, usuario):
    while True:
        mensaje = input(f"{usuario}: ")
        # Limitar longitud
        if len(mensaje) > MAX_LEN:
            print(f"Error: El mensaje no debe exceder {MAX_LEN} caracteres.")
            continue
        if mensaje.strip() == "":
            continue
        texto = f"{usuario}|{mensaje}"
        try:
            sock.sendto(texto.encode('utf-8'), (BROADCAST_IP, PORT))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            break

def main():
    print("**************************************************") # Liena para separar programa
    print(" ") # Separacion de Linea
    usuario = input("Introduce tu nombre de usuario: ").strip()
    print(" ") # Separacion de Liena
    print("**************************************************") # Linea para separar programa
    print(" ") # Separacion de Linea

    if not usuario:
        usuario = "Usuario"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", PORT))
    threading.Thread(target=recibir_mensajes, args=(sock,), daemon=True).start()
    enviar_mensajes(sock, usuario)

if __name__ == "__main__":
    main()
