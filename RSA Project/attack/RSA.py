from sympy import randprime
import random
import gmpy2

#Implementing 1024 bits RSA encryption and decryption protocol
BVO_oracle = False


def gen_key():
    bits_len = 512
    lower_bound = 2**(bits_len-1)
    upper_bound = 2**bits_len - 1
    p = randprime(lower_bound,upper_bound)
    q = randprime(lower_bound,upper_bound)

    while abs(p-q) < 2**128: #A known vulnerability of RSA if |p-q| is small
        p = randprime(lower_bound, upper_bound)
        q = randprime(lower_bound, upper_bound)

    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e,-1,phi)
    n = p*q

    pub_key = (e,n)
    priv_key = (d,n)

    return pub_key,priv_key

def enc_integer(pub_key, m):
    return gmpy2.powmod(m,pub_key[0],pub_key[1])#pow(m,pub_key[0],pub_key[1])

def dec_integer(priv_key, c):
    return gmpy2.powmod(c,priv_key[0],priv_key[1])#pow(c,priv_key[0],priv_key[1])

def enc_msg(msg,pub_key,BVO = False):
#def enc_msg(msg,pub_key, BVO = False):
    BVO_oracle = BVO
    msg_bytes = PCKS_padding(msg, pub_key[1],BVO)
    num_msg = int.from_bytes(msg_bytes,"big")
    temp_val = enc_integer(pub_key,num_msg)
    temp_len = (pub_key[1].bit_length() + 7)//8 #After padding the length agrees with the modulus's one
    return temp_val.to_bytes(temp_len,'big')

def dec_msg(msg_bytes,priv_key):
    num_msg = int.from_bytes(msg_bytes,"big")
    temp_val = dec_integer(priv_key,num_msg) #Bad line?

    temp_len = (priv_key[1].bit_length() + 7)//8 #After padding the length agrees with the modulus's one
    padded_msg = temp_val.to_bytes(temp_len,'big')
    #original_message = PCKS_unpadding(padded_msg).decode("utf-8")
    return padded_msg #original_message

def PCKS_padding(message, modulus,BVO):
#def PCKS_padding(message, modulus, BVO):

    '''Padding a string message and returns it padded (in bytes form)'''
    msg_bytes = message.encode()
    if BVO:
        msg_bytes = b"\x03\x03" + msg_bytes
    padding = b"\x00\x02"
    k = (modulus.bit_length() + 7)//8
    D = len(msg_bytes)
    while len(padding) + D < k-1:
        cur_byte = int.to_bytes(random.randint(1,255),1,'big')
        padding += cur_byte
    padding += b"\x00"

    return padding + msg_bytes

def PCKS_unpadding(padded_message):
    '''Unpadding a bytes decrypted string message and returns it (bytes)'''
    if padded_message[:2] != b"\x00\x02":
        print("Error! invalid padding - first 2 bytes")
        return
    try:
        nullbyteSeperating = padded_message[1:].index(0x00)
        original_message_bytes = padded_message[nullbyteSeperating+2:]
        if BVO_oracle:
            original_message_bytes = original_message_bytes[2:]

        return original_message_bytes
    except ValueError:
        print("Error! invalid padding - missing null byte")
        return
