import csv
import tweepy

class TweetProcessing:
    def __init__(self):
        #Token per l'accesso all'API di Twitter
        self.api_token = 'AAAAAAAAAAAAAAAAAAAAAOTujAEAAAAAyX1EGWg%2FgxFP%2Bvtq4MD4Ro%2BhvhI%3DwcWzJBmMeTJbzuXDHguk8yQY6miHUeIzQ211suzm6Jci7L5LwO'

    '''
        Funzione realizzata per ottenere tutti i Tweet sul mondiale a partire da una lista di hashtag.
        Restituisce una lista di oggetti Tweet per l'uso generico.
        Bound rappresenta il limite di tweet da raccogliere.
    '''
    def get_tweets(self,hashtags, max_results_bound: int = 100, bound: int = 10):
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

        raw_tweets = tweepy.Paginator(client.search_recent_tweets, query,
                                    tweet_fields=['context_annotations', 'created_at'],
                                    max_results=max_results_bound).flatten(limit=bound)
        return raw_tweets


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
    def filter_tweets(self,unfiltered_tweets, date_filter_lower=None, date_filter_upper=None, ad_filter: dict = None):
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


# TODO: Strutturare efficacemente la struttura del file CSV. Proposto ae come carattere separatore in quanto non
#  presente in genere nei tweet inglesi. Bisogna definire bene anche i campi da salvare.
    def write_tweets_csv(self,filtered_tweets, file_handle):
        with open(file_handle, "w+", encoding="utf-8") as f:
            httpwriter = csv.writer(f, delimiter='æ')

            httpwriter.writerow(['TWEET', 'DATA'])

            for tweet in filtered_tweets:
                httpwriter.writerow([tweet.text, tweet.created_at])


