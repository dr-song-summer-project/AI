# import preprocess
import pandas as pd
from tqdm.notebook import tqdm
from pandas.io.parsers import read_csv
from keyword_convert import read_file, remove_tag

class readFile:
    def __init__(self):
        self.path_train = 'data/train_data.csv'
        self.df = pd.read_csv(self.path_train)
    
    def getContent(self):
        return self.df['reviewContent']

    def to_csv(self, content):
        self.df['reviewContent'] = content
        self.df.to_csv('src/train_prepro.csv', index=False)

def preprocessing():
    read = readFile()
    prepro = preprocess.Preprocess(read.getContent())
    read.to_csv(prepro.proprocess())
    # prepro.spell_text()

def filter_keyword():
    path = 'G:/내 드라이브/닥터송 여름 프로젝트/4. 대-스타 해결 2/DRSONG_AI_Project/AI/전처리/data/data_beforeKeywordFilter.xlsx'
    sentence = read_file(path)
    convert_keyword = []
    for i in tqdm(range(0, len(sentence))) :
        # convert_keyword.append(keyword_(sentence[i]))
        convert_keyword.append(remove_tag((sentence[i])))
    print(convert_keyword)

    df = pd.DataFrame([ x for x in convert_keyword])
    df.to_excel('G:/내 드라이브/닥터송 여름 프로젝트/4. 대-스타 해결 2/DRSONG_AI_Project/AI/전처리/src/unlabeled_data_keyword.xlsx', sheet_name='sentence')

if __name__ == '__main__' :
    filter_keyword()