def parseINPUT(file_name):
    f=open(file_path,"r")

    B,L,D=map(int,f.readline().split(" "))
    print(B,L,D)

    B_value=list(map(int,f.readline().split(" ")))
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


file_name_list=["a_example.txt","b_read_on.txt","c_incunabula.txt"
                ,"d_tough_choices.txt","e_so_many_books.txt","f_libraries_of_the_world.txt"]

file_path=file_name_list[4]

