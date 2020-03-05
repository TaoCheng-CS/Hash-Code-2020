from solve import parseINPUT
import numpy as np
def b_problem():
    input=parseINPUT("b_read_on.txt")
    B_value=input["valueOFbook"]
    M=input["numOFbooksSHIPPED"]
    for value in B_value:
        assert value==100
    for value in M:
        assert value==1
    
def c_problem():
    input=parseINPUT("c_incunabula.txt")
    N_n,M=input["numOFbooksINlib"],input["numOFbooksSHIPPED"]
    for i in range(len(N_n)):
        assert N_n[i]<M[i]
    
    print("Sum of N_n is %d"%(np.sum(N_n)))
    B_value=input["valueOFbook"]
    print("Sum value is %d"%(np.sum(B_value)))

    N=input["booksINlib"]
    book_time_dic={}
    for lib in N:
        for book in lib:
            if book in book_time_dic:
                book_time_dic[book]+=1
            else:
                book_time_dic[book]=1
    bucks={}
    for book in book_time_dic:
        value=book_time_dic[book]
        if  value in bucks:
            bucks[value]+=1
        else:
            bucks[value]=1
    print("bucks of book exist: ")
    print(bucks)

    value_bucks={}
    for value in B_value:
        if  int(value/10) in value_bucks:
            value_bucks[int(value/10)]+=1
        else:
            value_bucks[int(value/10)]=1
    print("bucks of book value: ")
    print(value_bucks)

def d_problem():
    input=parseINPUT("d_tough_choices.txt")
    B,L,D,B_value,N,T,M,N_n=input.values()

    for value in B_value:
        assert value==65
    
    for n in N_n:
        assert n<=14

    for t in T:
        assert t==2
    
    for m in M:
        assert m==1
    
    print(np.sum(N_n))
    book_time_dic={}
    for lib in N:
        for book in lib:
            if book in book_time_dic:
                book_time_dic[book]+=1
            else:
                book_time_dic[book]=1
    bucks={}
    for book in book_time_dic:
        value=book_time_dic[book]
        if  value in bucks:
            bucks[value]+=1
        else:
            bucks[value]=1
    print("bucks of book exist: ")
    print(bucks)

    N_n_bucks={}
    for value in N_n:
        if  value in N_n_bucks:
            N_n_bucks[value]+=1
        else:
            N_n_bucks[value]=1
    print("bucks of N_n value: ")
    print(N_n_bucks)

    time_list=[]
    for lib in N:
        time=0
        for book in lib:
            if book_time_dic[book]==2:
                time+=1
        time_list.append(time)
    
    time_bucks={}
    for value in time_list:
        if  value in time_bucks:
            time_bucks[value]+=1
        else:
            time_bucks[value]=1
    print("bucks of book time appears value: ")
    print(time_bucks)



def e_problem():
    input=parseINPUT("e_so_many_books.txt")
    N_n,M=input["booksINlib"],input["numOFbooksSHIPPED"]
    print(np.sum(N_n))
    for m in M:
        assert m==1 or m==2

    
    B_value=input["valueOFbook"]
    B_value.sort(reverse=True)
    print(np.sum(B_value[:28669]))


def f_problem():
    input=parseINPUT("f_libraries_of_the_world.txt")
    N_n,M=input["booksINlib"],input["numOFbooksSHIPPED"]
    print(np.sum(N_n))

    T=input["numOFsignupDays"]
    print("T min is %d"%(np.min(T)))
    print("T max is %d"%(np.max(T)))

    M=input["numOFbooksSHIPPED"]
    print("M min is %d"%(np.min(M)))
    print("M max is %d"%(np.max(M)))

    B_value=input["valueOFbook"]
    print("value min is %d"%(np.min(B_value)))
    print("value max is %d"%(np.max(B_value)))
    B_value.sort(reverse=True)
    print(np.sum(B_value[:12881]))



d_problem()