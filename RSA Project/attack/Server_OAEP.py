import socket
import RSA
import random

from RSA import PCKS_padding

pub_key, priv_key = RSA.gen_key()

oracle_type = "TTT"
soundness = False
soundness_probability = 0.05

def PCKS_Conforming(candidate):
    global priv_key
    dec_candidate = RSA.dec_msg(candidate,priv_key)
    bit_flag = (random.random() < soundness_probability) and soundness
    #flipping answer
    if bit_flag:
        if oracle_type == "OAEP":
            return not dec_candidate[:1] == b"\x00"
        else:
            if dec_candidate[:2] == b"\x00\x02":
                try:
                    if dec_candidate[2:].index(0x00) >= 11: #FFT
                        return not True
                    else: #A zero in first, FTT
                        return not oracle_type[1] == 'T'
                except ValueError: #No zeros..., TFT
                    return not oracle_type[0] == 'T'

            return not False

    else:
        if oracle_type == "OAEP":
            return dec_candidate[:1] == b"\x00"
        else:
            if dec_candidate[:2] == b"\x00\x02":
                try:
                    if dec_candidate[2:].index(0x00) >= 11:  # FFT
                        return True
                    else:  # A zero in first, FTT
                        return (oracle_type[1] == 'T')
                except ValueError:  # No zeros..., TFT
                    return (oracle_type[0] == 'T')
            return False


def start_server():
    global pub_key,priv_key,oracle_type,soundness
    message = input("Enter a secret!\n")
    oracle_type = input("Choose an oracle type; TTT,TFT, FFT or FTT or OAEP\n")
    sound_type = input("Noisy oracle type; T or F\n")
    print(f"Encoded message: {message.encode()}")
    if sound_type == 'T':
        soundness = True
    #soundness = True if sound_type == 'T' else soundness = False
    #third T - not of fixed length.
    #second T - may contain zero byte in first 8 bytes (after 0x00 and 0x02)
    #first T - doesn't contain a zero (except first byte)

    if oracle_type != "TTT" and oracle_type != "TFT" and oracle_type != "FFT" and oracle_type !="OAEP":
        print("WRONG ORACLE TYPE")
        return

    with open("public_key", "wb") as file:
        file.write(pub_key[0].to_bytes((pub_key[0].bit_length()+7)//8,'big'))
        file.write(pub_key[1].to_bytes((pub_key[1].bit_length()+7)//8,'big'))

    with open("encrypted_message", "wb") as file:
        temp_sniffed = RSA.enc_msg(message,pub_key,False)
        file.write(temp_sniffed)


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345

    server_socket.bind((host, port))
    print("Server is waiting for connection...")
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        encrypted_data = client_socket.recv(2048)
        if PCKS_Conforming(encrypted_data):
            client_socket.send(b"Valid")
        else:
            client_socket.send(b"Invalid")


start_server()