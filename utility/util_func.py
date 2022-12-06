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
        return 'Positive sentiment'
    elif compound > -0.05 and compound < 0.05:
        return 'Neutral sentiment'
    elif compound <= -0.05:
        return 'Negative sentiment'

def filterTweet(text_tweet):
    keywords = ['live','livestream','live stream','match link','nft']
    for keyword in keywords:
        if keyword in text_tweet:
            return True
    return False