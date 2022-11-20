from processing.TweetProcessor import TweetProcessor
import datetime
import pytz


tweetObj = TweetProcessor()
tweetObj.read_tweets_csv('test_results\\tweetExample.csv')