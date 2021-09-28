from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import pandas as pd

def returnWhichBig_label(a, b):
  result = []
  for i in range(0, len(a)):
    if a[i]>b[i]:
      result.append(1)
    else:
      result.append(0)
  return result

def returnWhichBig_type(a, b, c):  # a = interview, b = failure, c = recruit
    result = []
    for i in range(0, len(a)):
        if a[i] > b[i] and a[i] > c[i]:
            result.append(0)
        elif b[i] > c[i]:
            result.append(1)
        else:
            result.append(2)
    return result

def F1_score(label, guess):
    # train_df = pd.read_csv(label)
    train_df = pd.read_csv(label, delimiter='\t', header=0)
    guess_df = pd.read_csv(guess, delimiter='\t', header=0)
    # train_df.drop(['encodedSenderId', 'encodedTargetId', 'DateTime'], axis=1, inplace=True)
    # train_df = train_df.drop([train_df.index[0]])
    # train_df.head()

    train_df = train_df.reset_index(drop=True)  # 인덱스 초기화
    guess_df = guess_df.reset_index(drop=True)

    # print(train_df)
    return train_df, guess_df

def labels(label, guess):
  train_df, guess_df = F1_score(label, guess)
  labels = train_df['Label'].values.tolist()

  posi = guess_df['Positive'].values.tolist()
  nega = guess_df['Negative'].values.tolist()

  guesses = returnWhichBig_label(posi, nega)

  print('guesses:', len(guesses), ':', guesses)

  print('accuracy:', accuracy_score(labels, guesses))
  print('recall:', recall_score(labels, guesses))
  print('precision:', precision_score(labels, guesses))
  print('f1_score:', f1_score(labels, guesses))

def reviewType(label, guess):
    train_df, guess_df = F1_score(label, guess)
    tmp_labels = train_df['reviewType'].values.tolist()  # 실제 측정값
    label_dict = {'interviewReview': 0, 'failureReview': 1, 'recruitReview': 2}
    labels = []
    for x in tmp_labels:
        labels.append(label_dict[x])
    print('labels:', len(labels), ':', labels)

    interview = guess_df['interviewReview'].values.tolist()
    failure = guess_df['failureReview'].values.tolist()
    recruit = guess_df['recruitReview'].values.tolist()

    guesses = returnWhichBig_type(interview, failure, recruit)

    print('guesses:', len(guesses), ':', guesses)

    print('accuracy:', accuracy_score(labels, guesses))
    print('recall:', recall_score(labels, guesses, average='weighted'))
    print('precision:', precision_score(labels, guesses, average='weighted'))
    print('f1_score:', f1_score(labels, guesses, average='weighted'))


##################실행######################


##실제 데이터
label_path = '../data/TrainData/13400/test_data_13400.txt'

##예측 결과 데이터
guess_path = '../data/test_results.tsv'


##긍부정 정확도
# labels(label_path, guess_path)

##리뷰 타입 정확도
reviewType(label_path, guess_path)