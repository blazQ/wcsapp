import spacy

def decode_date(argument_date: str) -> tuple[str, str, str, str]:
    # Divido la data dal tempo
    date, time = argument_date.split(sep='T')
    # Divido mesi dai giorni
    month, day = (date.split(sep='-'))
    # Divido ore da minuti
    hrs, mnt = (time.split(sep=':'))
    return month, day, hrs, mnt

def sentimentValue(compound):
    if compound >= 0.05:
        return 'pos'
    elif compound > -0.05 and compound < 0.05:
        return 'neu'
    elif compound <= -0.05:
        return 'neg'

def calculateScore(compound,verified):
    '''
    if sentiment == 'pos':
        score = compound * 2
    elif sentiment == 'neg':
        score = compound * 1.5
    else: #allora significa che è neutro
        return compound
    '''
    if verified == 'True':
        score = compound * 1
    else:
        score = compound * 1.5
    return score

def filterTweet(text_tweet):
    keywords = ['live','livestream','live stream','match link','nft','bitcoin','straming','stream']
    for keyword in keywords:
        if keyword in text_tweet.lower() or text_tweet.startswith('RT',0,2):
            return True
    return False

def getCountry(text_tweet):
    countriesWC = ['australia','iran','japan','qatar','saudi arabia','korea','canada','costa rica','mexico','united states','usa','argentina','brazil','ecuador','uruguay','belgium',
                'croatia','denmark','england','france','germany','netherlands','poland','portugal','serbia','spain','switzerland','wales','morocco','cameroon','tunisia','senegal','ghana']
    NER = spacy.load("en_core_web_sm")
    text1= NER(text_tweet)
    countries = []
    for word in text1.ents:
        #Se fra le parole viene trovata una nazione essa avrà etichetta GPE
        if word.label_ == 'GPE' and word.text.lower() in countriesWC:
            countries.append(word.text.lower())
    return countries

def get_match_abbr(filename):
    match = filename.split('tweet_')
    match = match[1].split('.csv')[0]
    return match