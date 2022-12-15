import csv
import os
import sys
from utility import util_func
import tweepy
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Bearer Keys
gabriele_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOTujAEAAAAAyX1EGWg%2FgxFP%2Bvtq4MD4Ro%2BhvhI' \
                        '%3DwcWzJBmMeTJbzuXDHguk8yQY6miHUeIzQ211suzm6Jci7L5LwO '
pietro_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOC9jwEAAAAASKimZd8aW1PcroOjmQz55aIdpSA' \
                      '%3D0uIhHfPOQy3Eof4HaPEhK6pCXtPQnFq4eo9WlnBQ9LNLJqfjn0 '


class TweetProcessor:
    def __init__(self,
                 api_token=pietro_bearer_token):

        # Token per l'accesso all'API di Twitter, il valore di default è la chiave di Gabriele, può essere
        # specificata un'altra chiave per uso futuro
        self.api_token = api_token

    '''
        Funzione realizzata per ottenere tutti i Tweet sul mondiale a partire da una lista di hashtag.
        Restituisce una lista di coppie (Oggetto Tweet, Oggetto Utente) che contiene il tweet e il suo autore.
        Bound rappresenta il limite di tweet da raccogliere.
    '''

    # TODO: Aggiornare la funzione per restituire il tweet intero, extended

    def get_tweets(self, hashtags=None, keywords=None, max_results_bound: int = 100, bound: int = 10,
                   date_filter_lower=None,
                   date_filter_upper=None):
        try:
            client = tweepy.Client(bearer_token=self.api_token)
        except tweepy.TweepyException as e:
            logging.error('Couldn''t get client object: ' + str(e))
            return None
        logging.info('Obtained reference to client object')

        query = ''

        # Se il valore passato è una lista di hashtag, li concateniamo
        if type(hashtags) is list:
            # Constructing query from hashtag list
            query += '('
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

        # alla fine inseriamo i parametri opzionali alla query
        query += '-is:retweet -is:quote -is:reply lang:en'

        logging.info(f'Query: {query}')

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
            logging.info('Paginator object received')

            raw_tweets_tuples = []
            for rsp in raw_tweets:
                users = {u["id"]: u for u in rsp.includes['users']}
                for tweet in rsp.data:
                    if users[tweet.author_id]:
                        raw_tweets_tuples.append((tweet, users[tweet.author_id]))

            logging.info('Coupled users and tweets')

        except tweepy.TweepyException as e:
            logging.error('Error : ' + str(e))

        return raw_tweets_tuples

    @staticmethod
    def clean_tweet(tweet_text):
        """
        Rimuove link e caratteri speciali tranne # usando le regex.
        """
        tweet_text =  re.sub(r"http\S+", "", tweet_text)
        tweet_text = re.sub('[^a-zA-Z0-9# \n\.]', '', tweet_text)
        return re.sub(' +', ' ', tweet_text)
        #return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet_text).split())

    '''
    Restituisce una lista di tuple contenente solamente i tweet con predizione della vincitrice dei mondiali
    '''

    @staticmethod
    def only_predictions(keyword, unfiltered_tweets):

        filtered_tweets = []
        # Scorriamo la lista di tuple tweet-utente e controlliamo se il testo del campo text è nel formato di una
        # predizione
        for (tweet, user) in unfiltered_tweets:
            '''In base alla keyword passata, controlla se la keyword è abbinata con le parole di predizione di 
            vincitrice del mondiale. Ignora se maiuscolo o minuscole e tollera più di un whitespace fra le due coppie 
            di parole. '''
            if re.search(
                    f'(?i){keyword}\s+(will\s+)?(win|wins|(be\s+)?world\s+champion|(be\s+)?champion|(be\s+)?champions|triumph)',
                    tweet.text) is not None:
                filtered_tweets.append(
                    (tweet, user))  # se troviamo un match inseriamo la tupla in una lista di tuple filtrate
        return filtered_tweets

    @staticmethod
    def write_tweets_csv(filtered_tweets_tuples, file_handle):
        with open(file_handle, "a", encoding="utf-8") as f:
            tweetwriter = csv.writer(f, delimiter='æ')

            tweetwriter.writerow(['TWEET', 'AUTHOR_ID', 'VERIFIED', 'DATA'])

            i = 1
            for (tweet, user) in filtered_tweets_tuples:
                tweetwriter.writerow([tweet.text.replace("\n", ""), tweet.author_id, user.verified, tweet.created_at])
                logging.info(f'(Wrote tweet no.{i} in {file_handle} )')
                i += 1

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
            i = 1
            for row in tweet_reader:
                if row:
                    tweets.append((row[0],row[2]))  # implica che la prima colonna di ogni riga contenga il testo del tweet
                    #logging.info(f'Tweet read no. {i}')
                    i += 1
        return tweets
    
    def csv_filtering(filename):
    #viene aperto il file csv da pulire
        with open(filename,'r',encoding='utf-8') as match_csv:
            #crea un nuovo file csv dove inserire i tweet filtrati
            with open(f'test_results/match_filtered/{os.path.basename(match_csv.name)}','a',encoding='utf-8') as filtered_csv:
                tweetwriter = csv.writer(filtered_csv, delimiter='æ')
                tweetwriter.writerow(['TWEET', 'AUTHOR_ID', 'VERIFIED', 'DATA'])
                
                tweet_reader = csv.reader(match_csv, delimiter='æ')
                
                for row in tweet_reader:
                    if row:
                        #controlliamo se ci sono keyword che indentificano tweet che vogliamo scartare e se la riga che stiamo considerando non è un intestazione
                        if util_func.filterTweet(row[0]) == False and row[0] != 'TWEET':
                            #inseriamo il tweet nel nuovo csv
                            tweetwriter.writerow([TweetProcessor.clean_tweet(row[0]), row[1], row[2], row[3]])
                   


