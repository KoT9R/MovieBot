import requests

HEADERS_KINO = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; '
                  'ru; rv:1.9.1.8) Gecko/20100214 '
                  'Linux Mint/8 (Helena) Firefox/'
                  '3.5.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              '*/*;q=0.8',
    'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
    'Accept-Encoding': 'deflate',
    'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Referer': 'http://www.kinopoisk.ru/',
    'Cookie': 'users_info[check_sh_bool]=none; '
              'search_last_date=2010-02-19; search_last_month=2010-02; '
              'PHPSESSID=b6df76a958983da150476d9cfa0aab18',
}

HEADERS_IVI = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; '
                  'ru; rv:1.9.1.8) Gecko/20100214 '
                  'Linux Mint/8 (Helena) Firefox/'
                  '3.5.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              '*/*;q=0.8',
    'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
    'Accept-Encoding': 'deflate',
    'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Referer': 'https://www.ivi.tv/',
    'Cookie': 'users_info[check_sh_bool]=none; '
              'search_last_date=2010-02-19; search_last_month=2010-02; '
              'PHPSESSID=b6df76a958983da150476d9cfa0aab18',
}

HEADERS_GO = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; '
                  'ru; rv:1.9.1.8) Gecko/20100214 '
                  'Linux Mint/8 (Helena) Firefox/'
                  '3.5.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              '*/*;q=0.8',
    'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
    'Accept-Encoding': 'deflate',
    'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive': '300',
    'Connection': 'keep-alive',
    'Referer': 'https://megogo.ru/ru/',
    'Cookie': 'users_info[check_sh_bool]=none; '
              'search_last_date=2010-02-19; search_last_month=2010-02; '
              'PHPSESSID=b6df76a958983da150476d9cfa0aab18',
}

MEGOGO = "MEGOGO"
IVI = "IVI"

