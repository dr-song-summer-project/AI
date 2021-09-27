from collections import OrderedDict
from controller.nlp_controller import nlp_process
from controller.init import etri_process_getSrl, etri_process_getMorphList, KNU_process
import kss

class ApiForCorpus():
    def __init__(self, corpus):
        # originCorpus = request.json.get('corpus')
        self.originCorpus = corpus
        # 형태소 분석 Controller
    def getCorpus(self):
        processed_corpus = nlp_process(self.originCorpus)
        return processed_corpus

class divideCorpus():
    def __init__(self, corpus):
        self.corpus = corpus

    def splitSentence(self):
        self.splittedSentence = []
        for sent in kss.split_sentences(self.corpus):
            print('문장 구분 :', sent)
            self.splittedSentence.append(sent)

    def getCorpus(self):
        result = []
        self.splitSentence()
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
    corpus = '저는 아이 돌보는 것을 참 좋아하는 학생입니다. 그런데 솔직히 너무 너무 힘들었어요. 아이가 자기하고싶은대로만 하려고 해서 혼내면 욕하고 때리려고하고.. 아이가 너무 폭력적이었어요. ' \
             '놀이터에 나가서도 다른 어린친구들 괴롭히려고 하는데 어찌해야할지 모르겠더라구요.'
    # api = ApiForCorpus(corpus).getCorpus()
    # print(api)
    divide = divideCorpus(corpus).getCorpus()
    for each in divide:
        each_score = 0
        print(each['phrase'])
        for senti in each['sentiScore']:
            # each_score += int(senti['score'])
            print(senti)