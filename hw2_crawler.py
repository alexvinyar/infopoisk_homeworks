import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime
import os

def get_page(link):
    p = requests.get(link)
    if p:
        return p.text
    else:
        return None

def download_page(page,idx,link):
    soup = BeautifulSoup(page,'lxml')
    title = soup.find('h1').get_text()
    date = parse(soup.find('time')['datetime']).strftime('%d.%m.%Y')
    author = soup.select('div[class=author] a')
    if author:
        author = author[0].get_text()
    else:
        author = 'Noname'
    cats = [a.get_text() for a in soup.select('div[class=terms]')[0].findAll('a')]
    text = '\n'.join([x.get_text() for x in soup.select('div[class=content] p')])
    with open('articles/'+str(idx)+'.txt','w',encoding='utf-8-sig') as f:
        f.write('@au '+author+'\n')
        f.write('@ti '+title+'\n')
        f.write('@da '+date+'\n')
        f.write('@topic '+', '.join(cats)+'\n')
        f.write('@url '+link+'\n')
        f.write(text)
    
    

def crawl():
    n = 0
    if not os.path.exists('articles'):
        os.makedirs('articles')
    main_page = 'http://www.pravda-news.ru'
    p = get_page(main_page)
    soup = BeautifulSoup(p,'lxml')
    latest = soup.select('h3 > a')[0]['href']
    idx = int(latest.split('/')[-1].split('.')[0])
    while n < 1000:
        link = 'http://www.pravda-news.ru/topic/{}.html'.format(idx)
        p = get_page(link)
        if p is not None:
            print(link)
            download_page(p,idx,link)
            n += 1
        idx -= 1

crawl()
