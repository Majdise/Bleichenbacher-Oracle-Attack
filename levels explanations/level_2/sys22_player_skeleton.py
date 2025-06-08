import socket
from RSA import PCKS_unpadding
import gmpy2

host = '127.0.0.1' #IP TARGET
port = 6969

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


def one_step_next_s2(a1, b1, r, curr_s, c0,B,n,e):
    shigh = ceil(3*B + r * n, a1) - 1
    while curr_s > shigh:
        r += 1
        curr_s = ceil((2 * B + r * n), b1)
        shigh = ceil((3 * B + r * n), a1) - 1
    payload = (c0 * gmpy2.powmod(curr_s,e,n)) % n
    if communicate_with_server(payload) == "Valid":
        return True, curr_s, r
    else:
        curr_s += 1
        return False, curr_s, r


def gen_state(M, s,B,n):
    state = []
    for a1, b1 in M:
        r = ceil(2 * (b1 * s - 2 * B), n)
        slow = ceil((2 * B + r * n), b1)
        state.append((r, slow))
    return state


def parallel_threads(M, message, s,B,n,e,E_prime,F_prime):
    state = gen_state(M, s,B,n)
    while True:
        for i in range(len(M)):
            success, curr_s, r = one_step_next_s2(M[i][0], M[i][1], state[i][0], state[i][1], message,B,n,e)
            if success:
                M = update_intervals(M, curr_s,E_prime,F_prime,n)
                if len(M) == 1:
                    return curr_s, M
                else:
                    state = gen_state(M, curr_s,B,n)
                    break
            else:
                state[i] = (r, curr_s)
                
                
def update_intervals(M, si, E_prime, F_prime, n):
    M_nxt = []
    for tup in M:
        a_cur, b_cur = tup
        lower_bound = ceil((a_cur * si - F_prime), n)
        upper_bound = floor((b_cur * si - E_prime), n)
        for r_cur in range(lower_bound, upper_bound + 1):
            l_range = max(a_cur, ceil((E_prime + r_cur * n), si))
            r_range = min(b_cur, floor((F_prime + r_cur * n), si))
            if l_range > r_range:
                continue
            range_cur = (l_range, r_range)
            # Dealing with overlaps:
            # Worth mentioning it's possible to do this operation in O(nlogn),
            # but the number of ranges is quite small, so it's fine either way
            flag_insertion = True
            for i in range(len(M_nxt)):
                range_other = M_nxt[i]
                if not (range_cur[1] <= range_other[0] or range_cur[0] >= range_other[1]):
                    flag_insertion = False
                    range_merged = (min(range_cur[0], range_other[0]), max(range_cur[1], range_other[1]))
                    M_nxt[i] = range_merged
                    range_cur = range_merged

            if flag_insertion:
                M_nxt.append(range_cur)
    return M_nxt  
                
def start_attacking():
    global queries
    client_socket.connect((host, port))
    print("Attack started, beware!")

    # **Step 1: Receive Public Key (n, e)**
    n_len = int.from_bytes(client_socket.recv(2), 'big')
    n = int.from_bytes(client_socket.recv(n_len), 'big')

    e_len = int.from_bytes(client_socket.recv(2), 'big')
    e = int.from_bytes(client_socket.recv(e_len), 'big')
    
    
    c0_len = int.from_bytes(client_socket.recv(4), 'big')
    c0 = int.from_bytes(client_socket.recv(c0_len),'big')
    
    k = (n.bit_length()+7)//8

    si = 1
    B = 2**(8*(k-2))
    E_prime = 2*B + ((256**49)*((256**(k-51))-1))//255
    F_prime = 3*B - 255*((256**48)-1)
#    M = [(E_prime,F_prime)]
    M = '''Complete the missing line'''
    counter = 0

    '''STEP 1: irrelevant for our use. '''
    '''STEP 2:'''
    print("Staring step 2")
    while not (len(M) == 1 and M[0][0] == M[0][1]):
        counter += 1
        if counter==1 or len(M) > 1:
            print("Staring step 2A")
            if counter == 1:#counter>1 && len(M) =0
                si = '''Complete the missing line'''
#                si = ceil(n,(F_prime+1))
                payload = (c0 * gmpy2.powmod(si,e,n)) % n
                print("Entering while loop in step '''2.A AND 2.B'''")
                while communicate_with_server(payload) == "Invalid":
                    si += 1
                    payload = (c0 * gmpy2.powmod(si,e,n)) % n
                print("Out of while loop in step '''2.A AND 2.B'''")
            print("Staring step 2B")
#            if len(M) > 1:##counter>1 && len(M) > 1
            if '''Complete the missing condition'''

                si,M = parallel_threads(M, c0, si,B,n,e,E_prime,F_prime)                
                
        else:##counter>1 && len(M) = 1
            print("Staring step 2C")
            s_nxt = -1
            flag = False
            a_cur, b_cur = M[0]
#           ri = ceil(2 * (b_cur * si - E_prime), n)
            ri = '''Complete the missing line'''
            while not flag:
#                lower_bound = ceil((E_prime+ri*n),b_cur)
                lower_bound = '''Complete the missing line'''
                upper_bound = floor((F_prime+ri*n),a_cur)
                for s_cand in range(lower_bound,upper_bound+1):
                    payload = (c0 * gmpy2.powmod(s_cand, e, n)) % n
                    if communicate_with_server(payload) == "Valid":
                        s_nxt = s_cand
                        flag = True
                        break
                ri += 1
            si = s_nxt ##flag raised,si has been found, go to step 3   
        print("Staring step 3")
        M = update_intervals(M,si,E_prime,F_prime,n)
        print(f"M size inside loop : {len(M)}")
        print(f"M inside loop is: : {M}")

    print("Staring step 4")
    #Now we have the integer value of the padded message. back to bytes and depadding:
    m = M[0][0]
    original_message_padded = m.to_bytes(128,'big')
    original_message = PCKS_unpadding(original_message_padded)
    print(f"Original messsage retrieved : {original_message.decode()}")
    print(f"Number of oracle calls : {queries}")

start_attacking()
