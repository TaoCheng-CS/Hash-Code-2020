import copy
from solve import *

def orderedLib2N_n(orderLib,B_value,T,M,N_n,N,D):
    def sortBybookValuein(key):
        return B_valueCur[key] 
    curDay=0
    shippedBooks=[]
    B_valueCur=copy.deepcopy(B_value)
    for lib in orderLib:
        sumBooks=min((D-curDay-T[lib])*M[lib],N_n[lib])
        if sumBooks<N_n[lib]:
            N[lib].sort(key=sortBybookValuein,reverse=True)
        shippedBooks+=[N[lib][:sumBooks]]
        curDay+=T[lib]
        for book in N[lib][:sumBooks]:
            B_valueCur[book]=0
    return shippedBooks


def solveByLocalOpt(candidateLib,B_value,T,M,N_n,N,lastDays):

    def sortBybookValue(key):
        return B_valueCur[key]
    
    def cmp(lib):
        if curDay+T[lib]<D:
            SumValue=0
            sumBooks=min((D-curDay-T[lib])*M[lib],N_n[lib])
            if sumBooks<N_n[lib]:
                N[lib].sort(key=sortBybookValue,reverse=True)
                shippedBooksLib=N[lib][:sumBooks]
                for book in shippedBooksLib:
                    SumValue+=B_valueCur[book]
                return SumValue/T[lib]
            else:
                return libValue[lib]/T[lib]
        else: 
            return 0

    D=lastDays
    orderBYcmp=copy.deepcopy(candidateLib)
    B_valueCur=copy.deepcopy(B_value)

    # book in which library dictionary.
    # used to reduce time complexity
    book_dic={}
    for lib in candidateLib:
        for book in N[lib]:
            if book in book_dic:
                book_dic[book].append(lib)
            else:
                book_dic[book]=[lib]

    libValue={}
    for lib in candidateLib:
        SumValue=0
        for book in N[lib]:
            SumValue+=B_valueCur[book]
        libValue[lib]=SumValue

    #iteration
    curDay=0
    optValue=0
    while curDay<=D and len(orderBYcmp)>=1:
        # get the best lib
        orderBYcmp.sort(key=cmp,reverse=True)
        curLib=orderBYcmp[0]
        orderBYcmp=orderBYcmp[1:]

        if curDay+T[curLib]<D:
            curDay+=T[curLib]
            sumBooks=min((D-curDay)*M[curLib],N_n[curLib])
            if sumBooks<N_n[curLib]:
                N[curLib].sort(key=sortBybookValue,reverse=True)

            #set value to zero
            for book in N[curLib][:sumBooks]:
                optValue+=B_valueCur[book]
                if book in book_dic:
                    for lib in book_dic[book]:
                        libValue[lib]-=B_valueCur[book]
                    del book_dic[book]
                B_valueCur[book]=0
        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            break
    return optValue

def cmp(lib):
    if curDay+T[lib]<D:
        SumValue=0
        sumBooks=min((D-curDay)*M[lib],N_n[lib])
        if sumBooks<N_n[lib]:
            N[lib].sort(key=sortBybookValue,reverse=True)
        shippedBooksLib=N[lib][:sumBooks]
        for book in shippedBooksLib:
            SumValue+=B_valueCur[book]
        return SumValue/T[lib]
    else: 
        return 0

def sortBybookValue(key):
    return B_valueCur[key]

limit=100
input=parseINPUT("f_libraries_of_the_world.txt")
B,L,D,B_value,N,T,M,N_n=input.values()


B_valueCur=copy.deepcopy(B_value)
orderBYcmp=[i for i in range(L)]
orderLib=[]

finalScore=0
curDay=0
while curDay<=D and len(orderBYcmp)>=1:
    orderBYcmp.sort(key=cmp,reverse=True)
    candidateLib=orderBYcmp[:limit]

    choose=-1
    valueGain=0
    libGain=0
    for lib in candidateLib:
        if curDay+T[lib]<D:
            gain=0
            B_valueCur4lib=copy.deepcopy(B_valueCur)
            sumBooks=min((D-curDay-T[lib])*M[lib],N_n[lib])
            if sumBooks<N_n[lib]:
                N[lib].sort(key=sortBybookValue,reverse=True)
            for book in N[lib][:sumBooks]:
                gain+=B_valueCur4lib[book]
                B_valueCur4lib[book]=0
            
            orderBYcmpCur=copy.deepcopy(orderBYcmp)
            orderBYcmpCur.remove(lib)
            estimateGain=solveByLocalOpt(orderBYcmpCur,B_valueCur4lib,T,M,N_n,N,D-curDay-T[lib])
            gain+=estimateGain
            if gain>valueGain:
                valueGain=gain
                choose=lib
                libGain=gain-estimateGain
    
    if choose==-1:
        break
    sumBooks=min((D-curDay-T[choose])*M[choose],N_n[choose])
    if sumBooks<N_n[choose]:
        N[choose].sort(key=sortBybookValue,reverse=True)
    for book in N[choose][:sumBooks]:
        B_valueCur[book]=0

    curDay+=T[choose]
    finalScore+=libGain
    orderLib.append(choose)
    print(len(orderLib))
    orderBYcmp.remove(choose)
print("final score %d"%finalScore)
print("Curday %d"%curDay)
print(orderLib)
# orderLib=[147, 204, 210, 694, 719, 595, 774, 901, 618, 369, 422, 312, 622, 672, 828, 454, 431]
shippedBooks=orderedLib2N_n(orderLib,B_value,T,M,N_n,N,D)
submission=generateSubmission(orderLib,shippedBooks)
# show score of the submission.
print(judgeFunction(submission,B_value))

#write submission to file.
with open("f"+"_answer_esti.txt","w") as f:
    f.write(submission)