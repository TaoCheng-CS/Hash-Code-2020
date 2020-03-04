import copy
from solve import *

def bubbleSortReversed(inList,cmp,number):
    length=len(inList)
    assert length>=number

    for i in range(number):
        for j in range(i+1,length):
            if cmp(inList[i],inList[j])<0:
                # swap
                inList[i],inList[j]=inList[j],inList[i]

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


def solveByLocalOpt(candidateLib,LibBookValueCur,T,M,N_n,N,lastDays,book_dic):

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

if __name__ == "__main__":

    def sortBybookValuein(key):
        return B_value[key] 
    def cmp(lib1, lib2):
        return calGain(lib1,False)/T[lib1]-calGain(lib2,False)/T[lib2]
    
    def calGain(lib,returnchooseList):
        choosedList=[]
        if curDay+T[lib]<D:
            SumValue=0
            sumBooks=min((D-curDay-T[lib])*M[lib],N_n[lib])
            # condition 1 when we have to choose the best 
            if sumBooks<N_n[lib]:
                chooseNum=0
                for i in range(N_n[lib]):
                    Bookvalue=LibBookValue[lib][i]
                    if chooseNum>=sumBooks:
                        break
                    if Bookvalue!=0:
                        chooseNum+=1
                        SumValue+=Bookvalue
                        choosedList.append(i)
                
                if returnchooseList:
                    return SumValue,choosedList
                else:
                    return SumValue
            else:
                SumValue=np.sum(LibBookValue[lib])
                if returnchooseList:
                    return SumValue,[i for i in range(N_n[lib])]
                else:
                    return SumValue
        else: 
            if returnchooseList:
                return 0,[]
            else:
                return 0


    limit=1
    input=parseINPUT("f_libraries_of_the_world.txt")
    B,L,D,B_value,N,T,M,N_n=input.values()

    orderBYcmp=[i for i in range(L)]
    orderLib=[]

    for i in range(L):
        N[i].sort(key=sortBybookValuein,reverse=True)

    # libvalue is used to store the maxim value of library.
    # libBookValue is used to store the current value of book
    # book dic is book in which library dictionary.
    # used to reduce time complexity
    # variable initialization
    LibBookValue={}
    book_dic={}
    for lib in orderBYcmp:
        valueList=[]
        for index in range(N_n[lib]):
            book=N[lib][index]
            valueList.append(B_value[book])
            if book in book_dic:
                book_dic[book].append((lib,index))
            else:
                book_dic[book]=[(lib,index)]
        LibBookValue[lib]=valueList 

    shippedBooks=[]
    finalScore=0
    curDay=0
    while curDay<=D and len(orderBYcmp)>=1:
        bubbleSortReversed(orderBYcmp,cmp,limit)
        candidateLib=orderBYcmp[:limit]

        chooseLib=-1
        valueGain=0
        libGain=0
        curLibchoosed=[]
        for lib in candidateLib:
            if curDay+T[lib]<D:
                gain,choosedList=calGain(lib,True)

                LibBookValueCur=copy.deepcopy(LibBookValue)
                for bookindex in choosedList:
                    book=N[lib][bookindex]
                    for curlib,index in book_dic[book]:
                        LibBookValueCur[curlib][index]=0

                orderBYcmpCur=copy.deepcopy(orderBYcmp)
                orderBYcmpCur.remove(lib)
                # estimateGain=solveByLocalOpt(orderBYcmpCur,LibBookValueCur,T,M,N_n,N,D-curDay-T[lib],book_dic)
                estimateGain=0
                gain+=estimateGain
                if gain>valueGain:
                    valueGain=gain
                    chooseLib=lib
                    libGain=gain-estimateGain
                    curLibchoosed=choosedList
        if chooseLib==-1:
            break
        book_List=[]
        for bookindex in curLibchoosed:
            book=N[chooseLib][bookindex]
            book_List.append(book)
            for lib,index in book_dic[book]:
                LibBookValue[lib][index]=0
        
        shippedBooks.append(book_List)
        curDay+=T[chooseLib]
        finalScore+=libGain
        orderLib.append(chooseLib)
        orderBYcmp.remove(chooseLib)
    print("final score %d"%finalScore)
    print("Curday %d"%curDay)
    print(orderLib)
    # orderLib=[147, 204, 210, 694, 719, 595, 774, 901, 618, 369, 422, 312, 622, 672, 828, 454, 431]
    # shippedBooks=orderedLib2N_n(orderLib,B_value,T,M,N_n,N,D)
    submission=generateSubmission(orderLib,shippedBooks)
    # show score of the submission.
    print(judgeFunction(submission,B_value))

    # #write submission to file.
    # with open("f"+"_answer_esti.txt","w") as f:
    #     f.write(submission)