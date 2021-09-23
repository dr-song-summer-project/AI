from konlpy.tag import Okt
import pandas as pd
from pandas import read_excel
from tqdm.notebook import tqdm

def read_file(path):
  # df = pd.read_csv(path)
  df = pd.read_csv(path, delimiter='\t', header=0)  #tsv 파일 읽을 때
  print(df)
  sentence = df['reviewContent'].values.tolist()
  index = df['reviewIndex'].values.tolist()
  return df, sentence, index

def keyword(text) :
  if text == '':
    print('error')
    return(text)
  else:
    okt_pos = Okt().pos(text, norm=True, stem=True)   # 형태소 분석 ( norm : 정규화 )
    okt_filtering = [x for x, y in okt_pos if y in ['Noun']]
    return okt_filtering

def to_excel(text) :
  df, sentence, index = read_excel('/content/unlabeled_data_prepro.txt')
  convert_keyword = []
  for i in tqdm(range(0, len(sentence))):
    convert_keyword.append(keyword(sentence[i]))
    # print(convert_keyword[i])