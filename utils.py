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
        "booksINlib":N,
        "numOFsignupDays":T,
        "numOFbooksSHIPPED":M,
        "numOFbooksINlib":N_n
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

def weak_judgeFunction(shippedBooks,B_value):
    sum_score=0
    B_value_cur=copy.deepcopy(B_value)
    for lib in shippedBooks:
        for book in lib:
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

def bubbleSortReversed(inList,cmp,number):
    length=len(inList)
    assert length>=number

    for i in range(number):
        for j in range(i+1,length):
            if cmp(inList[i],inList[j])<0:
                # swap
                inList[i],inList[j]=inList[j],inList[i]

def min(a,b):
    if a>b:
        return b
    else:
        return a

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