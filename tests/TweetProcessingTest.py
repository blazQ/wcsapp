from TweetProcessing import TweetProcessing
import datetime
import pytz
'''
   Test con un timeframe di esempio.
'''
date_filter_test = datetime.datetime(2022, 11, 18, 10, 00, 00, tzinfo=pytz.utc)
date_filter_test_2 = datetime.datetime(2022, 11, 19, 21, 00, 00, tzinfo=pytz.utc)
tweetObj = TweetProcessing()
filtered_tweets_test = tweetObj.filter_tweets(tweetObj.get_tweets('qatecu'),
                                     date_filter_lower=date_filter_test,
                                     date_filter_upper=date_filter_test_2)

tweetObj.write_tweets_csv(filtered_tweets_test, 'tweet.csv')