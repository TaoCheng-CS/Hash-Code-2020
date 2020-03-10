from utils import parseINPUT
from utils import generateSubmission, judgeFunction
from utils import bubbleSortReversedByvalue, orderedLib2N_n
import copy
import numpy as np

consider_range = 2
sum_depth = 0
thresh_day = 0
max_prob = 0.5
np.random.seed(0)


def solve(B_value: list, sum_value: dict, candidate_lib: list, N_number: list,
          curDay: int, depth: int):
    def get_lib_value(lib):
        number = min(N_numberCur[lib], (D - curDay - T[lib]) * M[lib])
        if number >= N_numberCur[lib]:
            return sum_valueCur[lib]
        else:
            sum = 0
            time = 0
            for book in N[lib]:
                if time >= number:
                    break
                if B_valueCur[book] != 0:
                    time += 1
                    sum += B_valueCur[book]
            return sum

    def average_value(lib):
        return get_lib_value(lib) / T[lib]

    def reduce_sum_value(sumvalue_list, choosed_lib, B_valueList,
                         N_numberlist):
        number = min(N_numberCur[choosed_lib],
                     (D - curDay - T[choosed_lib]) * M[choosed_lib])
        time = 0
        for book in N[choosed_lib]:
            if time >= number:
                break
            if B_valueList[book] != 0:
                time += 1
                for lib in book_dic[book]:
                    sumvalue_list[lib] -= B_valueList[book]
                    N_numberlist[lib] -= 1
                B_valueList[book] = 0

    orderedLib = []

    Sum_gain = 0
    B_valueCur = copy.deepcopy(B_value)
    sum_valueCur = copy.deepcopy(sum_value)
    N_numberCur = copy.deepcopy(N_number)

    # iteration begans
    while curDay < D:
        # get the best lib
        value = list(map(average_value, candidate_lib))
        # bubbleSortReversed(candidate_lib, cmp, consider_range)
        curLib = -1
        gain = 0
        if depth >= 1 and curDay >= thresh_day:
            bubbleSortReversedByvalue(candidate_lib, value, consider_range)
            max_value = 0
            for i in range(consider_range):
                lib = candidate_lib[i]
                temp_B_value = copy.deepcopy(B_valueCur)
                temp_sum_value = copy.deepcopy(sum_valueCur)
                temp_candidate_lib = copy.deepcopy(candidate_lib)
                temp_N_number = copy.deepcopy(N_numberCur)
                curgain = int(value[i] * T[lib])

                temp_candidate_lib.remove(lib)
                reduce_sum_value(temp_sum_value, lib, temp_B_value,
                                 temp_N_number)
                _, est_gain = solve(temp_B_value, temp_sum_value,
                                    temp_candidate_lib, temp_N_number,
                                    curDay + T[lib], depth - 1)
                est_sumgain = curgain + est_gain
                if est_sumgain >= max_value:
                    max_value = est_sumgain
                    curLib = lib
                    gain = curgain
                if max_value + Sum_gain > 5348248:
                    print("ahahahah")
                    print(max_value + Sum_gain)
        else:
            bubbleSortReversedByvalue(candidate_lib, value, consider_range)
            prob = np.random.rand(1)
            if prob < max_prob:
                choose_index = 1
            else:
                choose_index = 0

            curLib = candidate_lib[choose_index]
            gain = int(value[choose_index] * T[curLib])

        reduce_sum_value(sum_valueCur, curLib, B_valueCur, N_numberCur)
        Sum_gain += gain
        candidate_lib.remove(curLib)
        # if depth == sum_depth:
        #     print(("curDay : %d") % curDay)
        curDay += T[curLib]
        if curDay < D:
            orderedLib.append(curLib)
    return orderedLib, Sum_gain


if __name__ == "__main__":

    def sortedByvalue(book):
        return B_value[book]

    input = parseINPUT("f_libraries_of_the_world.txt")
    B, L, D, B_value, N, T, M, N_n = input.values()
    book_dic = {}
    for i in range(L):
        for book in N[i]:
            if book in book_dic:
                book_dic[book].append(i)
            else:
                book_dic[book] = [i]

    sumValue = {}
    for lib in range(L):
        value = 0
        for book in N[lib]:
            value += B_value[book]
        sumValue[lib] = value

    for lib in N:
        lib.sort(key=sortedByvalue, reverse=True)

    max_prob = 0
    orderedLib, Sum_gain = solve(B_value, sumValue, [i for i in range(L)], N_n,
                                 0, sum_depth)

    shippedBooks = orderedLib2N_n(orderedLib, B_value, T, M, N_n, N, D)
    submission = generateSubmission(orderedLib, shippedBooks)
    print(Sum_gain)
    print(judgeFunction(submission, B_value))
    # # write submission to file.
    # with open(
    #         "f_answer_est_range_%d_depth_%d_threshday_%d.txt" %
    #     (consider_range, sum_depth, thresh_day), "w") as f:
    #     f.write(submission)