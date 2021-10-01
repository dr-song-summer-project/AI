import pandas as pd

def returnWhichBig_label(a, b):
  result = []
  for i in range(0, len(a)):
    if a[i]>b[i]:
      result.append(0)
    else:
      result.append(1)
  return result

def returnWhichBig_type(a, b, c):  # a = interview, b = failure, c = recruit
    result = []
    for i in range(0, len(a)):
        if a[i] > b[i] and a[i] > c[i]:
            result.append('interviewReview')
        elif b[i] > c[i]:
            result.append('failureReview')
        else:
            result.append('recruitReview')
    return result

def getType():
    df = pd.read_csv('../data/ResultData/리뷰타입_results.tsv', delimiter="\t")
    test_result = pd.DataFrame()
    test_result['reviewIndex'] = df['reviewIndex']
    # test_result['reviewContent'] = df['reviewContent']

    interview = df['interviewReview'].values.tolist()
    failure = df['failureReview'].values.tolist()
    recruit = df['recruitReview'].values.tolist()
    test_result['reviewType'] = returnWhichBig_type(interview, failure, recruit)
    return test_result

def getLabel():
    df = pd.read_csv('../data/ResultData/긍부정_results.tsv', delimiter="\t")

    nega = df['0'].values.tolist()
    posi = df['1'].values.tolist()

    return returnWhichBig_label(nega, posi)

test_result = pd.DataFrame()

test_result = getType()
test_result['Label'] = getLabel()



test_result.to_csv('test_data_result.csv', index = False)