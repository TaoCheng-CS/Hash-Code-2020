from utils import parseINPUT
from utils import generateSubmission, judgeFunction
from utils import bubbleSortReversedByvalue
import copy
import numpy as np

consider_range = 2

np.random.seed(0)
max_prob = 0.65


def solve(B_value: list, sum_value: dict, candidate_lib: list, curDay: int):
    def average_value(lib):
        if curDay + T[lib] < D:
            return sum_valueCur[lib] / T[lib]
        else:
            return 0

    def reduce_sum_value(sumvalue_list, choosed_lib, B_valueList):
        for book in N[choosed_lib]:
            if B_valueList[book] != 0:
                for lib in book_dic[book]:
                    sumvalue_list[lib] -= B_valueList[book]
                B_valueList[book] = 0

    orderedLib = []
    shippedBooks = []

    Sum_gain = 0
    B_valueCur = copy.deepcopy(B_value)
    sum_valueCur = copy.deepcopy(sum_value)

    # iteration begans
    while curDay < D:
        # get the best lib
        value = list(map(average_value, candidate_lib))
        # bubbleSortReversed(candidate_lib, cmp, consider_range)
        curLib = -1
        gain = 0
        bubbleSortReversedByvalue(candidate_lib, value, consider_range)
        prob = np.random.rand(1)

        if prob < max_prob:
            choose_index = 1
        else:
            choose_index = 0

        curLib = candidate_lib[choose_index]
        if curDay + T[curLib] < D:
            gain = sum_valueCur[curLib]
        else:
            gain = 0

        Sum_gain += gain
        candidate_lib.remove(curLib)
        reduce_sum_value(sum_valueCur, curLib, B_valueCur)
        curDay += T[curLib]
        if curDay < D:
            shippedBooks += [N[curLib]]
            orderedLib.append(curLib)
    return orderedLib, shippedBooks, Sum_gain


if __name__ == "__main__":

    input = parseINPUT("c_incunabula.txt")
    B, L, D, B_value, N, T, M, N_n = input.values()
    book_dic = {}
    for i in range(L):
        for book in N[i]:
            if book in book_dic:
                book_dic[book].append(i)
            else:
                book_dic[book] = [i]

    sumValue = {}
    B_valueCur = copy.deepcopy(B_value)
    for lib in range(L):
        value = 0
        for book in N[lib]:
            B_valueCur[book] = B_value[book]
            value += B_valueCur[book]
        sumValue[lib] = value

    orderedLib, shippedBooks, Sum_gain = solve(B_valueCur, sumValue,
                                               [i for i in range(L)], 0)
    submission = generateSubmission(orderedLib, shippedBooks)
    print(Sum_gain)
    print(judgeFunction(submission, B_value))
    # # write submission to file.
    # with open(
    #         "c_answer_est_method_considerrange_%d_threshday_%d.txt" %
    #     (consider_range, thresh_day), "w") as f:
    #     f.write(submission)
