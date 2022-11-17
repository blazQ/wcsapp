import re
import tweepy
import datetime
import pytz

#per i tweet generici sul mondiale
def getTweets():
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAOTujAEAAAAAyX1EGWg%2FgxFP%2Bvtq4MD4Ro%2BhvhI%3DwcWzJBmMeTJbzuXDHguk8yQY6miHUeIzQ211suzm6Jci7L5LwO')

    query = '#FIFAWorldCup OR #Qatar2022 -is:retweet lang:en'
    tweets = tweepy.Paginator(client.search_recent_tweets,query, tweet_fields=['context_annotations', 'created_at'],max_results=100).flatten(limit=10000)
    '''
    for tweet in tweets:
        print(tweet.created_at) #for get the tweet creation date
        print(tweet.text) #for get the text
    '''
    return tweets

#tweet per partita
def getMatchTw(matchAbbr,filter):
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAOTujAEAAAAAyX1EGWg%2FgxFP%2Bvtq4MD4Ro%2BhvhI%3DwcWzJBmMeTJbzuXDHguk8yQY6miHUeIzQ211suzm6Jci7L5LwO')
    query = '#%s -is:retweet lang:en'%matchAbbr
    tweets = tweepy.Paginator(client.search_recent_tweets,query, tweet_fields=['context_annotations', 'created_at'],max_results=100).flatten(limit=10)
    tweetsLi = list(tweets)
    if filter == False: #da chiamare con false il giorno del pre-partita (?)
        return tweetsLi
    else:
        for tweet in tweetsLi:
            if filter > tweet.created_at: #per filtrare i tweet fatti il giorno dopo della partita
                tweetsLi.remove(tweet)
        return tweetsLi
'''        
filter = datetime.datetime(2022,11,17,12,00,00,tzinfo=pytz.utc)
tweets = getMatchTw('QATECU',filter)
for tweet in tweets:
    print(tweet.created_at) 
'''
