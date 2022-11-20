from processing.TweetProcessor import TweetProcessor
import datetime
import pytz

date_filter_beginning = datetime.datetime(2022, 11, 20, 16, 00, 00, tzinfo=pytz.utc)
date_filter_test_end = datetime.datetime(2022, 11, 20, 20, 00, 00, tzinfo=pytz.utc)
tweetObj = TweetProcessor()

max_queries = 5

match = 'qatecu'

relevant_hashtags = ['Qatar2022',
                     'FIFAWorldCup',
                     'WorldCup',
                     'WC2022',
                     'QatarWorldCup2022',
                     match
                     ]

match_file = f'test_results/tweet_{match}.csv'

filtered_tweets_test = tweetObj.get_tweets(relevant_hashtags, max_results_bound=100, bound=20,
                                           date_filter_lower=date_filter_beginning,
                                           date_filter_upper=date_filter_test_end)
tweetObj.write_tweets_csv(filtered_tweets_test, match_file)
