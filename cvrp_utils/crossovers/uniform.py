import random


def crossover(chr_1, chr_2, prb):
    size = min(len(chr_1), len(chr_2))

    for i in range(size):
        if random.Random < prb:
            chr_1[i], chr_2[i] = chr_2[i], chr_1[i]

    return chr_1, chr_2
