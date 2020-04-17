def czytaj(sciezka):
    with open(sciezka) as f:
        n, kolumny = [int(x) for x in next(f).split()]
        data = [[int(x) for x in line.split()] for line in f]
    return n, data


def modifyBit(n, p, b):
    mask = 1 << p
    return (n & ~mask) | ((b << p) & mask)


def decimalToBinary(num):
    return bin(num).replace("0b", "")


def binaryToDecimal(num):
    return int(num, 2)


def PD_rekurencyjny(I, d, F):
    bin = decimalToBinary(I)
    max_val_tab = []
    for j in range(0, len(bin)):
        modified = modifyBit(I, j, 0)
        modified_binary = decimalToBinary(modified)
        reversedstring = ''.join(reversed(bin))
        p = [pos for pos, char in enumerate(reversedstring) if char == '1']
        if bin != modified_binary:
            ile = 0
            for m in range(0, len(p)):
                ile += d[p[m]][0]
            current_F = F[modified]
            if current_F == -1:
                current_F = PD_rekurencyjny(modified, d, F)
            max_val = max(ile - d[j][2], 0) * d[j][1] + current_F
            max_val_tab.append(max_val)
    min_val = min(max_val_tab)
    F[I] = min_val
    return min_val


def PD_itreacyjny(n, d):
    F = []
    max_val_tab = []

    F.append(max(d[0][0] - d[0][2], 0) * d[0][1])
    for i in range(1, 2 ** n):
        bin = decimalToBinary(i)
        for j in range(0, len(bin)):
            modified = modifyBit(i, j, 0)
            modified_binary = decimalToBinary(modified)
            reversedstring = ''.join(reversed(bin))
            p = [pos for pos, char in enumerate(reversedstring) if char == '1']
            if bin != modified_binary:
                ile = 0
                for m in range(0, len(p)):
                    ile += d[p[m]][0]
                max_val = max(ile - d[j][2], 0) * d[j][1] + F[modified]
                max_val_tab.append(max_val)
        min_val = min(max_val_tab)
        F.append(min_val)
        max_val_tab = []
    return F.pop()


def main():
    iteracyjne = []
    rekurencyjne = []
    pliki = ['data10.txt', 'data11.txt', 'data12.txt', 'data13.txt', 'data14.txt', 'data15.txt']
    #pliki = ['data10.txt', 'data11.txt', 'data12.txt', 'data13.txt', 'data14.txt', 'data15.txt', 'data16.txt', 'data17.txt', 'data18.txt', 'data19.txt', 'data20.txt']

    for f in pliki:
        n, d = czytaj(f)
        iteracyjne.append(PD_itreacyjny(n, d))
        F = [0]
        for i in range(0, 2 ** n - 1):
            F.append(-1)
        I = 2 ** n - 1
        PD_rekurencyjny(I, d, F)
        rekurencyjne.append(F.pop())
    print(iteracyjne)
    print(rekurencyjne)

if __name__ == '__main__':
    main()


