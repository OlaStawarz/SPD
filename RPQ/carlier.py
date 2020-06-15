import sys
from heapq import heappush, heapify, nlargest, heappop
from copy import copy, deepcopy

new_pi = 0
LB = 0
UB = sys.maxsize


def read(filepath):
    with open(filepath) as f:
        n, columns = [int(x) for x in next(f).split()]
        data = [[int(x) for x in line.split()] for line in f]
    return data


def sortR(tab):
    data = tab.copy()
    order_by_access_time = data.copy()
    order_by_access_time.sort(key=lambda x: x[0])
    return order_by_access_time


def loss_function(tab):
    data = tab.copy()
    max_time_q = data[0][0] + data[0][1] + data[0][2]
    time = data[0][0] + data[0][1]
    C = []
    C.append(time)
    for t in range(1, len(data)):
        if time > data[t][0]:
            time = time + data[t][1]
        else:
            time = data[t][0] + data[t][1]
        time_q = data[t][2] + time
        max_time_q = max(max_time_q, time_q)
        if max_time_q in C:
            C.append(time_q)
        else:
            C.append(max_time_q)
    return C


def find_max_C(data):
    max_C = data[0]
    for i in range(0, len(data)):
        if data[i] > max_C:
            max_C = data[i]
    return max_C


def find_max_q_and_p(data):
    max = 0
    el = []
    p = 0
    for i in range(0, len(data)):
        if data[i][2] > max:
            max = data[i][2]
            el = data[i]
            p = data[i][1]
    return max, el, p


def heap(data):
    q = [(x[2], x) for x in data]
    heapify(q)
    max = nlargest(1, q)
    max_q = max[0][0]
    max_el = max[0][1]
    p = max[0][1][1]
    return max_q, max_el, p


def schrage(tab):
    N = tab.copy()
    pi = []
    k = 1
    G = []
    sorted = sortR(N)
    min_r = sorted[0][0]
    time = sorted[0][0]
    while len(N) != 0 or len(G) != 0:
        while len(N) != 0 and (min_r <= time):
            el = sorted[0]
            G.append(el)
            N.remove(el)
            sorted.remove(el)
            if len(sorted) != 0:
                min_r = sorted[0][0]
        if len(G) != 0:
            max_q, el_2, p = find_max_q_and_p(G)
            G.remove(el_2)  # usuwam ten element z G
            time += p  # do czasu rozpoczęcia dodaję czas wykonania
            k += 1
            pi.append(el_2)
        else:
            time = sorted[0][0]
    return pi

def schrage_pmtn(tab):
    N = deepcopy(tab)
    G = []
    sorted = sortR(N)
    min_r = sorted[0][0]
    time = 0
    C_max = 0
    el_l = [0, 0, 1000000]
    while len(N) != 0 or len(G) != 0:
        while len(N) != 0 and min_r <= time:
            el = sorted[0]
            G.append(el)
            N.remove(el)
            sorted.remove(el)
            if len(sorted) != 0:
                min_r = sorted[0][0]
            if el[2] > el_l[2]:
                el_l[1] = time - el[0]
                time = el[0]
                if el_l[1] > 0:
                    G.append(el_l)
        if len(G) == 0:
            time = sorted[0][0]
        else:
            max_q, el_2, p = find_max_q_and_p(G)
            G.remove(el_2)
            el_l = el_2
            time += p
            C_max = max(C_max, time + max_q)
    return C_max, tab


def find_max_b(data_b, C_max):
    for i in range(len(data_b) - 1, 0, -1):
        if data_b[i] == C_max:
            return data_b.index(data_b[i])


def find_min_a(data, C_max, b):
    sum_p = 0
    for i in range(0, len(data)):
        for j in range(i, b + 1):
            sum_p += data[j][1]
        r = data[i][0]
        q = data[b][2]
        C_max_pom = data[i][0] + sum_p + data[b][2]
        if C_max_pom == C_max:
            return i
        sum_p = 0


def find_max_c(data, a, b):
    for i in range(b, a - 1, -1):
        if data[i][2] < data[b][2]:
            return i


def find_new_rpq(c, b, data):
    new_p = 0
    new_r = sys.maxsize
    # min_q = sys.maxsize
    new_q = sys.maxsize
    for i in range(c + 1, b + 1):
        if data[i][0] < new_r:
            new_r = data[i][0]
        if data[i][2] < new_q:
            new_q = data[i][2]
        new_p += data[i][1]
    return new_r, new_p, new_q


def carlier(array):
    array_schrage = schrage(array.copy())
    array_loss = loss_function(array_schrage)
    U = find_max_C(array_loss)
    old_pi = find_max_C(array_loss)
    C_max = find_max_C(array_loss)
    global UB
    global new_pi
    if U < UB:
        UB = U
        new_pi = old_pi
    b = find_max_b(array_loss, C_max)
    a = find_min_a(array_schrage, C_max, b)
    c = find_max_c(array_schrage, a, b)
    if c is None:
        return new_pi
    new_r, new_p, new_q = find_new_rpq(c, b, array_schrage)
    r_c = array_schrage[c][0]
    array_schrage[c][0] = max(array_schrage[c][0], new_r + new_p)
    global LB
    LB, original_schrage = schrage_pmtn(array_schrage)
    if LB < UB:
        carlier(original_schrage)
    original_schrage[c][2] = r_c
    q_c = original_schrage[c][2]
    original_schrage[c][2] = max(original_schrage[c][2], new_q + new_p)
    LB, more_original_schrage = schrage_pmtn(original_schrage)
    if LB < UB:
        carlier(more_original_schrage)
    more_original_schrage[c][2] = q_c
    return new_pi


print(carlier(read('data10.txt')))