import numpy as np
import copy
import math
from functools import cmp_to_key

def min(a,b):
        if a>b:
            return b
        else:
            return a

# function used to parse input.
def parseINPUT(file_name):
    f=open(file_name,"r")

    B,L,D=map(int,f.readline().split(" "))

    B_value=list(map(int,f.readline().split(" ")))
    # N_n used to store books in each library
    N_n=[]
    T=[]
    M=[]
    N=[]
    for i in range(L): 
        n,t,m=map(int,f.readline().split(" "))
        N_n.append(n)
        T.append(t)
        M.append(m)
        id_list=list(map(int,f.readline().split(" ")))
        N.append(id_list)
    f.close()
    return {
        "numOFbooks":B,
        "numOFlibs":L,
        "numOFdays":D,
        "valueOFbook":B_value,
        "numOFbooksINlib":N,
        "numOFsignupDays":T,
        "numOFbooksSHIPPED":M,
        "booksINlib":N_n
    }

# function to compute  the score of the submission.
# The input to the function is limited and it assume that the book all can be shipped legally.
# It is used for fine-tunning
def judgeFunction(output_string,B_value):
    # used to store current score can be added by this book.
    B_value_cur=copy.deepcopy(B_value)

    lines=output_string.split("\n")
    A=int(lines[0])

    sumBooks=0
    sum_score=0
    for i in range(A):
        books=list(map(int,lines[i*2+2].split(" ")))
        for book in books:
            sum_score+=B_value_cur[book]
            if B_value_cur[book]!=0:
                sumBooks+=1
                B_value_cur[book]=0
    print("number of books is %d"%sumBooks)
    return sum_score

def generateSubmission(orderedLib,shippedBooks):
    A=len(orderedLib)
    output=str(A)+"\n"
    for i in range(A):
        output+=(str(orderedLib[i])+" "+str(len(shippedBooks[i]))+"\n")
        for book in shippedBooks[i]:
            output+=(str(book)+" ")
        output=output[:-1]
        output+="\n"
    return output

def optimizer4b(input):
    def cmp_function(book):
        return T[book]

    B,L,D,B_value,N,T,M,N_n=input.values()
    orderedLib=[]
    shippedBooks=[]
    
    # sort by the number of sign up days
    orderBYsignup=[i for i in range(L)]
    orderBYsignup.sort(key=cmp_function)

    #iteration
    curDay=0
    numLibs=0
    while curDay<=D and numLibs<=B:
        # get the best lib
        curLib=orderBYsignup[0]
        orderBYsignup=orderBYsignup[1:]
        
        if curDay+T[curLib]<=D:
            curDay+=T[curLib]
            numLibs+=1
            orderedLib.append(curLib)
            sumBooks=min((D-curDay)*M[curLib],N_n[curLib])
            shippedBooks+=[N[curLib][:sumBooks]]
        else:
            break
    
    return orderedLib,shippedBooks

def optimizer4c(input):
    def cmp(lib):
        if curDay+T[lib]<D:
            SumValue=0
            for book in N[lib]:
                SumValue+=B_valueCur[book]
            return SumValue/T[lib]
        else: 
            return 0

    B,L,D,B_value,N,T,M,N_n=input.values()
    orderedLib=[]
    shippedBooks=[]
    # B_valueCur is used to store current value of books.
    B_valueCur=copy.deepcopy(B_value)

    orderBYcmp=[i for i in range(L)]
    
    #iteration
    curDay=0
    numLibs=0
    while curDay<=D and numLibs<=B:
        # get the best lib
        orderBYcmp.sort(key=cmp,reverse=True)
        curLib=orderBYcmp[0]
        orderBYcmp=orderBYcmp[1:]

        if curDay+T[curLib]<D:
            #set value to zero
            for book in N[curLib]:
                B_valueCur[book]=0

            curDay+=T[curLib]
            numLibs+=1
            orderedLib.append(curLib)
            sumBooks=min((D-curDay)*M[curLib],N_n[curLib])
            shippedBooks+=[N[curLib][:sumBooks]]
        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            break
    print(curDay)
    return orderedLib,shippedBooks

def optimizer4d(input):
    def sortBybookValue(key):
            return B_valueCur[key] 
    
    def cmp(lib):
        if curDay+T[lib]<D:
            return min(D-curDay-T[lib],N_n_copy[lib])
        else: 
            return 0

    B,L,D,B_value,N,T,M,N_n=input.values()
    orderedLib=[]
    shippedBooks=[]

    # B_valueCur is used to store current value of books.
    B_valueCur=copy.deepcopy(B_value)

    orderBYcmp=[i for i in range(L)]

    # book in which library dictionary.
    # used to reduce time complexity
    book_dic={}
    for i in range(L):
        for book in N[i]:
            if book in book_dic:
                book_dic[book].append(i)
            else:
                book_dic[book]=[i]
    
    #iteration
    curDay=0
    numLibs=0
    N_n_copy=copy.deepcopy(N_n)

    while curDay<=D and numLibs<=B:
        # get the best lib
        orderBYcmp.sort(key=cmp,reverse=True)
        curLib=orderBYcmp[0]
        orderBYcmp=orderBYcmp[1:]

        if curDay+T[curLib]<D:
            curDay+=T[curLib]
            numLibs+=1
            orderedLib.append(curLib)
            sumBooks=min((D-curDay)*M[curLib],N_n[curLib])
            if sumBooks<N_n[curLib]:
                N[curLib].sort(key=sortBybookValue,reverse=True)
            shippedBooks+=[N[curLib][:sumBooks]]

            #set value to zero
            for book in N[curLib][:sumBooks]:
                B_valueCur[book]=0
                if book in book_dic:
                    for lib in book_dic[book]:
                        N_n_copy[lib]-=1
                    del book_dic[book]
        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            break
    return orderedLib,shippedBooks

def optimizer4e(input):
    def sortBybookValue(key):
            return B_valueCur[key] 

    def cmp1(lib):
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

    def cmp2(lib):
        if curDay+T[lib]<D:
            SumValue=0
            sumBooks=min((D-curDay)*M[lib],N_n[lib])
            if sumBooks<N_n[lib]:
                N[lib].sort(key=sortBybookValue,reverse=True)
            shippedBooksLib=N[lib][:sumBooks]
            for book in shippedBooksLib:
                SumValue+=B_valueCur[book]
            # if curDay<=D/2:
            if curDay<=D/2:
                return SumValue/T[lib]
            else:
                return SumValue/math.sqrt(T[lib])
        else: 
            return 0

    B,L,D,B_value,N,T,M,N_n=input.values()
    orderedLib=[]
    shippedBooks=[]

    # B_valueCur is used to store current value of books.
    B_valueCur=copy.deepcopy(B_value)

    orderBYcmp=[i for i in range(L)]
    
    #iteration
    curDay=0
    numLibs=0
    L_valueCur=[0 for i in range(L)]
    while curDay<=D and numLibs<=B:

        # update value
        # used to save time
        for lib in orderBYcmp:
            L_valueCur[lib]=cmp1(lib)

        # get the best lib
        # orderBYcmp.sort(key=cmp1,reverse=True)
        # orderBYcmp.sort(key=cmp2,reverse=True)
        orderBYcmp.sort(key=cmp_to_key(cmp4),reverse=True)
        curLib=orderBYcmp[0]
        orderBYcmp=orderBYcmp[1:]

        if curDay+T[curLib]<D:
            curDay+=T[curLib]
            numLibs+=1
            orderedLib.append(curLib)
            sumBooks=min((D-curDay)*M[curLib],N_n[curLib])
            if sumBooks<N_n[curLib]:
                N[curLib].sort(key=sortBybookValue,reverse=True)
            shippedBooks+=[N[curLib][:sumBooks]]

            #set value to zero
            for book in N[curLib][:sumBooks]:
                B_valueCur[book]=0

        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            break    
    return orderedLib,shippedBooks

def optimizer4f(input):
    def sortBybookValue(key):
            return B_valueCur[key] 

    def cmp1(lib):
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

    def cmp3(lib1,lib2):
        gainValue1=cmp1(lib1)
        gainValue2=cmp1(lib2)
        if abs(gainValue1-gainValue2)<=480:
            return (T[lib2]-T[lib1])*(gainValue1-gainValue2)
        else:
            return gainValue1-gainValue2

    def cmp4(lib1,lib2):
        gainValue1=cmp1(lib1)
        gainValue2=cmp1(lib2)
        if abs(gainValue1-gainValue2)<=50:
            if gainValue1<gainValue2 and T[lib1]>=T[lib2]:
                return -1
            elif gainValue1>gainValue2 and T[lib1]<=T[lib2]:
                return 1
            else:
                if curDay<=D/2:
                    return T[lib2]-T[lib1]
                else:
                    return T[lib1]-T[lib2]
        else:
            return gainValue1-gainValue2

    B,L,D,B_value,N,T,M,N_n=input.values()
    orderedLib=[]
    shippedBooks=[]

    # B_valueCur is used to store current value of books.
    B_valueCur=copy.deepcopy(B_value)

    orderBYcmp=[i for i in range(L)]
    
    #iteration
    curDay=0
    numLibs=0

    while curDay<=D and numLibs<=B:
        # get the best lib
        # orderBYcmp.sort(key=cmp1,reverse=True)
        orderBYcmp.sort(key=cmp_to_key(cmp4),reverse=True)
        curLib=orderBYcmp[0]
        orderBYcmp=orderBYcmp[1:]

        if curDay+T[curLib]<D:
            curDay+=T[curLib]
            numLibs+=1
            orderedLib.append(curLib)
            sumBooks=min((D-curDay)*M[curLib],N_n[curLib])
            if sumBooks<N_n[curLib]:
                N[curLib].sort(key=sortBybookValue,reverse=True)
            shippedBooks+=[N[curLib][:sumBooks]]

            #set value to zero
            for book in N[curLib][:sumBooks]:
                B_valueCur[book]=0

        else:
            if curDay+T[curLib]==D:
                print("Fine tunning needed for the last choice")
            print(curDay)
            break
            
    return orderedLib,shippedBooks


if __name__ == "__main__":
    
    file_name_list=["a_example.txt","b_read_on.txt","c_incunabula.txt"
                    ,"d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]

    file_name=file_name_list[5]

    input=parseINPUT(file_name)
    orderedLib,shippedBooks=optimizer4f(input)
    submission=generateSubmission(orderedLib,shippedBooks)

    # show score of the submission.
    print(judgeFunction(submission,input["valueOFbook"]))
    
    # #write submission to file.
    # with open(file_name[0]+"_answer.txt","w") as f:
    #     f.write(submission)