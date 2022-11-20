from processing.TweetProcessor import TweetProcessor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


tweetObj = TweetProcessor()
tweets = tweetObj.read_tweets_csv_text('test_results\\tweetExample.csv')

Analyzer = SentimentIntensityAnalyzer()

for tweet in tweets:
    polarity_dict = Analyzer.polarity_scores(tweet)
    print("Raw sentiment dictionary : ", polarity_dict)

text = 'Qatar sucks'
print(Analyzer.polarity_scores(text))
