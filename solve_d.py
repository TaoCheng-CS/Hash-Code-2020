from utils import parseINPUT, orderedLib2N_n
from utils import generateSubmission, judgeFunction
from utils import bubbleSortReversedBydict
import copy
import numpy as np

consider_range = 1


def solve(B_value: list, candidate_lib: list, curDay: int):

    # iteration
    curDay = 0
    N_n_copy = copy.deepcopy(N_n)
    book_dicCur = copy.deepcopy(book_dic)
    orderedLib = []
    values = {}
    for lib in candidate_lib:
        values[lib] = N_n_copy[lib]

    while curDay <= D:
        # get the best lib
        bubbleSortReversedBydict(candidate_lib, values, consider_range)
        curLib = candidate_lib[0]
        candidate_lib = candidate_lib[1:]

        if curDay + T[curLib] < D:
            curDay += T[curLib]
            orderedLib.append(curLib)
            for book in N[curLib]:
                if book_dicCur[book] != -1:
                    for lib in book_dicCur[book]:
                        values[lib] -= 1
                    book_dicCur[book] = -1
        else:
            if curDay + T[curLib] == D:
                print("Fine tunning needed for the last choice")
            break
    return orderedLib


if __name__ == "__main__":
    input = parseINPUT("d_tough_choices.txt")
    B, L, D, B_value, N, T, M, N_n = input.values()
    book_dic = {}
    for i in range(L):
        for book in N[i]:
            if book in book_dic:
                book_dic[book].append(i)
            else:
                book_dic[book] = [i]

    orderedLib = solve(B_value, [i for i in range(L)], 0)
    shippedBooks = orderedLib2N_n(orderedLib, B_value, T, M, N_n, N, D)
    submission = generateSubmission(orderedLib, shippedBooks)
    print(judgeFunction(submission, B_value))

    # # write submission to file.
    # with open("d_answer.txt", "w") as f:
    #     f.write(submission)