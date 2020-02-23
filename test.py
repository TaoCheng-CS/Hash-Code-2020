from solve import*

def test_genSubmission():
    orderedLib=[1,0]
    shippedBooks=[
        [5,2,3],
        [0,1,2,3,4]
    ]
    print(generateSubmission(orderedLib,shippedBooks))

test_genSubmission()