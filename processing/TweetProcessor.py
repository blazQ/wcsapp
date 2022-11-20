import csv
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
        Restituisce una lista di oggetti Tweet per l'uso generico.
        Bound rappresenta il limite di tweet da raccogliere.
    '''

    # TODO: Aggiornare la funzione get_tweets per avere parti della query che non sono hashtags (per esempio per
    #  cercare i tweet coi nomi dei giocatori)

    # TODO: Aggiornare la funzione get_tweets per usare la richiesta e la risposta invece del paginator per prendere
    #  campi non inclusi nel flatten
    def get_tweets(self, hashtags, max_results_bound: int = 100, bound: int = 10):
        client = tweepy.Client(bearer_token=self.api_token)

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

        try:
            raw_tweets = tweepy.Paginator(client.search_recent_tweets, query,
                                          tweet_fields=['context_annotations', 'created_at', 'author_id'],
                                          max_results=max_results_bound).flatten(limit=bound)
        except tweepy.TweepyException as e:
            print('Error : ' + str(e))

        return raw_tweets

    def clean_tweet(self, tweet):
        '''
        Rimuove link, caratteri speciali usando le regex.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet).split())

    '''
        Filtra una lista di tweet in base a un criterio temporale.
        Viene passato come filtro una data  specifica.
        NUOVA IMPLEMENTAZIONE: I filtri vengono implementati come parametro opzionali, valore default: None. 
        Questo consente di chiamare la funzione senza specificarli. 
        Modifica nell'ottica del riutilizzo della funzione con più di un filtro.
        Nel caso la funzione venga chiamata senza filtri restituisce la lista di partenza.
        La logica della funzione è contorta per permettere la presenza di diverse combinazioni di filtri.
        Gli id dei tweet spam vanno acquisiti.
    '''

    def filter_tweets(self, unfiltered_tweets, date_filter_lower=None, date_filter_upper=None, ad_filter: dict = None):
        filtered_tweets = []

        for tweet in unfiltered_tweets:  # Per ogni tweet della lista non filtrata

            add_flag = True  # Assumi debba essere aggiunto, da precondizioni

            if date_filter_lower:  # Se c'è un lower bound per la data (cioé vogliamo tutti i tweet dopo una certa data)

                if date_filter_lower > tweet.created_at:  # Ma il tweet è prima di quella data
                    add_flag = False  # Non aggiungere

            if date_filter_upper and add_flag:  # Se hai passato il controllo precedente e c'è un filtro per l'upper bound

                if date_filter_upper < tweet.created_at:  # Ma il tweet è dopo quella data
                    add_flag = False  # Non aggiungere

            if ad_filter and add_flag:  # Se hai passato tutti gli altri controlli, ma c'è un filtro per gli id di utenti AD

                if tweet.author_id in ad_filter.keys():  # E l'autore del tweet è un advertiser
                    add_flag = False  # Non aggiungere

            if add_flag:  # Se il flag di aggiunta è sopravvisuto
                filtered_tweets.append(tweet)  # Rispetta tutti i criteri, aggiungi

        return filtered_tweets

    # TODO: Aggiungere altri campi (IS VERIFIED e USER ID) richiede trattare la richiesta diversamente,
    #  cioé non usando il flatten ma utilizzando le risposte di ogni singola richiesta e analizzandola. Più
    #  complicata, decidiamo se farlo o mantenere semplicemente i tweet. todo2.
    def write_tweets_csv(self, filtered_tweets, file_handle):
        with open(file_handle, "w+", encoding="utf-8") as f:
            tweetwriter = csv.writer(f, delimiter='æ')

            tweetwriter.writerow(['TWEET', 'DATA'])

            for tweet in filtered_tweets:
                tweetwriter.writerow([tweet.text, tweet.created_at])

    # Legge il file CSV in modo classico. La frase da stampare la cambieremo quando ci salveremo tutti i campi. Ci ho
    # inserito una chiamata a clean tweet per farmeli stampare puliti, ovviamente la funzione la modificheremo in
    # base a ciò che ci serve
    def read_tweets_csv(self, file_handle):
        with open(file_handle, 'r', encoding='utf-8') as csv_file:
            tweet_reader = csv.reader(csv_file, delimiter='æ')
            for row in tweet_reader:
                if row:
                    print(f'({self.clean_tweet(row[0])}) created at ({row[1]})')

    # TODO: Gestione dei sondaggi
    # TODO: Prove con VADER
    # TODO: Regex per pulire i tweet e raccogliere le predizioni
