# import kss
from pykospacing import Spacing
from hanspell import spell_checker
from soynlp.normalizer import *
from tqdm import tqdm


###################전처리부######################
# Basic proprocessing : 태그 제거, "@%*=()/+ 와 같은 punctuation 제거
# Spell check(맞춤법, 띄어쓰기)
#  pip install git+https://github.com/haven-jeon/PyKoSpacing.git  : 띄어쓰기 검사
# pip install tensorflow
# pip install keras
# pip install git+https://github.com/ssut/py-hanspell.git         : 맞춤법 검사  **500자 이상 안됨


class Preprocess:
    def __init__(self, content):
        self.content = content
        self.punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
        self.punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x",
                              "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'",
                              '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/',
                              'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi',
                              "^": ""}
        self.rule = ['맘시터', '스케줄', '스케쥴', '시터', '시터분', '시터 분']  # 띄어쓰기 규칙

    def basic_Preprocessing(self, content, punct, mapping):  # html tag 제거, 숫자 제거, Lowercasing, punctuation 제거
        result = []
        for text in content:
            for p in mapping:
                text = text.replace(p, mapping[p])
            for p in punct:
                text = text.replace(p, f'{p}')
                text = text.replace('"', '')
                text = text.replace('&', ',')
                text = text.replace('@', '')
                text = text.replace(':)', '')
                text = text.replace('❤️', '')
                text = text.replace('☺️', '')
                text= text.replace('☺', '')

            specials = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', 'करना': '', 'है': ''}
            for s in specials:
                text = text.replace(s, specials[s])
            result.append(text.strip())
        return result

    def spell_check(self, content):  # 띄어쓰기, 맞춤법 검사, 반복되는 글자 제거
        spacing = Spacing(rules=self.rule)
        result = []
        for sent in tqdm(content):
            spaced_text = spacing(sent)
            try:
                spelled_sent = spell_checker.check(spaced_text)
            except:
                print('content :', spaced_text)
            checked_sent = spelled_sent.checked
            normalized_sent = repeat_normalize(checked_sent)
            if normalized_sent == '' :
                result.append(sent[:200]+' 글자 수 초과')
            else:
                result.append(normalized_sent)
        return result

    def spell_text(self):
        sent = "한글 맞춤법검사기 재대로작동돼는지테스트"
        spelled_sent = spell_checker.check(sent)
        checked_sent = spelled_sent.checked

        print(checked_sent)

    def proprocess(self):
        self.content = self.basic_Preprocessing(self.content, self.punct, self.punct_mapping)
        spell_content = self.spell_check(self.content)

        return spell_content

corpus = '저는 아이 돌보는 것을 참 좋아하는 학생입니다. 그런데 솔직히 너무 너무 힘들었어요. 아이가 자기하고싶은대로만 하려고 해서 혼내면 욕하고 때리려고하고.. 아이가 너무 폭력적이었어요. ' \
             '놀이터에 나가서도 다른 어린친구들 괴롭히려고 하는데 어찌해야할지 모르겠더라구요.'
tmp = Preprocess(corpus)
tmp.spell_text()