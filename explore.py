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

def f_problem():
    input=parseINPUT("f_libraries_of_the_world.txt")
    N_n,M=input["booksINlib"],input["numOFbooksSHIPPED"]
    print(np.sum(N_n))
