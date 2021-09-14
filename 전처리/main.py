import preprocess
import pandas as pd

class readFile:
    def __init__(self):
        self.path_train = 'data/train_data.csv'
        self.df = pd.read_csv(self.path_train)
    
    def getContent(self):
        return self.df['reviewContent']

    def to_csv(self, content):
        self.df['reviewContent'] = content
        self.df.to_csv('src/train_prepro.csv', index=False)

if __name__ == '__main__' :
    read = readFile()
    prepro = preprocess.Preprocess(read.getContent())
    read.to_csv(prepro.proprocess())
    # prepro.spell_text()