import socket
import threading
import RSA

pub_key, priv_key = RSA.gen_key()


oracle_type = "BVO"
soundness = False
soundness_probability = 0.05


def SPCKS_Conforming(cipher):
    global priv_key
    n = pub_key[1]
    k = (n.bit_length()+7)//8
    decrypted = RSA.dec_msg(cipher,priv_key)
    if decrypted[:2] == b"\x00\x02":
        print(f"@SPCKS_Conforming decrypted[:2] : {decrypted[:2]}, decrypted[k-49]: {decrypted[k-49]}")
        zero = (decrypted[k-49] == 0)
        if zero:
            print(f"@SPCKS_Conforming isZero: {zero}")
            wrong_vnumbers = (decrypted[k-48:k-46] != b"\x03\x03")
            if wrong_vnumbers:
                nonzeros = all ((x != 0) for x in decrypted[2:k-49])
                print(f"@SPCKS_Conforming isNonzeros: {nonzeros}")
                return nonzeros
            return False
        return False
    return False
    
def handle_client(client_socket, addr):
    print(f"New connection from {addr}")

    try:
        message = "super_random"

        # **Step 1: Send the Public Key (n, e)**
        n_bytes = pub_key[1].to_bytes((pub_key[1].bit_length() + 7) // 8, 'big')
        e_bytes = pub_key[0].to_bytes((pub_key[0].bit_length() + 7) // 8, 'big')

        client_socket.send(len(n_bytes).to_bytes(2, 'big'))  # Send length of n
        client_socket.send(n_bytes)  # Send n
        client_socket.send(len(e_bytes).to_bytes(2, 'big'))  # Send length of e
        client_socket.send(e_bytes)  # Send e

        # **Step 2: Send the Encrypted Message**
        temp_sniffed = RSA.enc_msg(message, pub_key,True)
        client_socket.send(len(temp_sniffed).to_bytes(4, 'big'))  # Send length of message
        client_socket.send(temp_sniffed)  # Send message

        # **Step 3: Handle Player Queries**
        while True:
            encrypted_data = client_socket.recv(2048)
            if not encrypted_data:
                break  # Client disconnected

            if SPCKS_Conforming(encrypted_data):
                client_socket.send(b"Valid")
            else:
                client_socket.send(b"Invalid")

    except Exception as e:
        print(f"Error with {addr}: {e}")

    finally:
        client_socket.close()
        print(f"Connection closed for {addr}")


def start_server():
    global oracle_type, soundness
    
    oracle_type = "BVO"  # Hardcoded for now
    soundness = False  # Hardcoded for now

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5070))  # System port - 42069
    server_socket.listen(50)  # Allow multiple connections   

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.daemon = True  # Automatically closes thread on exit
        client_thread.start()



start_server()
