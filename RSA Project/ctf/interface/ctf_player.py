import socket

server_ip = '127.0.0.1' # CHANGE BEFORE PRODUCT
port = 12345 #Maybe each player will have unique port?

player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main_menu():
    player_socket.connect((server_ip, port))
    plot = """\
    Welcome, Agent 007.

    You have been chosen to take part in a top-secret mission to thwart the attempt of a hostile government to launch a nuclear strike against an undisclosed target. 

    Our intelligence suggests that a rogue faction, operating under the codename "Project Cerberus," has acquired decommissioned nuclear warheads and is working to bypass the outdated but still dangerous security systems of an abandoned military silo.

    Your mission is to infiltrate their communication channels, decode their encryption methods, and sabotage their launch sequence before it’s too late. Time is running out, and conventional intelligence methods have failed. That’s where you come in.

    Thanks to our advanced signal intelligence division, we’ve managed to intercept fragments of their encrypted transmissions. While we were unable to decrypt everything, we obtained a crucial piece of data—a leaked message file.

    This file contains valuable information that will help you breach their defenses. "Project Cerberus" is protected by four layers of security systems, each requiring a separate password. Your first objective is to analyze the 'leaked_message' file and retrieve the password for the first system.

    If you can break through, you will be one step closer to stopping the attack. 

    Good luck, Agent. The fate of millions rests in your hands.
    """

    print(plot)
    player_input = ""
    #solved_levels = []
    while player_input != "Q":
        player_input = input("Which system would you like to break? (0/1/2.1/2.2/2.3/3)\n")
        temp_flag_entry = True
        if player_input == "0":
            attack_sys_0(input("enter level 0 password\n"))
        elif player_input == "1":
            attack_sys_1(input("enter level 1 password\n"))
        elif player_input == "2.1":
            attack_sys_21(input("enter level 2.1 password\n"))
        elif player_input == "2.2":
            attack_sys_22(input("enter level 2.2 password\n"))
        elif player_input == "2.3":
            attack_sys_23(input("enter level 2.3 password\n"))
        elif player_input == "3":
            attack_sys_3(input("enter level 3 password\n"))
        else:
            print("Incorrect system number. try again.")
            temp_flag_entry = False


        #Instead the server will send the score.
        if temp_flag_entry:
            score = player_socket.recv(2048).decode()
            print(score)

def attack_sys_0(enterance_password):
    #Calling server on lvl_password to check if it's correct
    #if incorrect, return
    #if correct, gives them the shell to complete it
    player_socket.sendall("0".encode())
    player_socket.recv(1)
    player_socket.sendall(enterance_password.encode())
    link = player_socket.recv(2048).decode()
    if link != "Invalid":
        print(f"Download code skeleton from here: {link}\ncomplete it, and run it to find deciphered password for next level. \n")
        return True
    return False

def attack_sys_1(enterance_password):
    player_socket.sendall("1".encode())
    player_socket.recv(1)
    player_socket.sendall(enterance_password.encode())
    link = player_socket.recv(2048).decode()
    if link != "Invalid":
        print(f"Download code skeleton from here: {link}\ncomplete it, and run it to find deciphered password for next level. \n")
        #Code skeleton contains C0 and public key
        return True
    return False


def attack_sys_21(enterance_password):
    player_socket.sendall("2.1".encode())
    player_socket.recv(1)
    player_socket.sendall(enterance_password.encode())
    link = player_socket.recv(2048).decode()
    if link != "Invalid":
        print(f"Download code skeleton from here: {link}\ncomplete it, and run it to find deciphered password for next level. \n")
        return True
    return False

def attack_sys_22(enterance_password):
    player_socket.sendall("2.2".encode())
    player_socket.recv(1)
    player_socket.sendall(enterance_password.encode())
    link = player_socket.recv(2048).decode()
    if link != "Invalid":
        print(f"Download code skeleton from here: {link}\ncomplete it, and run it to find deciphered password for next level. \n")
        return True
    return False

def attack_sys_23(enterance_password):
    player_socket.sendall("2.3".encode())
    player_socket.recv(1)
    player_socket.sendall(enterance_password.encode())
    link = player_socket.recv(2048).decode()
    if link != "Invalid":
        print(f"Download code skeleton from here: {link}\ncomplete it, and run it to find deciphered password for next level. \n")
        return True
    return False


def attack_sys_3(enterance_password):
    player_socket.sendall("3".encode())
    player_socket.recv(1)
    player_socket.sendall(enterance_password.encode())
    link = player_socket.recv(2048).decode()
    if link != "Invalid":
        print(f"Download code skeleton from here: {link}\ncomplete it, and run it to find deciphered password for next level. \n")
        return True
    return False


main_menu()