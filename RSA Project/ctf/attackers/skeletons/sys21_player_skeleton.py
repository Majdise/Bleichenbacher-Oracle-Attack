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

def start_attacking():
    global queries
    client_socket.connect((host, port))
    print("Attack started, beware!")

    # **Step 1: Receive Public Key (n, e)**
    n_len = int.from_bytes(client_socket.recv(2), 'big')
    n = int.from_bytes(client_socket.recv(n_len), 'big')

    e_len = int.from_bytes(client_socket.recv(2), 'big')
    e = int.from_bytes(client_socket.recv(e_len), 'big')

    public_key = (n, e)
    k = (n.bit_length()+7)//8


    c0_len = int.from_bytes(client_socket.recv(4), 'big')
    c0 = int.from_bytes(client_socket.recv(c0_len),'big')

    si = 1
    B = 2 ** (8 * (k - 2))
    M = [(2 * B, 3 * B - 1)]
    counter = 0

    '''STEP 1, Trimming M0: '''

    print("Starting Trimming")
    st = 3
    sb = 7

    # Idea - find all t which divides m0, by checking m0*(t+-1)/t is conforming, if not then (t+-2)/t, so on up to t(+-st)/t
    # t <= 2^12, found in experimental way
    # only check t which are coprime to current lcm.

    u_low, u_high = n - 1, 1
    lcm_t = 1

    for t_i in range(4, 4096 + 1):
        if '''Complete the missing line''' : 
            continue
        if gmpy2.gcd(lcm_t, t_i) > 1: 
            continue


        flag_t = False

        for x in range(1, st + 1):
            if flag_t:
                break

            for j in range(0, 1 + 1):
                if flag_t:
                    break

                u_cur = '''Complete the missing line'''

                payload = '''Complete the missing line'''

                if communicate_with_server(payload) == "Valid":
                    flag_t = True

        if flag_t:
            lcm_t *= t_i

    # Calculate lcm(t_i) = t'
    # binary search u_low in [floor(2t'/3) + 1,t'] for which m0*u/t' is conforming ,u_high in [t',ceil(3t'/2)-1].

    if lcm_t > 1:
        inv_t = gmpy2.powmod(lcm_t, -1, n)

        # Now we binary search u_low:
        r_bound = lcm_t
        l_bound = floor(2 * lcm_t, 3) + 1
        

        while l_bound <= r_bound:
            middle = floor(l_bound + r_bound, 2)
            flag_bin = False
            for j in range(0, sb + 1):
                if '''Complete the missing part here''' and gmpy2.gcd(middle - j, lcm_t) == 1:
                    u_cand = (middle - j) * inv_t
                    payload = c0 * gmpy2.powmod(u_cand, e, n)

                    if communicate_with_server(payload) == "Valid":
                        flag_bin = True
                        u_low = middle - j
                        r_bound = middle - 1
                        break
            if not flag_bin:
                l_bound = middle + 1

        # Now we binary search u_high:
        l_bound = lcm_t
        r_bound = ceil(3 * lcm_t, 2) - 1

        while l_bound <= r_bound:
            middle = floor(l_bound + r_bound, 2)
            flag_bin = False
            for j in range(0, sb + 1):
                if '''Complete the missing part here''' and gmpy2.gcd(middle + j, lcm_t) == 1:
                    u_cand = (middle + j) * inv_t
                    payload = c0 * gmpy2.powmod(u_cand, e, n)

                    if communicate_with_server(payload) == "Valid":
                        flag_bin = True
                        u_high = middle + j
                        l_bound = middle + 1
                        break
            if not flag_bin:
                r_bound = middle - 1

        trimmed_range = '''Complete the missing line'''
        M = [(max(trimmed_range[0], M[0][0]), min(trimmed_range[1], M[0][1]))]

    '''STEP 2:'''

    print("Staring step 2")
    while not (len(M) == 1 and M[0][0] == M[0][1]):
        counter += 1
        if counter == 1:
            '''2.A'''
            j = 0
            flag_s = False
            a_cur, b_cur = M[0]
            while not flag_s:
                j += 1
                for s_cand in '''Complete the missing line''':
                    payload = (c0 * gmpy2.powmod(s_cand, e, n)) % n
                    if communicate_with_server(payload) == "Valid":
                        flag_s = True
                        si = s_cand
                        break

        #Part 2.B & 2.C are the identical to the basic version, thus aren't part of the CTF.
        elif len(M) > 1:
            '''2.B'''
            si += 1
            payload = (c0 * gmpy2.powmod(si, e, n)) % n
            while communicate_with_server(payload) == "Invalid":
                si += 1
                payload = (c0 * gmpy2.powmod(si, e, n)) % n
        else:
            '''2.C'''
            s_nxt = -1
            flag = False
            a_cur, b_cur = M[0]
            ri = ceil(2 * (b_cur * si - 2 * B), n)
            while not flag:
                lower_bound = ceil((2 * B + ri * n), b_cur)
                upper_bound = floor((3 * B + ri * n), a_cur)
                for s_cand in range(lower_bound, upper_bound + 1):
                    payload = (c0 * gmpy2.powmod(s_cand, e, n)) % n
                    if communicate_with_server(payload) == "Valid":
                        s_nxt = s_cand
                        flag = True
                        break
                ri += 1
            si = s_nxt

        '''STEP 3:'''
        # Needs extra carefulness as some ranges may overlap?
        M_nxt = []
        for tup in M:
            a_cur, b_cur = tup

            lower_bound = ceil((a_cur * si - 3 * B + 1), n)
            upper_bound = floor((b_cur * si - 2 * B), n)

            for r_cur in range(lower_bound, upper_bound + 1):
                l_range = max(a_cur, ceil((2 * B + r_cur * n), si))
                r_range = min(b_cur, floor((3 * B - 1 + r_cur * n), si))
                if l_range > r_range:
                    continue

                range_cur = (l_range, r_range)

                # Dealing with overlaps:
                # Worth mentioning it's possible to do this operation in O(nlogn),
                # but a the number of ranges is quite small, so it's fine either way

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

        M = M_nxt
        print(f"M size : {len(M)}")
        print(f"M is: : {M}")

    '''STEP 4:'''
    #Now we have the integer value of the padded message. back to bytes and depadding:

    m = M[0][0]
    original_message_padded = m.to_bytes(128,'big')
    original_message = PCKS_unpadding(original_message_padded)
    print(f"Original messsage retrieved : {original_message.decode()}")
    print(f"Number of oracle calls : {queries}")

start_attacking()