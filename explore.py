from solve import parseINPUT
def b_problem():
    B_value=parseINPUT("b_read_on.txt")["valueOFbook"]
    for value in B_value:
        assert value==100