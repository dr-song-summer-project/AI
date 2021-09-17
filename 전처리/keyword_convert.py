from konlpy.tag import Okt
import pandas as pd
from tqdm.notebook import tqdm

def read_file(path):
  df = pd.read_excel(path)
  sentence = df['reviewContent'].values.tolist()
  # index = df['reviewIndex'].values.tolist()
  return sentence

def keyword_(text) :
  okt_pos = Okt().pos(text, norm=True, stem=True)   # 형태소 분석 ( norm : 정규화 )
  okt_filtering = [x for x, y in okt_pos if y in ['Noun']] 
  return okt_filtering

def remove_tag(text) :
  text = text.replace('\'', '')
  text = text.replace(',', '')
  text = text.replace('[', '')
  text = text.replace(']', '')
  return text