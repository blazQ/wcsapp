from processing.tweet_processor import TweetProcessor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect,LangDetectException
from utility import util_func

# TODO: Iniziare a fare dei mock di medie salvataggi di informazioni di sentiment ecc.
# TODO: Scartare tweet di sponsorizzazione live delle partite
# TODO: Salvare i dati ottenuti in un csv con Nome nazione|Compund medio|Seniment|Numero di tweet (più eventuali altri campi)

tweetObj = TweetProcessor()
tweets = tweetObj.get_tweet_list_csv('test_results\\match\\tweet_CANMAR.csv')

Analyzer = SentimentIntensityAnalyzer()
compounds = []
for tweet in tweets:
    if tweet:
        try: #se il tweet è in inglese e non contiene parole proibite, allora lo consideriamo per la valutazione del sentiment
            if detect(tweet) == 'en' and util_func.filterTweet(tweet) == False:
                tweet = tweetObj.clean_tweet(tweet)
                polarity_dict = Analyzer.polarity_scores(tweet)
                #print("Raw sentiment dictionary : ", polarity_dict)
                compounds.append(polarity_dict['compound'])
        except LangDetectException : 
            continue    
print(f'Compound medio: {sum(compounds)/len(compounds)}, {util_func.sentimentValue(sum(compounds)/len(compounds))}')