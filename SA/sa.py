from copy import deepcopy
import random
import math
import sys

def czytaj(sciezka):
    data = []
    parametry = []
    with open(sciezka) as f:
        nazwa = f.readline()
        n, m = [int(x) for x in next(f).split()]
        data_pom = [[int(x) for x in line.split()] for line in f]
    for i in range(0, len(data_pom)):
        el = data_pom[i][1::2]
        data.append(el)
    data.pop()
    parametry.append(n)
    parametry.append(m)
    return nazwa, parametry, data

W = []
S = []
C = []

def calculate(data):
    S.clear()
    C.clear()
    J = deepcopy(data)
    czas_r_tab = []
    czas_z_tab = []
    czas_z = 0
    for m in range(0, parametry[1]):
        for j in range(0, len(J)):
            if m == 0:
                czas_r = czas_z
                czas_z = czas_r + J[j][m]
            else:
                if j == 0:
                    czas_r = C[m-1][j]
                    czas_z = czas_r + J[j][m]
                else:
                    czas_r = max(C[m-1][j], czas_z)
                    czas_z = czas_r + J[j][m]
            czas_r_tab.append(czas_r)
            czas_z_tab.append(czas_z)
        S.append(czas_r_tab)
        C.append(czas_z_tab)
        czas_r_tab = []
        czas_z_tab = []
    return C[-1][-1]


def NEH(data):
    w = 0
    k = 1
    pi = []
    new_pi = []
    for j in range(0, parametry[0]):
        for m in range(0, parametry[1]):
            w += data[j][m]
        el = [w, j]
        W.append(el)
        w = 0
    W.sort()
    while W != 0:
        c_max = sys.maxsize
        idx = W[-1][1]
        new_j = N[idx]
        l = 0
        for l in range(l, k):
            pi.insert(l, new_j)
            c = calculate(pi)
            if c < c_max:
                c_max = c
                new_pi = pi.copy()
            pi.remove(new_j)
            l += 1
        pi = new_pi.copy()
        W.remove(W[-1])
        k += 1
        if len(W) == 0:
            return new_pi
    return -1


def swapPositions(list, pos1, pos2):
    l = deepcopy(list)
    first_ele = l.pop(pos1)
    second_ele = l.pop(pos2-1)
    l.insert(pos1, second_ele)
    l.insert(pos2, first_ele)
    return l


def insert(list, pos1, pos2):
    l = deepcopy(list)
    first_ele = l.pop(pos1)
    l.insert(pos2, first_ele)
    return l


def reduceTemperature(T, T0):
    return 0.97 * T

#nazwa, parametry, data = czytaj('ta003.txt')
#N = deepcopy(data)
#T0 = 100
T_end = 0.01
k = 1
e = 2.71828


def SA(data, choice_L, T0):
    T = T0
    pi = NEH(data)
    pi_prim = deepcopy(pi)
    L = choice_L
    while T > T_end:
        for w in range(k, L):
            i = random.randint(0, parametry[0]-1)
            j = random.randint(0, parametry[0]-1)
            new_pi = insert(pi, i, j-1)
            C_max = calculate(pi)
            C_max_new = calculate(new_pi)
            if C_max_new > C_max:
                r = random.random()
                delta_C_max = C_max - C_max_new
                pom = e ** (delta_C_max/T)
                if r >= pom:
                    new_pi = pi.copy()
            pi = new_pi
            if calculate(pi) < calculate(pi_prim):
                pi_prim = pi.copy()
        T = reduceTemperature(T, T0)
    return pi_prim


nazwa, parametry, data = czytaj('ta003.txt')
N = deepcopy(data)
print(calculate(SA(N, parametry[0], 100)))

