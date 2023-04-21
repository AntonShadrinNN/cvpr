import random


def crossover(chr_1, chr_2):

    size = len(chr_1)
    pos_ind_1 = [0] * size
    pos_ind_2 = [0] * size

    for i in range(size):
        pos_ind_1[chr_1[i] - 1] = i
        pos_ind_2[chr_2[i] - 1] = i

    point_1 = random.randint(0, size)
    point_2 = random.randint(0, size - 1)

    if point_2 >= point_1:
        point_2 += 1

    else:
        point_1, point_2 = point_2, point_1

    for i in range(point_1, point_2):
        temp_1, temp_2 = chr_1[i], chr_2[i]

        chr_1[i], chr_1[pos_ind_1[temp_2]] = temp_2, temp_1
        chr_2[i], chr_2[pos_ind_2[temp_1]] = temp_1, temp_2

        pos_ind_1[temp_1], point_1[temp_2] = pos_ind_1[temp_2], pos_ind_1[temp_1]
        pos_ind_2[temp_1], pos_ind_2[temp_2] = pos_ind_2[temp_2], pos_ind_2[temp_1]

    return chr_1, chr_2
