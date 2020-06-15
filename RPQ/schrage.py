def czytaj(filepath):
    data = []
    with open(filepath) as f:
        n, kolumny = [int(x) for x in next(f).split()]
        data = [[int(x) for x in line.split()] for line in f]
    return n, data


def sortujR(data):
    posortowane = data.copy()
    posortowane.sort(key=lambda x: x[0])
    return posortowane


def find_maxq_and_p(data):
    max = 0
    el = []
    p = 0
    for i in range(0, len(data)):
        if data[i][2] > max:
            max = data[i][2]
            el = data[i]
            p = data[i][1]
    return max, el, p


def funkcjaStrat(data):
    max_time_q = sum(data[0])  # bieżący czas dostarczenia zadania
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
        C.append(max_time_q)
    return C


def schrage(data):
    pi = []
    n, N = czytaj(data)  # wczytuje dane z pliku
    k = 1
    G = []
    sorted = sortujR(N)
    min_r = sorted[0][0]
    time = sorted[0][0]
    while len(N) != 0 or len(G) != 0:
        while len(N) != 0 and (min_r <= time):
            el = sorted[0]
            G.append(el)  # dodaję element do G
            N.remove(el)  # usuwam element z N
            sorted.remove(el)
            if (len(sorted) != 0):
                min_r = sorted[0][0]
        if len(G) != 0:
            max_q, el_2, p = find_maxq_and_p(G)  # wyszukuję największy czas q
            G.remove(el_2)  # usuwam ten element z G
            time += p  # do czasu rozpoczęcia dodaję czas wykonania
            k += 1
            pi.append(el_2)
        else:
            time = sorted[0][0]
    return pi


def schrage_pmtn(data):
    n, N = czytaj(data)  # wczytuje dane z pliku
    # k = 1
    G = []
    sorted = sortujR(N)
    min_r = sorted[0][0]
    time = 0  # pobieram najmniejszy czas r (korzystam z sortowania po R)
    C_max = 0
    el_l = [0, 0, 1000000]
    while len(N) != 0 or len(G) != 0:
        while len(N) != 0 and min_r <= time:
            el = sorted[0]
            G.append(el)  # dodaję element do G
            N.remove(el)  # usuwam element z N
            sorted.remove(el)
            if (len(sorted) != 0):
                min_r = sorted[0][0]
            if el[2] > el_l[2]:
                el_l[1] = time - el[0]
                time = el[0]
                if el_l[1] > 0:
                    G.append(el_l)
        if len(G) == 0:
            time = sorted[0][0]
        else:
            max_q, el_2, p = find_maxq_and_p(G)  # wyszukuję największy czas q
            G.remove(el_2)  # usuwam ten element z G
            el_l = el_2
            time += p  # do czasu rozpoczęcia dodaję czas wykonania
            C_max = max(C_max, time + max_q)
    return C_max  # C_max dla liczenia C_max

def main():
    wyniki_schrage = []
    wyniki_schrage_pmtn = []

    wyniki_schrage.append(funkcjaStrat(schrage('data10.txt')).pop())
    wyniki_schrage.append(funkcjaStrat(schrage('data20.txt')).pop())
    wyniki_schrage.append(funkcjaStrat(schrage('data50.txt')).pop())
    wyniki_schrage.append(funkcjaStrat(schrage('data100.txt')).pop())
    wyniki_schrage.append(funkcjaStrat(schrage('data200.txt')).pop())
    wyniki_schrage.append(funkcjaStrat(schrage('data500.txt')).pop())
    print(wyniki_schrage)
    wyniki_schrage_pmtn.append(schrage_pmtn('data10.txt'))
    wyniki_schrage_pmtn.append(schrage_pmtn('data20.txt'))
    wyniki_schrage_pmtn.append(schrage_pmtn('data50.txt'))
    wyniki_schrage_pmtn.append(schrage_pmtn('data100.txt'))
    wyniki_schrage_pmtn.append(schrage_pmtn('data200.txt'))
    wyniki_schrage_pmtn.append(schrage_pmtn('data500.txt'))
    print(wyniki_schrage_pmtn)

if __name__ == '__main__':
    main()
