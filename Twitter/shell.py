import numpy as np
import pandas as pd
import re
import json
from os import listdir
from os.path import isfile, join
from TweetAnalyzer import *
#Extracting the campanies Twitter username
from Search import *
def url(company):
    try:
        s=seleniumSearch()
        url=s.get_urls(company)
        return url
    except:
        pass
def shell(url):
    L=[]
    name=''
    if url != None :
        # x is the url string
        try:
            c=url.split('?')[0]
        except :
            pass
        try:
            n=c.split('/')
            name=n[-1]
        except :
            pass
        if name not in L:    
            L.append(name)
    return L
def save(company):
    L=shell(url(company))
    for i in L :
        os.system('twint -u '+i+' -o '+i+'.json --json')
        return os.getcwd()
def filename(company):
    path=save(company)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for i in onlyfiles:
        if company.lower() in i.lower() and '.json' in i.lower():
            return i
def tanalyser(company):
    tweet_analyzer = TweetAnalyzer()
    res=[]
    tweetsdata = []
    tweets = []
    likes=0
    replies=0
    retweets=0
    path=filename(company)
    for line in open(path,'r',encoding="utf8"):
        tweetsdata.append(json.loads(line))
    for i in tweetsdata: 
        tweets.append(i["tweet"])
        likes=likes+int(i["likes_count"])
        replies=replies+int(i["replies_count"])
        retweets=retweets+int(i["retweets_count"])
    df = pd.DataFrame(data=[tweet for tweet in tweets], columns=['tweets'])
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    score=0
    for sent in df['sentiment']:
        score=score+int(sent)
        num=len(df['sentiment'])
    twitter_user=company
    res.append([twitter_user,score,num,likes,replies,retweets])
    final= pd.DataFrame(res, columns = ['twitter_user','twitter_score','tweets_num','twitter_likes','twitter_replies','twitter_retweets'])
    return final
