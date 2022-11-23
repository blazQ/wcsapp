import datetime
import getopt, sys
import logging

import pytz

from processing.tweet_processor import TweetProcessor
from utility import util_func

# Removing 1st argument from list of command line arguments
argumentList = sys.argv[1:]

# Options
options = 'n:s:e:t'

# Long options
long_options = ['National=', 'Start=', 'End=', 'Test']

# Esempio  di usage: recovery.py --National=argeng --Keywords=Messi,Kane --Start=16:00 --End=18:30 (--Test)
national = None
start = None
end = None
test_flag = False

try:
    # Individuo ogni coppia di opzioni e relativi argomenti
    opts, args = getopt.getopt(argumentList, options, long_options)
    for opt, arg in opts:
        if opt in ['-n', '--National']:
            national = arg
        elif opt in ['-s', '--Start']:
            start = arg
        elif opt in ['-e', '--End']:
            end = arg
        elif opt in ['-t', '--Test']:
            test_flag = True  # Se c'è l'opzione Test appende un identificatore al file

except getopt.error as e:
    logging.error(str(e))

# Almeno l'informazione sulla nazionale da cercare e sul lasso di tempo deve essere presente

if not national or not start or not end:
    logging.error('Must specify national team, start time and end time!')
    logging.error('Usage: recovery.py --National=national --Start=mm-ddThh:mm -End=mm-ddThh:mm')
    sys.exit(-1)

logging.info(f'Starting tweet retrieval of prediction about {national} starting {start} and ending {end}. Test '
             f'Flag: {test_flag}')



# Decodifico inizio e fine come tuple
start = util_func.decode_date(start)
end = util_func.decode_date(end)

# Tuple unpacking
monthS, dayS, hStart, mStart = start
monthEnd, dayEnd, hEnd, mEnd = end


# Creazione orari formattati
date_filter_beginning = datetime.datetime(2022, int(monthS), int(dayS), int(hStart), int(mStart), 00, tzinfo=pytz.utc)
date_filter_test_end = datetime.datetime(2022, int(monthEnd), int(dayEnd), int(hEnd), int(mEnd), 00, tzinfo=pytz.utc)

# Richiamo l'oggetto che processa i dati
tweetObj = TweetProcessor()

# Hashtag da monitorare
relevant_hashtags = ['Qatar2022',
                     'FIFAWorldCup',
                     'WorldCup',
                     'WC2022',
                     'QatarWorldCup2022',
                     ]
# File in cui scrivere
predictions_file = f'./test_results/tweet_predictions_{national}'
if test_flag:
    predictions_file += '_TEST_PREDICTIONS_BATCH'
predictions_file += '.csv'

filtered_tweets_test = tweetObj.get_tweets(relevant_hashtags,keywords=national,max_results_bound=100, bound=20,
                                           date_filter_lower=date_filter_beginning,
                                           date_filter_upper=date_filter_test_end)

tweetObj.write_tweets_csv(TweetProcessor.only_predictions(national,filtered_tweets_test),predictions_file )