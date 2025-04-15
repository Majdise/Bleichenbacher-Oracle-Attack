import socket
import RSA

pub_key, priv_key = RSA.gen_key()

oracle_type = "BVO"

def PCKS_Conforming(candidate):
    global priv_key
    dec_candidate = RSA.dec_msg(candidate,priv_key)

    if dec_candidate[:2] == b"\x00\x02":
        #print(f"()^e value: : {int.from_bytes(dec_candidate,'big')}")
        try:
            if dec_candidate[2:].index(0x00) >= 11: #FFT
                return True
            else: #A zero in first, FTT
                return oracle_type[1] == 'T'
        except ValueError: #No zeros..., TFT
            return oracle_type[0] == 'T'

    return False


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
    

def start_server():
    global pub_key,priv_key,oracle_type
    message = input("Enter a secret!\n")
    oracle_type = input("Choose an oracle type; TTT,TFT, FFT, FTT or BVO\n")
    #third T - not of fixed length.
    #second T - may contain zero byte in first 8 bytes (after 0x00 and 0x02)
    #first T - doesn't contain a zero (except first byte)

    if oracle_type != "TTT" and oracle_type != "TFT" and oracle_type != "FFT" and oracle_type != "BVO":
        print("WRONG ORACLE TYPE")
        return

    with open("public_key", "wb") as file:
        file.write(pub_key[0].to_bytes((pub_key[0].bit_length()+7)//8,'big'))
        file.write(pub_key[1].to_bytes((pub_key[1].bit_length()+7)//8,'big'))

    with open("encrypted_message", "wb") as file:
        file.write(RSA.enc_msg(message,pub_key, oracle_type=="BVO"))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 5072

    server_socket.bind((host, port))
    print("Server is waiting for connection...")
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        encrypted_data = client_socket.recv(2048)
        if oracle_type != "BVO":
            if PCKS_Conforming(encrypted_data):
                client_socket.send(b"Valid")
            else:
                client_socket.send(b"Invalid")
        else:
            if SPCKS_Conforming(encrypted_data):
                print(f"oracle_type is  {oracle_type}")
                client_socket.send(b"Valid")
            else:
                client_socket.send(b"Invalid")


start_server()
