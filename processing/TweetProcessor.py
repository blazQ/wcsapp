import csv
import datetime
import pytz
import tweepy
import re


class TweetProcessor:
    def __init__(self,
                 api_token='AAAAAAAAAAAAAAAAAAAAAOTujAEAAAAAyX1EGWg%2FgxFP%2Bvtq4MD4Ro%2BhvhI'
                           '%3DwcWzJBmMeTJbzuXDHguk8yQY6miHUeIzQ211suzm6Jci7L5LwO'):

        # Token per l'accesso all'API di Twitter, il valore di default è la chiave di Gabriele, può essere
        # specificata un'altra chiave per uso futuro
        self.api_token = api_token

    '''
        Funzione realizzata per ottenere tutti i Tweet sul mondiale a partire da una lista di hashtag.
        Restituisce una lista di coppie (Oggetto Tweet, Oggetto Utente) che contiene il tweet e il suo autore.
        Bound rappresenta il limite di tweet da raccogliere.
    '''

    # TODO: Aggiornare la funzione per restituire il tweet intero, extended

    # TODO: Regex per pulire i tweet e raccogliere le predizioni

    def get_tweets(self, hashtags=None,keywords=None,max_results_bound: int = 100, bound: int = 10, date_filter_lower=None,
                   date_filter_upper=None):
        client = tweepy.Client(bearer_token=self.api_token)

        query = ''

        # Se il valore passato è una lista di hashtag, li concateniamo
        if type(hashtags) is list:
            # Constructing query from hashtag list
            query+='(' 
            for i in range(len(hashtags) - 1):
                query += f'#{hashtags[i]} OR '
            query += f'#{hashtags[len(hashtags) - 1]}) '
        # Altrimenti è un singolo hashtag
        elif type(hashtags) is str:
            query += f'#{hashtags}'

        # Se il valore passato è una lista di keywords, le concateniamo
        if type(keywords) is list:
            for i in range(len(keywords) - 1):
                query += f'{keywords[i]} OR '    

            query += f'{keywords[len(keywords) - 1]} '
        elif type(keywords) is str:
        # Altrimenti è una singola hkeyword
            query += f'{keywords} '

        #alla fine inseriamo i parametri opzionali alla query
        query += '-is:retweet lang:en'
        print(query)
        try:
            raw_tweets = tweepy.Paginator(
                client.search_recent_tweets,
                query=query,
                tweet_fields=['context_annotations', 'created_at', 'author_id'],
                user_fields=['verified'],
                expansions='author_id',
                start_time=date_filter_lower,
                end_time=date_filter_upper,
                max_results=max_results_bound,
                limit=bound
            )

            raw_tweets_tuples = []
            for rsp in raw_tweets:
                users = {u["id"]: u for u in rsp.includes['users']}
                for tweet in rsp.data:
                    if users[tweet.author_id]:
                        raw_tweets_tuples.append((tweet, users[tweet.author_id]))

        except tweepy.TweepyException as e:
            print('Error : ' + str(e))

        return raw_tweets_tuples

    @staticmethod
    def clean_tweet(tweet_text):
        """
        Rimuove link, caratteri speciali usando le regex.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet_text).split())

    @staticmethod
    def write_tweets_csv(filtered_tweets_tuples, file_handle):
        with open(file_handle, "a", encoding="utf-8") as f:
            tweetwriter = csv.writer(f, delimiter='æ')

            tweetwriter.writerow(['TWEET', 'AUTHOR_ID', 'VERIFIED', 'DATA'])

            for (tweet, user) in filtered_tweets_tuples:
                tweetwriter.writerow([tweet.text, tweet.author_id, user.verified, tweet.created_at])

    # Legge il file CSV in modo classico. La frase da stampare la cambieremo quando ci salveremo tutti i campi. Ci ho
    # inserito una chiamata a clean tweet per farmeli stampare puliti, ovviamente la funzione la modificheremo in
    # base a ciò che ci serve
    @staticmethod
    def read_tweets_csv(file_handle):
        with open(file_handle, 'r', encoding='utf-8') as csv_file:
            tweet_reader = csv.reader(csv_file, delimiter='æ')
            for row in tweet_reader:
                if row:
                    print(f'({TweetProcessor.clean_tweet(row[0])}) created by ({row[1]}) who is (verified: {row[2]}) '
                          f'on ({row[3]})')

    @staticmethod
    def get_tweet_list_csv(file_handle):
        with open(file_handle, 'r', encoding='utf-8') as csv_file:
            tweet_reader = csv.reader(csv_file, delimiter='æ')
            tweets = []
            for row in tweet_reader:
                if row:
                    tweets.append(row[0])
        return tweets
