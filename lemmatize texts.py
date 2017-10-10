import pymorphy2
from string import punctuation
import os
import json

def create_index(docs):
    final_index = {}
    for d in docs:
        for term in docs[d]:
            if term not in final_index:
                final_index[term] = [d]
            else:
                final_index[term].append(d)
    return final_index

def process_texts():
    '''
    из папки со статьями - папка с лемматизированными текстами статей и ссылками
    и обратный индекс
    '''
    collection = {}
    lengths = []
    morph = pymorphy2.MorphAnalyzer()
    if not os.path.exists('./articles_lemmatized'):
        os.makedirs('./articles_lemmatized')
    with open('stopwords.txt','r',encoding='utf-8-sig') as f:
        stopwords = [x.strip() for x in f.readlines()]
    articles = os.listdir('./articles')
    for filename in articles:
        with open('./articles/'+filename,'r',encoding='utf-8-sig') as f:
            text = ''
            for line in f.readlines():
                if line.startswith('@url'):
                    url = line.replace('@url ','').strip()
                elif line.startswith('@ti'):
                    title = line.replace('@ti ','').strip()
                elif not line.startswith('@'):
                    text += line
        tokens = text.lower().split()
        lemmas = [morph.parse(x.strip(punctuation+'«»…'))[0].normal_form
                  for x in tokens if x.strip(punctuation) not in stopwords]
        lengths.append(len(lemmas))
        with open('./articles_lemmatized/'+filename,'w',encoding='utf-8-sig') as f:
            f.write(url+'\n=====\n'+title+'\n=====\n'+' '.join(lemmas))
        collection[filename] = lemmas
    idx = create_index(collection)
    obj = json.dumps(idx,ensure_ascii=False,indent=2)
    with open('index.json','w',encoding='utf-8-sig') as f:
        f.write(obj)
    with open('avdl.txt','w',encoding='utf-8-sig') as f:
        f.write(str(sum(lengths) / len(lengths)))

process_texts()
