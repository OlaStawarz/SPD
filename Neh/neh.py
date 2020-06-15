from copy import deepcopy
import sys
import random
import math
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


def select_1(pi):
    calculate(pi)
    m = parametry[1] - 1
    j = len(pi) - 1
    suma_tab = []
    suma_tab.append([pi[j][m], j])
    flag = True
    while flag:
        if C[m - 1][j] > C[m][j - 1]:
            suma_tab.append([pi[j][m-1], j])
            m -= 1
        else:
            suma_tab.append([pi[j-1][m], j])
            j -= 1
        if j == 0:
            for i in range(0, m):
                suma_tab.append([pi[j][i], j])
            flag = False
        if m == 0:
            for i in range(0, j):
                el = [pi[i][m], i]
                suma_tab.append(el)
            flag = False
    max_val = max(suma_tab)
    max_idx = max_val[1]
    usuniete = pi[max_idx]
    pi.remove(usuniete)
    return usuniete


def select_3(pi):
    calculate(pi)
    m = parametry[1] - 1
    j = len(pi) - 1
    suma = 1
    suma_tab = []
    flag = True
    while flag:
        if C[m - 1][j] > C[m][j - 1]:
            suma += 1
            m -= 1
        else:
            el = [suma, j]
            suma_tab.append(el)
            suma = 1
            j -= 1
        if j == 0:
            for i in range(0, m):
                suma += 1
            flag = False
            el = [suma, j]
            suma_tab.append(el)
        if m == 0:
            el = [suma, j]
            suma_tab.append(el)
            suma = 1
            for i in range(0, j):
                el = [1, i]
                suma_tab.append(el)
            flag = False
    max_val = max(suma_tab)
    max_idx = max_val[1]
    usuniete = pi[max_idx]
    pi.remove(usuniete)
    return usuniete


def select_2(pi):
    calculate(pi)
    m = parametry[1] - 1
    j = len(pi) - 1
    suma = C[m][j]
    suma_tab = []
    flag = True
    while flag:
        if C[m-1][j] > C[m][j-1]:
            suma += C[m - 1][j]
            m -= 1
        else:
            el = [suma, j]
            suma_tab.append(el)
            suma = C[m][j - 1]
            j -= 1
        if j == 0:
            for i in range(0, m):
                suma += C[i][j]
            flag = False
            el = [suma, j]
            suma_tab.append(el)
        if m == 0:
            el = [suma, j]
            suma_tab.append(el)
            suma = 0
            for i in range(0, j):
                el = [C[m][i], i]
                suma_tab.append(el)
            flag = False
    max_val = max(suma_tab)
    max_idx = max_val[1]
    usuniete = pi[max_idx]
    pi.remove(usuniete)
    return usuniete


def select_4(pi):
    c_max_pom = sys.maxsize
    usuniete = []
    for j in range(0, len(pi)-1):
        zadanie = pi[j]
        pi.remove(zadanie)
        c_max = calculate(pi)
        if c_max < c_max_pom:
            c_max_pom = c_max
            usuniete = zadanie
        pi.insert(j, zadanie)
    pi.remove(usuniete)
    return usuniete


def NEH_PLUS(data, choice):
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
        if len(pi) > 1:
            if choice == 1:
                x = select_1(pi)
            elif choice == 2:
                x = select_2(pi)
            elif choice == 3:
                x = select_3(pi)
            else:
                x = select_4(pi)
            l = 0
            for l in range(l, k):
                pi.insert(l, x)
                c = calculate(pi)
                if c < c_max:
                    c_max = c
                    new_pi = pi.copy()
                pi.remove(x)
                l += 1
            pi = new_pi.copy()
        k += 1
        if len(W) == 0:
            return new_pi
    return -1


nazwa, parametry, data = czytaj('ta021.txt')
N = deepcopy(data)
print(calculate(NEH(data)))
print(calculate(NEH_PLUS(data, 1)))








