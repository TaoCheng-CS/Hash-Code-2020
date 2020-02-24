import numpy as np
import copy

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

    sum_score=0
    for i in range(A):
        books=list(map(int,lines[i*2+2].split(" ")))
        for book in books:
            sum_score+=B_value_cur[book]
            B_value_cur[book]=0
    
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

    def min(a,b):
        if a>b:
            return b
        else: 
            return a

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

if __name__ == "__main__":
    
    file_name_list=["a_example.txt","b_read_on.txt","c_incunabula.txt"
                    ,"d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]

    file_name=file_name_list[1]

    input=parseINPUT(file_name)
    orderedLib,shippedBooks=optimizer4b(input)
    submission=generateSubmission(orderedLib,shippedBooks)

    print(judgeFunction(submission,input["valueOFbook"]))
    
    # #write submission to file.
    # with open(file_name[0]+"_answer.txt","w") as f:
    #     f.write(submission)
