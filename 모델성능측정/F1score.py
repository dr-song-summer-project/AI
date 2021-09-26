from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import pandas as pd


#edit point __
def returnWhichBig(a, b):
  result = []
  for i in range(0, len(a)):
    if a[i]>b[i]:   #긍정
      result.append(1)
    else:           #부정
      result.append(0)
  return result

def F1_score(label, guess):
  train_df = pd.read_csv(label)
  guess_df = pd.read_csv(guess, delimiter='\t', header=0)
  train_df.drop(['encodedSenderId', 'encodedTargetId', 'DateTime'], axis=1, inplace=True)
  train_df = train_df.drop([train_df.index[0]])
  # train_df.head()

  train_df = train_df.reset_index(drop=True)  # 인덱스 초기화
  guess_df = guess_df.reset_index(drop=True)
  print(train_df)

  labels = train_df['Label'].values.tolist()  # 실제 측정값
  # print(len(labels), labels)

  posi = guess_df['Positive'].values.tolist()
  nega = guess_df['Negative'].values.tolist()

  # print(guess_df)

  guesses = returnWhichBig(posi, nega)

  print('accuracy:', accuracy_score(labels, guesses))
  print('recall:', recall_score(labels, guesses))
  print('precision:', precision_score(labels, guesses))
  print('f1_score:', f1_score(labels, guesses))


label_path = '../전처리/data/train_data.csv'
guess_path = '../../../데이터/train_data_modeling_결과.tsv'

F1_score(label_path, guess_path)
