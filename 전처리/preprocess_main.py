import preprocess
import pandas as pd
from tqdm.notebook import tqdm
from pandas.io.parsers import read_csv
from keyword_convert import read_file, to_excel, keyword

class readFile:
    def __init__(self):
        self.path_train = 'data/unlabeled_data.csv'
        self.df = read_csv(self.path_train)
        print(self.df.head())
    
    def getContent(self):
        return self.df['reviewContent']

    def to_csv(self, content):
        self.df['reviewContent'] = content
        self.df.to_csv('src/unlabeled_data_prepro.csv', index=False, encoding='utf-8')

    def to_tsv(self, content):
        self.df['reviewContent'] = content
        # DataFrame 이나 Serises 를 txt 파일로 깔끔하게 바꿀경우 (이건 tsv)
        self.df.to_csv('src/test_data_prepro.txt', index=False, sep="\t", encoding='utf-8')


def preprocessing():
    read = readFile()
    print('readFile done')
    prepro = preprocess.Preprocess(read.getContent())
    print('prepro done')
    read.to_csv(prepro.proprocess())
    print('to_csv done')

def get_keyword():
    path = 'data/unlabeled_data_prepro_keywordTemp.xlsx'
    sentence = read_file(path)
    convert_keyword = []
    for i in tqdm(range(0, len(sentence))) :
        convert_keyword.append(keyword(sentence[i]))  #파이참에서 Okt가 실행되지 않아 Colab에서 진행 후 파일 업로드
        # convert_keyword.append(remove_tag((sentence[i])))
    print(convert_keyword)
    df = pd.DataFrame([ x for x in convert_keyword])
    df.to_excel('src/train_data_keyword.xlsx', sheet_name='sentence')

if __name__ == '__main__' :
    preprocessing()
    # get_keyword()
