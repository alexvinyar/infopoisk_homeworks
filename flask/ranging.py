from math import log
from string import punctuation
import pymorphy2
import json
import os

k1 = 2.0
b = 0.75

def score_BM25(n, qf, N, dl, avdl):
    '''
    n - docs with word
    qf - freq in doc
    N - total docs
    dl - doc length
    avdl - average doc length
    '''
    K = compute_K(dl, avdl)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * qf) / (K + qf)
    return IDF * frac


def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))

def search(query):
    scores = {}
    morph = pymorphy2.MorphAnalyzer()
    articles = os.listdir('./articles_lemmatized')
    N = len(articles)
    avdl = float(open('avdl.txt','r',encoding='utf-8-sig').read())
    with open('stopwords.txt','r',encoding='utf-8-sig') as f:
        stopwords = [x.strip() for x in f.readlines()]
    with open('index.json','r',encoding='utf-8-sig') as f:
        idx = json.loads(f.read())
    tokens = query.lower().split()
    lemmas = [morph.parse(x.strip(punctuation+'«»…'))[0].normal_form
              for x in tokens if x.strip(punctuation) not in stopwords]
    for lemma in lemmas:
        if lemma in idx:
            docs = idx[lemma]
            n = len(docs)
            for doc in docs:
                with open('./articles_lemmatized/'+doc,'r',encoding='utf-8-sig') as f:
                    link,title,text = f.read().split('\n=====\n')
                words = text.split()
                dl = len(words)
                qf = len([x for x in words if x == lemma])
                score = score_BM25(n, qf, N, dl, avdl)
                if (link,title) not in scores:
                    scores[(link,title)] = score
                else:
                    scores[(link,title)] += score
    ranged_docs = sorted(scores.items(),key=lambda x: x[1],reverse=True)
    ranged_docs = [x[0] for x in ranged_docs]
    return ranged_docs[:10]