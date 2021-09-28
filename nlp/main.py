from collections import OrderedDict

import pandas as pd
from tqdm.notebook import tqdm

from controller.nlp_controller import nlp_process
from controller.init import etri_process_getSrl, etri_process_getMorphList, KNU_process
import kss
from pandas.io.parsers import read_csv

class ApiForCorpus(): #khaiii
    def __init__(self, corpus):
        # originCorpus = request.json.get('corpus')
        self.originCorpus = corpus
        # 형태소 분석 Controller
    def getCorpus(self):
        processed_corpus = nlp_process(self.originCorpus)
        return processed_corpus

class divideCorpus():  #etri
    def __init__(self):
        print('객체 생성')

    def splitSentence(self, corpus):
        self.splittedSentence = []
        for sent in kss.split_sentences(corpus):
            print('문장 구분 :', sent)
            self.splittedSentence.append(sent)

    def getCorpus(self,corpus):
        result = []
        self.splitSentence(corpus)
        for originCorpus in self.splittedSentence:
            processed_corpues = OrderedDict()
            processed_corpues0 = etri_process_getMorphList(originCorpus) #morph
            processed_corpus1 = etri_process_getSrl(originCorpus) #phrase
            processed_corpus2 = KNU_process(originCorpus) #sentimentScore
            processed_corpues['morph'] = processed_corpues0
            processed_corpues['phrase'] = processed_corpus1
            processed_corpues['sentiScore'] = processed_corpus2
            result.append(processed_corpues)
        return result
        #받은 문장을 가지고 분석 시작

class knuCorpus():
    def __init__(self, corpus):
        self.originCorpus = corpus
    def getCorpus(self):
        processed_corpus = KNU_process(self.originCorpus)
        return processed_corpus
        #받은 문장을 가지고 분석 시장


if __name__ == "__main__":
    # senti_Score = []
    # corpus = '서비스는 괜찮고 음식은 별로에요.'
    df = read_csv('../data/TrainData/train_prepro.csv')
    result = pd.DataFrame()
    corpuses = df['reviewContent'].values.tolist()
    print(corpuses)
    # corpus = '매주 오셔서 아이와 잘 놀아주세요~아이가 원해서 주 2회로 늘릴 예정입니다 성실하고 좋으신 분 같습니다.'
    mc = []
    divideCor = divideCorpus()
    for corpus in tqdm(corpuses):
        mc_tmp = []
        divide = divideCor.getCorpus(corpus)
        for each in divide:
            tmp = []
            for senti in each['sentiScore']:
                tmp.append(senti['morp'] + '/' + senti['score'])
            mc_tmp.append(tmp)
        mc.append(mc_tmp)
    print(mc)

    # raw_data={'reviewIndex':df['reviewIndex'].values.tolist(),
    #           'reviewContent': df['reviewContent'].values.tolist(),
    result['reviewIndex'] = df['reviewIndex']
    result['reviewContent'] = df['reviewContent']
    result['phraseSent'] = mc

    result.to_csv('src/train_phraseSent.csv')