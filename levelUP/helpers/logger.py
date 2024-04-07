""" console logger helper """
from time import localtime, strftime


def log(title: str = 'levelUP App', msg: str = 'By 6488004 & 6488089'):
    """ log any title and msg given with local time of the server 

    e.g. `>>[2024.04.07 @15:39:18]: title: msg` """
    print(f">>[{strftime('%Y.%m.%d @%H:%M:%S', localtime())}]:",
          f"{title}: {msg}")
