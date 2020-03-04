from solve import parseINPUT
import numpy as np
def b_problem():
    B_value=parseINPUT("b_read_on.txt")["valueOFbook"]
    for value in B_value:
        assert value==100
    
def c_problem():
    input=parseINPUT("c_incunabula.txt")
    N_n,M=input["booksINlib"],input["numOFbooksSHIPPED"]
    for i in range(len(N_n)):
        assert N_n[i]<M[i]
    
    print(np.sum(N_n))
    B_value=input["valueOFbook"]
    print("Sum value is %d"%(np.sum(B_value)))

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


c_problem()