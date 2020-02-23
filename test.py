from solve import*

def test_genSubmission():
    orderedLib=[1,0]
    shippedBooks=[
        [5,2,3],
        [0,1,2,3,4]
    ]
    print(generateSubmission(orderedLib,shippedBooks))

def test_score():
    f=open("a_answer.txt","r")
    B_value=[1,2,3,6,5,4]
    output_string=f.read()
    score=judgeFunction(output_string,B_value)
    print(score)

test_score()