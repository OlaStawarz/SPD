import itertools
import sys


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



def calculate(data, parametry):
    S = []
    C = []
    czas_z = 0
    czas_r_tab = []
    czas_z_tab = []
    for m in range(0, parametry[1]):
        for j in range(0, parametry[0]):
            if m == 0:
                czas_r = czas_z
                czas_z = czas_r + data[j][m]
            else:
                if j == 0:
                    czas_r = C[m-1][j]
                    czas_z = czas_r + data[j][m]
                else:
                    czas_r = max(C[m-1][j], czas_z)
                    czas_z = czas_r + data[j][m]
            czas_r_tab.append(czas_r)
            czas_z_tab.append(czas_z)
        S.append(czas_r_tab)
        C.append(czas_z_tab)
        czas_r_tab = []
        czas_z_tab = []
    return C.pop().pop()


def licz_kombinacje_iteracyjnie(data, parametry):
    comb = itertools.permutations(data, len(data))
    C_wynik = sys.maxsize
    for i in comb:
        wynik = calculate(i, parametry)
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
            l = l+1
        else:
            pi[k] = min_val
            k = k - 1
        data.remove(min_val)
    return pi


def main():
    parametry, data = czytaj('data001.txt')
    pi = johnson(data, parametry)
    print(calculate(pi, parametry))
    #licz_kombinacje_iteracyjnie(data, parametry)


if __name__ == '__main__':
    main()

