import argparse
import random
import numpy as np
import math
import time

distance_list = []
best_dna = []
best_dis = math.inf
mutate_p = 0.05
good_p = 0.3
c_num = 1


def total_dis_cal(dna):
    total_dis = 0
    for i in range(0, len(dna)-1):
        if dna[i] < dna[i+1]:
            total_dis += distance_list[dna[i+1]][dna[i]]
        else:
            total_dis += distance_list[dna[i]][dna[i+1]]
    if dna[-1] < dna[0]:
        total_dis += distance_list[dna[0]][dna[-1]]
    else:
        total_dis += distance_list[dna[-1]][dna[0]]

    return total_dis


def score_cal(total_dis_list):
    fit_list = []
    tail = min(total_dis_list)
    tail = tail / 1.2

    for i in range(0, len(total_dis_list)):
        fit_list.append(100/(total_dis_list[i] - tail))

    entire_fit = 0
    for i in range(0, len(fit_list)):
        entire_fit += fit_list[i]

    score_list = []
    for i in range(0, len(fit_list)):
        score_list.append(fit_list[i]/entire_fit)
    return score_list


def crossover(dna_1, dna_2):
    new = []
    p = len(dna_1)
    list_i = []

    for i in range(0, c_num * 2):
        list_i.append(int(random.random() * p))
    list_i.sort()
    for i in range(0, c_num):
        new.extend(dna_1[list_i[2 * i]:list_i[2 * i + 1]])

    for i in range(0, p):
        if dna_2[i] not in new:
            new.append(dna_2[i])
    return new


def mutate(dna):
    mp = mutate_p
    while random.random() < mp:
        for i in range(0, int(len(dna)/4)):
            p = len(dna)
            i_1 = int(random.random() * p)
            i_2 = int(random.random() * p)

            g_1 = dna[i_1]
            g_2 = dna[i_2]

            dna[i_1] = g_2
            dna[i_2] = g_1

    return dna


def generation(dna_list):
    global best_dis, best_dna

    # calculate entire distance of dna
    total_dis_list = []
    ppl = len(dna_list)
    new_best_dis = math.inf
    new_best_dna_index =0

    for i in range(0, ppl):
        new_dis = total_dis_cal(dna_list[i])
        total_dis_list.append(new_dis)
        if new_dis < new_best_dis:
            new_best_dis = new_dis
            new_best_dna_index = i

    # calculate score
    score_list = score_cal(total_dis_list)

    if new_best_dis < best_dis:
        best_dis = new_best_dis
        best_dna = dna_list[new_best_dna_index]
    print(best_dis)

    # make sorted dna list
    good_num = int(ppl * good_p)
    dic_list = []
    sorted_dna_list = []

    for i in range(0, ppl):
        dic_list.append((dna_list[i], total_dis_list[i]))
    dic_list = sorted(dic_list, key=lambda dna: dna[1])

    for i in range(0, good_num):
        sorted_dna_list.append(dic_list[i][0])

    # cross over and make new generation
    next_dna_list = sorted_dna_list

    for i in range(0, ppl-good_num):
        choice = np.random.choice(ppl, 2, score_list)
        one, two = dna_list[choice[0]], dna_list[choice[1]]
        new = crossover(one, two)
        next_dna_list.append(mutate(new))

    return next_dna_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=30,
                        help="set population")
    parser.add_argument('-f', type=int, default=1000,
                        help="set fitness number")
    parser.add_argument('file', type=str,
                        help="input file name")
    args = parser.parse_args()

    # init global
    global distance_list

    # population
    ppl = args.p

    # fitness number
    fn = args.f
    file_name = args.file

    # start reading
    file = open(file_name, 'r')
    lines = file.readlines()

    # parsing
    read_file_name = lines[0].strip().split()[-1]

    if file_name[:-4] != read_file_name:
        print("file name is not correct")
        return

    dimension = int(lines[3].strip().split()[-1])
    file_type = lines[4].strip().split()[-1]

    if file_type != "EUC_2D":
        print("file type is not EUC_2D")
        return

    point_list = []
    for i in range(6, dimension+6):
        temp = lines[i].strip().split()
        point_list.append((float(temp[-2]), float(temp[-1])))

    start = time.time()
    print("start : 0")

    # distance_list = [] is global
    for i in range(0, dimension):
        t_list = []
        p1 = point_list[i]
        for j in range(0, i):
            p2 = point_list[j]
            distance = ((p2[0]-p1[0]) ** 2 + (p2[1]-p1[1]) ** 2) ** 0.5
            t_list.append(distance)
        t_list.append(0)
        distance_list.append(t_list)

    nowT = time.time() - start
    print("complete cal distance list : ", nowT)

    dna_list = []   # dna list first making
    for i in range(0, ppl):
        dna = list(range(0, dimension))
        random.shuffle(dna)
        dna_list.append(dna)

    nowT = time.time() - start
    print("complete cal dna list : ", nowT)

    for i in range(0, fn):
        dna_list = generation(dna_list)
        nowT = time.time() - start
        print("complete " + str(i) + "th generation : ", nowT)

    print(best_dis)



if __name__ == "__main__":
    main()
