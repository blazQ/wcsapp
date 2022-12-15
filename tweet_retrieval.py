import datetime
import getopt, sys
import logging

import pytz

from processing.tweet_processor import TweetProcessor
from utility import util_func

# Removing 1st argument from list of command line arguments
argumentList = sys.argv[1:]

# Options
options = 'm:k:s:e:t'

# Long options
long_options = ['Match=', 'Keywords=', 'Start=', 'End=', 'Test']

# Esempio  di usage: recovery.py --Match=argeng --Keywords=Messi,Kane --Start=16:00 --End=18:30 (--Test)
match = None
keywords = None
start = None
end = None
test_flag = False

try:
    # Individuo ogni coppia di opzioni e relativi argomenti
    opts, args = getopt.getopt(argumentList, options, long_options)
    for opt, arg in opts:
        if opt in ['-m', '--Match']:
            match = arg
        elif opt in ['-k', '--Keywords']:
            keywords = arg.split(sep=',')
        elif opt in ['-s', '--Start']:
            start = arg
        elif opt in ['-e', '--End']:
            end = arg
        elif opt in ['-t', '--Test']:
            test_flag = True  # Se c'è l'opzione Test appende un identificatore al file


except getopt.error as e:
    logging.error(str(e))

# Almeno l'informazione sul match e sul lasso di tempo deve essere presente

if not match or not start or not end:
    logging.error('Must specify match, start time and end time!')
    logging.error('Usage: recovery.py --Match=match --Keywords=k1,k2 --Start=mm-ddThh:mm -End=mm-ddThh:mm')
    sys.exit(-1)

logging.info(f'Starting tweet retrieval for {match}  focusing on {keywords} starting {start} and ending {end}. Test '
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
                     match
                     ]
# File in cui scrivere
match_file = f'./test_results/tweet_{match}'
if test_flag:
    match_file += '_TEST_BATCH'
match_file += '.csv'

# Ottengo la lista di tweet filtrati
filtered_tweets_test = tweetObj.get_tweets(relevant_hashtags, keywords=keywords, max_results_bound=100, bound=20,
                                           date_filter_lower=date_filter_beginning,
                                           date_filter_upper=date_filter_test_end)
# Scrivo nel file
tweetObj.write_tweets_csv(filtered_tweets_test, match_file)

# Scrivo un nuovo file filtrando tutti i tweet
TweetProcessor.csv_filtering(match_file)
