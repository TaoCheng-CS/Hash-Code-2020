from utils import *
import copy
from math import sqrt
import numpy as np
def solve(B_value:list,candidate_lib:list,curDay:int):
    def sortBybookValue(key):
        return B_valueCur[key]
    def cmp(lib):
        if curDay+T[lib]<D:
            return N_n_copy[lib]
        else: 
            return 0
        
    # B_valueCur is used to store current value of books.
    B_valueCur=copy.deepcopy(B_value)
    
    #iteration
    curDay=0
    numLibs=0
    N_n_copy=copy.deepcopy(N_n)
    orderedLib=[]
    shippedBooks=[]

    while curDay<=D and numLibs<=L:
        # get the best lib
        candidate_lib.sort(key=cmp,reverse=True)
        curLib=candidate_lib[0]
        candidate_lib=candidate_lib[1:]

        if curDay+T[curLib]<D:
            curDay+=T[curLib]
            numLibs+=1
            orderedLib.append(curLib)
            sumBooks=min(D-curDay,N_n_copy[curLib])
            if sumBooks<N_n[curLib]:
                N[curLib].sort(key=sortBybookValue,reverse=True)
            shippedBooks+=[N[curLib][:sumBooks]]
            #set value to zero
            for book in N[curLib][:sumBooks]:
                if B_valueCur[book]!=0:
                    B_valueCur[book]=0
                    # if book in book_dic:
                    for lib in book_dic[book]:
                        N_n_copy[lib]-=1
        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            break
    return orderedLib,shippedBooks

def solveFromBook():
    def cmp(lib):
        return N_n_copy[lib]

    N_n_copy=copy.deepcopy(N_n)
    orderedLib=[]
    candidate_Lib=[]
    flag=[1 for i in range(B)]
    for book in book_dic:
        if len(book_dic[book])==2:
            candidate_list=book_dic[book]
            candidate_list.sort(key=cmp,reverse=True)
            curLib=candidate_list[0]
            orderedLib.append(curLib)
            candidate_Lib.append(candidate_list[1])
            for select_book in N[curLib]:
                if flag[select_book]!=0:
                    flag[select_book]=0
                    for lib in book_dic[select_book]:
                        N_n_copy[lib]-=1
    print(len(orderedLib))
    print((B-np.sum(flag))*65)

    shippedBooks=orderedLib2N_n(candidate_Lib,B_value,T,M,N_n,N,D)
    return orderedLib,shippedBooks


if __name__ == "__main__":
    input=parseINPUT("d_tough_choices.txt")
    B,L,D,B_value,N,T,M,N_n=input.values()
    book_dic={}
    for i in range(L):
        for book in N[i]:
            if book in book_dic:
                book_dic[book].append(i)
            else:
                book_dic[book]=[i]
    # orderedLib,shippedBooks=solve(B_value,[i for i in range(L)],0)
    orderedLib,shippedBooks=solveFromBook()
    submission=generateSubmission(orderedLib,shippedBooks)
    print(judgeFunction(submission,B_value))
    
    # # write submission to file.
    # with open("c_answer.txt","w") as f:
    #     f.write(submission)