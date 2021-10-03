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

def getType(path):
    with open(path, 'rb+') as fp:
        file_text=fp.read()
        fp.seek(0)
        fp.write(b'reviewIndex	interviewReview	failureReview	recruitReview\n' + file_text)

    df = pd.read_csv(path, delimiter="\t")
    # column_name = ['reviewIndex', 'interviewReview', 'failureReview', 'recruitReview']
    print(df)
    # test_result = pd.DataFrame(df, columns=column_name)

    test_result = pd.DataFrame()
    test_result['reviewIndex'] = df['reviewIndex']
    interview = df['interviewReview'].values.tolist()
    failure = df['failureReview'].values.tolist()
    recruit = df['recruitReview'].values.tolist()
    test_result['reviewType'] = returnWhichBig_type(interview, failure, recruit)
    return test_result

def getLabel(path):
    with open(path, 'rb+') as fp:
        file_text=fp.read()
        fp.seek(0)
        fp.write(b'reviewIndex	Negative	Positive\n' + file_text)

    df = pd.read_csv(path, delimiter="\t")
    column_name = ['reviewIndex', 'Negative', 'Positive']
    df = pd.DataFrame(df, columns=column_name)
    nega = df['Negative'].values.tolist()
    posi = df['Positive'].values.tolist()

    return returnWhichBig_label(nega, posi)

test_result = pd.DataFrame()

test_result = getType('../data/ResultData/리뷰타입_results_0930.tsv')
test_result['Label'] = getLabel('../data/ResultData/긍부정_results.tsv')



test_result.to_csv('test_data_result_0930.csv', index = False)