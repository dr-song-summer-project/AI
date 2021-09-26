import re
from typing import OrderedDict
import urllib3
import json
import NLP_감성사전.config as config

class Etri:
    def __init__(self, text):
        self.text = ""
        self.count = 0  # phrase 동사 찾기
        self.text = text
        self.json_data = ''
        self.morp_list = []  # 형태소 분석 결과
        self.word_list = []  # 어절 분석 결과
        self.word_morp_list = []  # 어절별 형태소 분석 결과
        self.openApiURL = config.ETRI_CONFIG['OPENAPIURL']
        self.accessKey = config.ETRI_CONFIG['ETRI_KEY']
        self.request_result = self.getEtri("srl") #Etri API reponse
        self.significant_tags = ['NNG', 'NNP', 'NP', 'NNB', 'VV', 'VA', 'VX', 'MAG', 'MAJ']

    def getEtri(self, type):
        requestJson = {
            "access_key": self.accessKey,
            "argument": {
                "text": self.text,
                "analysis_code": type
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            self.openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )

        result = (str(response.data, "utf-8"))
        self.json_data = json.loads(result)

        return json.loads(result)

# significant morp만 골라내기
    def getSignMorpList(self):
        json_morp = self.request_result        
        for sen in (json_morp['return_object']['sentence'][0]['morp']):
            if sen['type'] in self.significant_tags :
                self.morp_list.append((sen['lemma'], sen['type']))        
        return self.morp_list
        
#형태소 분석 결과 단어(어절) 단위로 합치기
    def makeList(self):
        json_reponse = self.request_result

        # Morph 목록
        for morph in (json_reponse['return_object']['sentence'][0]['morp']):
            self.morp_list.append((morph['lemma'], morph['type']))

        # Word 의 begin, end  id 값 리스트 저장
        for word in (json_reponse['return_object']['sentence'][0]['word']):
            self.word_list.append((word['begin'], word['end']))

        #word_morph_list 에 대입
        for begin, end in self.word_list:
            tmp = []
            for i in range(int(begin), int(end)+1):
                tmp.append(self.morp_list[i])
            self.word_morp_list.append(tmp)

        return self.word_morp_list    

#Phrase 분석
    def getSrl(self):
        json_SRL = self.request_result
        SRLObject = json_SRL.get("return_object").get("sentence")[0].get("SRL")
        phrase_list = []
        for i, x in enumerate(SRLObject):
            phrase_data = {"id": i}
            text = ""
            verb = ""
            args = x.get("argument")
            for arg in args:
                arg_text = arg.get("text")
                #감정분석을 위한 ARG1 type 체크
                arg_type = arg.get("type") 
                if arg_type == 'ARG1': # 대상 일때
                    phrase_data["ARG1"] = arg_text

                text += str(arg_text) + ' '
            verb = x.get("verb")
            #감정분석을 위한 verb 추가
            phrase_data["verb"] = verb             

            text += str(verb)
            ec, analysis = self.find_EC_type(verb, self.count)
            phrase_data["phrase"] = text

            phrase_data["ec"] = ec
            phrase_data["analysis"] = analysis
            phrase_list.append(phrase_data)

        return phrase_list

# 동사 -> 원형으로 바꾸기
    def stemming_text(self, text):
        p1 = re.compile('[가-힣A-Za-z0-9]+/NN. [가-힣A-Za-z0-9]+/XS.')
        p2 = re.compile('[가-힣A-Za-z0-9]+/NN. [가-힣A-Za-z0-9]+/XSA [가-힣A-Za-z0-9]+/VX')
        p3 = re.compile('[가-힣A-Za-z0-9]+/VV')
        p4 = re.compile('[가-힣A-Za-z0-9]+/VX')

        tmp = []
        for sent in text:
            tmp.append(sent[0] + '/' + sent[1] + ' ')
        text = tmp
        corpus = []
        for sent in (text):
            ori_sent = sent
            mached_terms = re.findall(p1, ori_sent)
            for terms in mached_terms:
                ori_terms = terms
                modi_terms = ''
                for term in terms.split(' '):
                    lemma = term.split('/')[0]
                    tag = term.split('/')[-1]
                    modi_terms += lemma
                modi_terms += '다/VV'
                sent = sent.replace(ori_terms, modi_terms)

            mached_terms = re.findall(p2, ori_sent)
            for terms in mached_terms:
                ori_terms = terms
                modi_terms = ''
                for term in terms.split(' '):
                    lemma = term.split('/')[0]
                    tag = term.split('/')[-1]
                    if tag != 'VX':
                        modi_terms += lemma
                modi_terms += '다/VV'
                sent = sent.replace(ori_terms, modi_terms)

            mached_terms = re.findall(p3, ori_sent)
            for terms in mached_terms:
                ori_terms = terms
                modi_terms = ''
                for term in terms.split(' '):
                    lemma = term.split('/')[0]
                    tag = term.split('/')[-1]
                    modi_terms += lemma
                if '다' != modi_terms[-1]:
                    modi_terms += '다'
                modi_terms += '/VV'
                sent = sent.replace(ori_terms, modi_terms)

            mached_terms = re.findall(p4, ori_sent)
            for terms in mached_terms:
                ori_terms = terms
                modi_terms = ''
                for term in terms.split(' '):
                    lemma = term.split('/')[0]
                    tag = term.split('/')[-1]
                    modi_terms += lemma
                if '다' != modi_terms[-1]:
                    modi_terms += '다'
                modi_terms += '/VV'
                sent = sent.replace(ori_terms, modi_terms)
            corpus.append(sent)

        dict_a = {}
        for i in range(len(corpus)):
            cut = corpus[i].find('/')
            # corpus[i] = corpus[i][0:cut]
            dict_a[corpus[i][0:cut]] = corpus[i][cut + 1:len(corpus[i])]
        a = list(dict_a.items())
        return corpus, a

# 연결 어미 종류
    def which_ec(self, ec):
        list = ['고', '며', '으며']
        Select = ['거나', '든지']
        Contrast = ['나', '으나', '지만', '는데', '은데', '아도', '어도']
        Simultaneous = ['면서', '으면서', '며', '으며', '자', '자마자']
        Order = ['고', '아서', '어서']
        Transition = ['다가']
        Cause = ['아서', '어서', '니', '으니', '으니까', '니까', '므로', '으므로', '느라고']
        Condition = ['면', '으면', '려면', '으려면', '아야', '어야']
        Purpose = ['러', '으러', '려고', '으려고', '도록', '게']
        Recognition = ['아도', '어도', '지라도', '을지라도', '더라도']
        Means = ['아서', '어서', '고']
        Background = ['는데', 'ㄴ데', '니', '으니']

        if ec in list:
            return '나열'
        elif ec in Select:
            return '선택'
        elif ec in Contrast:
            return '대립/대조'
        elif ec in Simultaneous:
            return '동시'
        elif ec in Order:
            return '순서'
        elif ec in Transition:
            return '전환'
        elif ec in Cause:
            return '원인'
        elif ec in Condition:
            return '조건'
        elif ec in Purpose:
            return '목적'
        elif ec in Recognition:
            return '인정'
        elif ec in Means:
            return '방법/수단'
        elif ec in Background:
            return '배경'
        else:
            return '구분 불가'

# 연결 어미 구분
    def find_EC_type(self, verb, count):
        morphList = self.makeList()
        # print(morphList)
        aumy = ""
        ec = ""
        newMorphList = morphList[count + 1:]
        # print(newMorphList)
        for i, morphs in enumerate(newMorphList):
            if verb == morphs[0][0]:
                # VC 마지막이 EC인 경우
                if morphs[-1][1] == 'EC':
                    ec = morphs[-1][0]
                    aumy = self.which_ec(morphs[-1][0])
                    self.count = i
                else :
                    aumy = '연결 어미 없음'
        return ec, aumy