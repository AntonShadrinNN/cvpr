import random


def crossover(chr_1, chr_2):
    point_1 = random.randint(1, len(chr_1))
    point_2 = random.randint(1, len(chr_1) - 1)

    if point_2 >= point_1:
        point_2 += 1

    else:
        point_1, point_2 = point_2, point_1

    chr_1[point_1:point_2], chr_2[point_1:point_2] = \
        chr_2[point_1:point_2], chr_1[point_1:point_2]

    return chr_1, chr_2
