from utils import *
import copy
from math import sqrt
def solve(B_value:list,candidate_lib:list,curDay:int):
    def cmp(lib1,lib2):
        value1=0
        if curDay+T[lib1]<D:
            value1=sum_value[lib1]
        value2=0
        if curDay+T[lib2]<D:
            value2=sum_value[lib2]
        return value1/T[lib1]-value2/T[lib2]

    orderedLib=[]
    shippedBooks=[]
    B_valueCur=copy.deepcopy(B_value)

    sum_value={}
    for lib in candidate_lib:
        value=0
        for book in N[lib]:
            value+=B_valueCur[book]
        sum_value[lib]=value

    #iteration begans
    while curDay<=D:
        # get the best lib
        bubbleSortReversed(candidate_lib,cmp,1)
        curLib=candidate_lib[0]
        candidate_lib=candidate_lib[1:]
        if curDay+T[curLib]<D:
            for book in N[curLib]:
                if B_valueCur[book]!=0:
                    for lib in book_dic[book]:
                        sum_value[lib]-=B_valueCur[book]
                    B_valueCur[book]=0

            curDay+=T[curLib]
            orderedLib.append(curLib)
            shippedBooks+=[N[curLib]]
            # print(T[curLib])
        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            break
    print(curDay)
    return orderedLib,shippedBooks

def grid_search(n,m):
    pass

if __name__ == "__main__":
    input=parseINPUT("c_incunabula.txt")
    B,L,D,B_value,N,T,M,N_n=input.values()
    book_dic={}
    for i in range(L):
        for book in N[i]:
            if book in book_dic:
                book_dic[book].append(i)
            else:
                book_dic[book]=[i]
    orderedLib,shippedBooks=solve(B_value,[i for i in range(L)],0)
    submission=generateSubmission(orderedLib,shippedBooks)
    print(judgeFunction(submission,B_value))
    # # write submission to file.
    # with open("c_answer.txt","w") as f:
    #     f.write(submission)