import re
import tweepy
import datetime
import pytz

# Token per l'accesso alle API di Twitter
api_token = 'AAAAAAAAAAAAAAAAAAAAAOTujAEAAAAAyX1EGWg%2FgxFP%2Bvtq4MD4Ro%2BhvhI' \
            '%3DwcWzJBmMeTJbzuXDHguk8yQY6miHUeIzQ211suzm6Jci7L5LwO '



'''
    Funzione realizzata per ottenere tutti i Tweet sul mondiale a partire da una lista di hashtag.
    Restituisce una lista di oggetti Tweet per l'uso generico.
'''


def get_tweets(hashtags):
    client = tweepy.Client(bearer_token=api_token)

    query = ''

    # Se il valore passato è una lista di hashtag, li concateniamo
    if type(hashtags) is list:
        # Constructing query from hashtag list

        for i in range(len(hashtags) - 1):
            query += f'#{hashtags[i]} OR '

        query += f'#{hashtags[len(hashtags) - 1]} -is:retweet lang:en'
    # Altrimenti è un singolo hashtag

    else:
        query += f'#{hashtags} -is:retweet lang:en'

    raw_tweets = tweepy.Paginator(client.search_recent_tweets, query,
                                  tweet_fields=['context_annotations', 'created_at'],
                                  max_results=100).flatten(limit=10)
    return raw_tweets


'''
    Filtra una lista di tweet in base a un criterio temporale.
    Viene passato come filtro una data  specifica.
'''


def filter_tweets_by_date(unfiltered_tweets, date_filter):
    filtered_tweets = []

    if not date_filter:
        return unfiltered_tweets
    else:
        for tweet in unfiltered_tweets:
            if date_filter < tweet.created_at:  # per filtrare i tweet fatti il giorno dopo della partita
                filtered_tweets.append(tweet)
        return filtered_tweets


'''
    Nuova sintassi di invocazione si limita a unire le due funzioni:
    
    date_filter_test = datetime.datetime(2022, 11, 17, 00, 00, 00, tzinfo=pytz.utc)
    
    tweets = filter_tweets_by_date(get_tweets('qatecu'), date_filter_test) -> Concatenazione funzioni
    
    for tweet in tweets:
        print(tweet)
'''
