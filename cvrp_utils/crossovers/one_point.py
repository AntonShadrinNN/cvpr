import random


def crossover(chr_1: list, chr_2: list):
    point = random.randint(1, len(chr_1) - 1)
    chr_1[point:], chr_2[point:] = chr_2[point:], chr_1[point:]

    return chr_1, chr_2
