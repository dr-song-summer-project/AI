from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm.notebook import tqdm
from collections import defaultdict
import pandas as pd
from konlpy.tag import Hannanum


def sorting(texts):
    sorted_txt = []
    for id, s in enumerate(texts):
        # s.sort(key = lambda s: s[1], reverse = True)
        s = sorted(s, key=lambda s: s[1], reverse=True)
        sorted_txt.append('[%d] %s ...' % (id, s[:5]))
    return sorted_txt


def read_file(path):
    df = pd.read_csv(path)

    is_recruit_review = df['reviewType'] == 'recruitReview'
    is_interview_review = df['reviewType'] == 'interviewReview'
    is_failure_review = df['reviewType'] == 'failureReview'

    recruit_review = df[is_recruit_review]
    interview_review = df[is_interview_review]
    failure_review = df[is_failure_review]

    df_np = pd.DataFrame.to_numpy(recruit_review['reviewContent'])
    recruit = []
    for i in range(len(df_np)):
        recruit.append(str(df_np[i]))

    df_np = pd.DataFrame.to_numpy(interview_review['reviewContent'])
    interview = []
    for i in range(len(df_np)):
        interview.append(str(df_np[i]))

    df_np = pd.DataFrame.to_numpy(failure_review['reviewContent'])
    failure = []
    for i in range(len(df_np)):
        failure.append(str(df_np[i]))

    return recruit, interview, failure


# ============================================
# -- Get TFIDF
# ============================================
def get_tfIdf(reviewType, name):
    vectorizer = TfidfVectorizer()
    sp_matrix = vectorizer.fit_transform(reviewType)
    hannanum = Hannanum()

    word2id = defaultdict(lambda: 0)
    for idx, feature in enumerate(vectorizer.get_feature_names()):
        word2id[feature] = idx

    f = open('src/' + name + 'TF_IDF.txt', 'w')

    for_sorting = [[] for _ in range(len(reviewType))]

    for i, sent in tqdm(enumerate(reviewType)):
        f.write('====== %d번 ======\n' % i)
        # print([ (token, sp_matrix[i, word2id[token]]) for token in sent.split() ])
        # f.write('[')
        for token in sent.split():
            f.write(token + ',')
            f.write(str(round(sp_matrix[i, word2id[token]], 6)) + ' ')
            for_sorting[i].append((token, round(sp_matrix[i, word2id[token]], 6)))
        f.write('\n')

    f.close()

    for_sorting = sorting(for_sorting)

    for i in range(len(for_sorting)):
        print(for_sorting[i])

    f = open('src/' + name + 'TF_IDF_sorted.txt', 'w')

    for i, sent in tqdm(enumerate(for_sorting)):
        # f.write('====== %d번 ======\n' % i)
        # for token in sent :
        f.write(sent)
        f.write('\n')

    f.close()


recruit, interview, failure = read_file('../data/TrainData/unlabeled_prepro.csv')

get_tfIdf(recruit, 'recruit')
get_tfIdf(interview, 'interview')
get_tfIdf(failure, 'failure')
