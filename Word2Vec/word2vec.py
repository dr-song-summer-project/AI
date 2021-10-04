from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import KeyedVectors
from tqdm import tqdm
from visualizing_word2vec import *

corpus_fname = '../data/TrainData/unlabeled_data.txt'
model_fname = '../data/KeywordEmbedding/embedding_word2vec'

class callback(CallbackAny2Vec):
    """Callback to print loss after each epoch."""

    def __init__(self):
        self.epoch = 0
        self.loss_to_be_subed = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subed
        self.loss_to_be_subed = loss
        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.epoch += 1

def generate_model():
    print('corpus 생성')
    corpus = [sent.strip().split(" ") for sent in tqdm(open(corpus_fname, 'r', encoding='utf-8').readlines())]
    print("학습 중")
    # 5번 반복, size = 100(임베딩 차원 수 100), cpu 쓰레드 수 = 4, skip gram 설정
    model = Word2Vec(corpus, size=100, workers=4, sg=1, compute_loss=True, iter=5)
    model.wv.save_word2vec_format(model_fname)
    print('완료')


generate_model()

# 모델을 로딩하여 가장 유사한 단어를 출력
loaded_model = KeyedVectors.load_word2vec_format(model_fname) # 모델 로드
print(loaded_model.wv.vectors.shape)
print(loaded_model.wv.most_similar("연락", topn=5))
print(loaded_model.wv.most_similar("별로", topn=5))
print(loaded_model.wv.similarity("시간", '약속'))
# print(loaded_model.wv.most_similar(positive=['어벤져스', '아이언맨'], negative=['스파이더맨'], topn=1))

model_name = model_fname
model = KeyedVectors.load_word2vec_format(model_name)

vocab = list(model.wv.vocab)
X = model[vocab]

# sz개의 단어에 대해서만 시각화
sz = 800
X_show = X[:sz, :]
vocab_show = vocab[:sz]

# show_tsne()
show_pca()