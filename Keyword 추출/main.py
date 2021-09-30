from tfidf_KOR import tfidfScorer
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm.notebook import tqdm
from collections import defaultdict
import nltk
import pandas as pd
from konlpy.tag import Hannanum
from openpyxl import Workbook


def read_file(path):
    df = pd.read_csv(path)

    is_recruit_review = df['reviewType'] == 'recruitReview'
    is_interview_review = df['reviewType'] == 'interviewReview'
    is_failure_review = df['reviewType'] == 'failureReview'

    recruit_review = df[is_recruit_review]
    interview_review = df[is_interview_review]
    failure_review = df[is_failure_review]

    return recruit_review, interview_review, failure_review


recruit, interview, failure = read_file('../data/TrainData/unlabeled_prepro.csv')

corpus = recruit['reviewContent']

for id, s in enumerate( tfidfScorer(corpus) ):
    s = sorted(s, key=lambda x:x[1], reverse=True)
    print('%s ...' % (s[:10]))