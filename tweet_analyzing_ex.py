from processing.tweet_processor import TweetProcessor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect

# TODO: Iniziare a fare dei mock di medie salvataggi di informazioni di sentiment ecc.

tweetObj = TweetProcessor()
tweets = tweetObj.get_tweet_list_csv('test_results\\tweet_Example1.csv')

Analyzer = SentimentIntensityAnalyzer()

for tweet in tweets:
    if tweet:
        print(detect(tweet))
        polarity_dict = Analyzer.polarity_scores(tweet)
        print("Raw sentiment dictionary : ", polarity_dict)
