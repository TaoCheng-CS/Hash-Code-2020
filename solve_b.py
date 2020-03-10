from utils import parseINPUT, judgeFunction, generateSubmission


def cmp_function(book):
    return T[book]


input = parseINPUT("b_read_on.txt")
B, L, D, B_value, N, T, M, N_n = input.values()
orderedLib = []
shippedBooks = []

# sort by the number of sign up days
orderBYsignup = [i for i in range(L)]
orderBYsignup.sort(key=cmp_function)

# iteration
curDay = 0
while curDay <= D:
    # get the best lib
    curLib = orderBYsignup[0]
    orderBYsignup = orderBYsignup[1:]
    if curDay + T[curLib] <= D:
        curDay += T[curLib]
        orderedLib.append(curLib)
        sumBooks = min((D - curDay) * M[curLib], N_n[curLib])
        shippedBooks += [N[curLib][:sumBooks]]
    else:
        break
print("cur day %d" % curDay)

submission = generateSubmission(orderedLib, shippedBooks)
# show score of the submission.
print(judgeFunction(submission, input["valueOFbook"]))

# write submission to file.
with open("b_answer.txt", "w") as f:
    f.write(submission)
