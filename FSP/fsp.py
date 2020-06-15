import itertools
import sys
from copy import deepcopy
from timeit import default_timer as timer
import random


def czytaj(sciezka):
    data = []
    parametry = []
    with open(sciezka) as f:
        n, m = [int(x) for x in next(f).split()]
        data_pom = [[int(x) for x in line.split()] for line in f]
    for i in range(0, len(data_pom)):
        el = data_pom[i][1::2]
        data.append(el)
    parametry.append(n)
    parametry.append(m)
    return parametry, data


parametry, data = czytaj('data001.txt')
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
        for j in range(0, len(data)):
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


def licz_kombinacje_iteracyjnie(data):
    comb = itertools.permutations(data, len(data))
    C_wynik = sys.maxsize
    for i in comb:
        wynik = calculate(i)
        if wynik < C_wynik:
            C_wynik = wynik
    return C_wynik


def johnson(data, parametry):
    l = 0
    k = parametry[0] - 1
    pi = [0] * parametry[0]
    while len(data) != 0:
        min_val = min(data, key=min)
        if min_val[0] < min_val[1]:
            pi[l] = min_val
            l = l + 1
        else:
            pi[k] = min_val
            k = k - 1
        data.remove(min_val)
    return pi


def bound_1(pi):
    max_tab = []
    calculate(pi)
    for i in range(0, parametry[1]):
        sum_p = 0
        C_max = C[i][len(pi)-1]
        for j in range(0, parametry[0]):
            if data[j] not in pi:
                sum_p = sum_p + data[j][i]
        max_tab.append(C_max + sum_p)
    LB = max(max_tab)
    return LB


def bound_2(pi):
    max_tab = []
    sum_min = []
    calculate(pi)
    suma = 0
    for i in range(0, parametry[1]):
        sum_p = 0
        C_max = C[i][len(pi) - 1]
        for m in range(i, parametry[1]):
            for j in range(0, parametry[0]):
                if m != i:
                    sum_min.append(data[j][m])
                if data[j] not in pi:
                    if i == m:
                        sum_p = sum_p + data[j][m]
            if len(sum_min) != 0:
                min_val = min(sum_min)
                suma = suma + min_val
                sum_min.clear()
        max_tab.append(C_max + sum_p + suma)
        suma = 0
    LB = max(max_tab)
    return LB


def bound_3(pi):
    max_tab = []
    sum_min = []
    calculate(pi)
    suma = 0
    for i in range(0, parametry[1]):
        sum_p = 0
        C_max = C[i][len(pi) - 1]
        for m in range(i, parametry[1]):
            for j in range(0, parametry[0]):
                if data[j] not in pi:
                    if i == m:
                        sum_p = sum_p + data[j][m]
                    if i != m:
                        sum_min.append(data[j][m])
            if len(sum_min) != 0:
                min_val = min(sum_min)
                suma = suma + min_val
                sum_min.clear()
        max_tab.append(C_max + sum_p + suma)
        suma = 0
    LB = max(max_tab)
    return LB


def bound_4(pi):
    max_tab = []
    suma_tab = []
    calculate(pi)
    for i in range(0, parametry[1]):
        sum_p = 0
        C_max = C[i][len(pi)-1]
        for j in range(0, parametry[0]):
            if data[j] not in pi:
                sum_p = sum_p + data[j][i]
        suma_tab.clear()
        for k in range(0, parametry[0]):
            sum_min = 0
            if data[k] not in pi:
                for w in range(i+1, parametry[1]):
                    sum_min += data[k][w]
            if sum_min != 0:
                suma_tab.append(sum_min)
        if len(suma_tab) != 0:
            suma = min(suma_tab)
        else:
            suma = 0
        max_tab.append(C_max + sum_p + suma)
    LB = max(max_tab)
    return LB


#UB - wartość maksymalna
UB = sys.maxsize

#UB - wartość funkcji celu dla losowej permutacji
count = 0
x = deepcopy(data)
b = x[:]
random.shuffle(b)
#UB = calculate(b)


#UB - wartość funkcji celu dla 10 losowych permutacji
def losowe_UB():
    losowe = []
    najlepsze = []
    for i in range(0, 10):
        x = deepcopy(data)
        b = x[:]
        random.shuffle(b)
        losowe.append(b)
    for i in range(0, len(losowe)):
        x = calculate(losowe[i])
        najlepsze.append(x)
    return min(najlepsze)

#UB = losowe_UB()


def prodecure_BnB():
    N = deepcopy(data)
    pi = []
    for j in N:
        global UB
        UB = BnB(j, pi, N)
        global count
        count = count + 1
    print("Liczba przeszukanych węzłów: {}".format(count))
    return UB


def BnB(j, pi_copy, J):
    N = deepcopy(J)
    pi = deepcopy(pi_copy)
    pi.append(j)
    N.remove(j)
    if len(N) != 0:
        #LB = bound_1(pi)
        #LB = bound_2(pi)
        #LB = bound_3(pi)
        LB = bound_4(pi)
        global UB
        if LB < UB:
            for j in N:
                UB = BnB(j, pi, N)
                global count
                count = count + 1
    else:
        C_max = calculate(pi)
        if C_max < UB:
           UB = C_max
    return UB


def main():
    #calculate - permutacja naturalna
    #print(calculate(data))

    #algorytm Johnsona
    #pi = johnson(data, parametry)
    #print(calculate(pi))

    #BnB
    wynik = prodecure_BnB()
    print("Wynik: " + str(wynik))

    #bruteforce
    #print(licz_kombinacje_iteracyjnie(data))


if __name__ == '__main__':
    main()

