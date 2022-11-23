def decode_date(argument_date: str) -> tuple[str, str, str, str]:
    # Divido la data dal tempo
    date, time = argument_date.split(sep='T')
    # Divido mesi dai giorni
    month, day = (date.split(sep='-'))
    # Divido ore da minuti
    hrs, mnt = (time.split(sep=':'))
    return month, day, hrs, mnt


