import itertools
import sys


def czytaj(sciezka):
    with open(sciezka) as f:
        n = f.readline()
        wyjscie = [[int(x) for x in line.split()] for line in f]
    return wyjscie


def sortujD(data):
    posortowane = data.copy()
    posortowane.sort(key=lambda x: x[2])
    return posortowane


def funkcjeCelu(data):
    S = []
    C = []
    T = []
    F = []
    S.append(0)
    el = 0
    for i in range(0, len(data) - 1):
        el += data[i][0]
        S.append(el)
    el = 0
    for i in range(0, len(data)):
        el += data[i][0]
        C.append(el)
    for i in range(0, len(C)):
        if C[i] > data[i][2]:
            T.append(C[i] - data[i][2])
        else:
            T.append(0)
    F_wynik = 0
    for i in range(0, len(C)):
        F.append(T[i] * data[i][1])
        F_wynik += F[i]
    return F_wynik


def licz_kombinacje(data):
    comb = itertools.permutations(data, len(data))
    F_wynik = sys.maxsize
    for i in comb:
        if funkcjeCelu(i) < F_wynik:
            F_wynik = funkcjeCelu(i)
    return F_wynik


def licz_kombinacje_rekursywnie(data):
    pom = data.copy()
    F_wynik = sys.maxsize
    if len(pom) == len(data):
        F_wynik2 = funkcjeCelu(pom)
        if F_wynik2 < F_wynik:
            F_wynik = F_wynik2
    for z in data:
        temp = pom + z
        licz_kombinacje_rekursywnie(temp)
    return F_wynik


def main():
    print(funkcjeCelu(sortujD(czytaj('data10.txt'))))
    print(licz_kombinacje(czytaj('data10.txt')))


if __name__ == '__main__':
    main()


