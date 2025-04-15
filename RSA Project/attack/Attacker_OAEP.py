import socket
from RSA import PCKS_unpadding
import gmpy2

host = '127.0.0.1'
port = 12345

queries = 0

with open("public_key", "rb") as file:
    first_var = int.from_bytes(file.read(3),'big') #e = 2**16 + 1
    second_var = int.from_bytes(file.read(128),'big') #as n is 1024 bits
    public_key = (first_var,second_var)

with open("encrypted_message", "rb") as file:
    sniffed_message = file.read(128)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#A lot of time spent on this - DONT AND I REPEAT DONT USE FLOAT (IN OUR CASE math.ceil/floor) - A LOSS OF PRECISION

#Thus we use self-made such functions

def ceil(x,y):
    return x//y + (x%y > 0)

def floor(x,y):
    return x//y

def communicate_with_server(payload):
    global queries
    payload_bytes = payload.to_bytes((payload.bit_length()+7)//8)
    client_socket.sendall(payload_bytes)

    response = client_socket.recv(1024).decode()
    queries += 1
    if queries % 10000 == 0:
        print(f"{queries} calls have been made.")

    return response

def start_attacking():
    global queries
    client_socket.connect((host, port))
    print("Attack started, beware!")

    n = public_key[1]
    k = (n.bit_length()+7)//8
    e = public_key[0]
    c0 = int.from_bytes(sniffed_message, 'big')

    si = 1
    B = 2**(8*(k-1))
    M = [(2*B,3*B-1)]
    counter = 0
    num_of_lvls = 0
    
    ##אולי צריך לשים פה מודולו n על החישובים
    
    '''STEP 1: irrelevant for our use. '''
    print("Starting step 1")
    f1_2=1
    while True:
        payload = (c0 * gmpy2.powmod((2*f1_2),e,n)) % n
        ans=communicate_with_server(payload)
        ## "Valid" = "< B"
        if ans=="Invalid":
            break
        else:
            f1_2=(f1_2*2)
    

            
    '''STEP 2:'''

    print("Staring step 2")
    f2=(f1_2*floor(n+B,B))
    while True:
        payload = (c0 * gmpy2.powmod((f2),e,n)) % n
        ans=communicate_with_server(payload)
        if ans=="Invalid":
            f2=f2+f1_2
        else:
            break
    
    '''STEP 3:'''
    print("Starting step 3")
    Mmin=ceil(n,f2)
    Mmax=floor(n+B,f2)
    while Mmin<Mmax: 
        ftmp=floor(2*B,Mmax-Mmin)
        i=floor(ftmp*Mmin,n)
        f3=ceil(i*n,Mmin)
        payload = (c0 * gmpy2.powmod((f3),e,n)) % n
        ans=communicate_with_server(payload)
        if ans=="Invalid":
            Mmin=ceil(i*n+B,f3)
        else:
            Mmax=floor(i*n+B,f3)
            
    '''STEP 4:'''
    #Now we have the integer value of the padded message. back to bytes and depadding:

    m = Mmin
    original_message_padded = m.to_bytes(128,'big')
    original_message = PCKS_unpadding(original_message_padded)
    print(f"Original messsage retrieved : {original_message.decode()}")
    print(f"Number of oracle calls : {queries}")

start_attacking()