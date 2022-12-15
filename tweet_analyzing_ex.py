import logging
from pathlib import Path
from processing.tweet_processor import TweetProcessor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect,LangDetectException
from utility import util_func
import spacy
from spacy import displacy
import csv

def get_sentiment_score(filename,home,away):

    tweetObj = TweetProcessor()
    tweets = tweetObj.get_tweet_list_csv(filename)
    Analyzer = SentimentIntensityAnalyzer()

    #Utilizziamo due dizionari, uno per accumulare lo score man mano che otteniamo i sentiment di ogni tweet
    countries_score = {}
    #il secondo per mantenere il conteggio del numero di tweet per ogni nazione
    countries_numtweets = {}

    #inizializziamo i dizionari utilizzando come chiave la squadra di casa e quella ospite
    countries_score[home] = 0
    countries_score[away] = 0

    countries_numtweets[home] = 0
    countries_numtweets[away] = 0
    '''
    Per ogni tweet andiamo a controllare se è in inglese, se lo è calcoliamo il sentiment con VADER
    '''
    for tweet in tweets:
        try:
            if detect(tweet[0]) == 'en':
                #utilizziamo spacy per cercare le nazioni di cui si parla nel tweet
                countries = util_func.getCountry(tweet[0])
                
                polarity_dict = Analyzer.polarity_scores(tweet[0])
                tweet_compound = polarity_dict['compound']
                #sentiment = util_func.sentimentValue(tweet_compound)
                '''
                Per ogni nazione trovata nel tweet che stiamo considerando, controlliamo se si sta parlando della
                squadra che gioca in casa oppure ospite (non ci interessano eventuali tweet di altre squadre), in
                tal caso andiamo ad aggiornare i dati dei dizionari
                '''
                for country in countries:
                    if country == home.lower() or country == away.lower():

                        #incrementiamo il contatore del tweet per la squadra trovata
                        countries_numtweets[country] += 1

                        #ora aggiorniamo lo score del sentiment per la sqaudra trovata
                        countries_score[country] += util_func.calculateScore(tweet_compound,tweet[1])
        except LangDetectException:
            continue

    print(f"Sentiment squadre: {countries_score}")
    print(f"Numero di tweet per squadra: {countries_numtweets}")
    '''
    Terminata l'analisi di tutti i tweet per la partita, aggiorniamo i valori nel dizionario che contiene lo score totale
    in modo da tener conto del numero dei tweet trovati per la squadra.
    Scorriamo il dizionario che contiene il numero di tweet per squadra e ci prendiamo il numero di tweet
    della squadra di casa e di quella ospite.
    '''
    #TODO: eliminare for, avendo home e away sappiamo già al campo da accedere al dizionario
    #prediamo il numero di tweet della sqaudra di casa e della sqaudra ospite
    tweets_home = int(countries_numtweets[home])
    tweets_away = int(countries_numtweets[away])
    
    if isinstance(tweets_home,int) and isinstance(tweets_away,int): 
        #aggiorniamo lo score tenendo conto del numero di tweet
        score_home = countries_score[home]
        score_home = score_home/(tweets_home + tweets_away)
       
        score_away = countries_score[away]
        score_away = score_away/(tweets_home + tweets_away)

    #se il file è stato già creato settiamo una variable a True in modo da non riscrivere l'header
    csvFile = Path(filename)
    if csvFile.is_file():
        header = False
    else:
        header = True

    with open('sentiment_results.csv','a',encoding='utf-8') as csv_file:
        tweetwriter = csv.writer(csv_file, delimiter='æ')
        if header == True:
            tweetwriter.writerow(['MATCH','HOME SENTIMENT SCORE','AWAY SENTIMENT SCORE'])
        tweetwriter.writerow([util_func.get_match_abbr(filename),score_home,score_away])

with open('utility/match.txt','r',encoding='utf-8') as f:
    for line in f:
        match_abbr,countries = line.split('|')
        home,away = countries.split(',')
        filename = f'test_results/match_filtered/tweet_{match_abbr}.csv'
        get_sentiment_score(filename,home.rstrip(),away.rstrip())