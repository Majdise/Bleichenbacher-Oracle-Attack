import socket
from RSA import PCKS_unpadding
import gmpy2

host = '127.0.0.1' #IP TARGET
port = 15342

queries = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#A lot of time spent on this - DONT AND I REPEAT DONT USE FLOAT (IN OUR CASE math.ceil/floor) - A LOSS OF PRECISION

#Thus we use self-made such functions

def ceil(x,y):
    return x//y + (x%y > 0)

def floor(x,y):
    return x//y

def communicate_with_server(payload):
    global queries
    payload_bytes = payload.to_bytes((payload.bit_length()+7)//8,'big')
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

    n_len = int.from_bytes(client_socket.recv(2), 'big')
    n = int.from_bytes(client_socket.recv(n_len), 'big')

    e_len = int.from_bytes(client_socket.recv(2), 'big')
    e = int.from_bytes(client_socket.recv(e_len), 'big')

    public_key = (n, e)
    k = (n.bit_length()+7)//8


    c0_len = int.from_bytes(client_socket.recv(4), 'big')
    c0 = int.from_bytes(client_socket.recv(c0_len), 'big')

    si = 1
    B = 2**(8*(k-1))
    M = [(2*B,3*B-1)]
    counter = 0
    
    ##אולי צריך לשים פה מודולו n על החישובים
    
    '''STEP 1: irrelevant for our use. '''
    print("Starting step 1")
    f1_2='''Complete the missing line'''
    while True:
        payload = (c0 * gmpy2.powmod((2*f1_2),e,n)) % n
        ans=communicate_with_server(payload)
        ## "Valid" = "< B"
        if ans=="Invalid":
            break
        else:
            '''Complete the missing line'''
    

            
    '''STEP 2:'''

    print("Staring step 2")
    f2=(f1_2*floor(n+B,B))
    while True:
        payload = (c0 * gmpy2.powmod((f2),e,n)) % n
        ans=communicate_with_server(payload)
        if ans=="Invalid":
            '''Complete the missing line'''
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
            '''Complete the missing line'''
        else:
            '''Complete the missing line'''
            
    '''STEP 4:'''
    #Now we have the integer value of the padded message. back to bytes and depadding:

    m = '''Complete the missing line'''
    original_message_padded = m.to_bytes(128,'big')
    original_message = PCKS_unpadding(original_message_padded)
    print(f"Original messsage retrieved : {original_message.decode()}")
    print(f"Number of oracle calls : {queries}")

start_attacking()