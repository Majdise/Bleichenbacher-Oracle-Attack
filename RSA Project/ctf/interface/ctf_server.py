import socket
import threading
from RSA import PCKS_unpadding

LEVEL_PASSWORDS = {
    "0": "secret_0",
    "1": "o7 buddy",
    "2.1": "random",
    "2.2": "super_random",
    "2.3": "you fell from heaven?",
    "3": "LOL somebody actually made it"
}

LEVEL_LINKS = {
    "0": "secret_0",
    "1": "o7 buddy",
    "2.1": "random",
    "2.2": "super_random",
    "2.3": "you fell from heaven?",
    "3": "LOL somebody actually made it"
}

def calculate_score(lst):
    result = 0
    if "0" in lst:
        result += 1
    if "1" in lst:
        result += 2
    if "2.1" in lst:
        result += 3
    if "2.2" in lst:
        result += 3
    if "2.3" in lst:
        result += 3
    if "3" in lst:
        result += 5
    return result

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    levels_solved = []

    try:
        while True:
            system_choice = client_socket.recv(1024).strip().decode()
            if not system_choice:
                break  # Client disconnected

            client_socket.send(bytes([0x01]))  # Send confirmation byte

            password_attempt = client_socket.recv(1024).strip().decode()
            if not password_attempt:
                break  # Client disconnected

            if system_choice in LEVEL_PASSWORDS and LEVEL_PASSWORDS[system_choice] == password_attempt:
                #Player is awarded for solving the level
                if system_choice not in levels_solved:
                    levels_solved.append(system_choice)

                #And gets a link to skeleton of next level.
                client_socket.send(LEVEL_LINKS[system_choice].encode())
            else:
                client_socket.send(b"Invalid")

            current_score = f"Your score is {calculate_score(levels_solved)}"

            client_socket.send(current_score.encode())


    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed for {addr}")

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(50)  # Allow multiple connections
    #print("Server is waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.daemon = True  # Automatically close thread when main process exits
        client_thread.start()

run_server()