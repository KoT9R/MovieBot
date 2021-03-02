import requests
from requests import get
from proxy_manager import ProxyAssistant
from config import HEADERS_IVI
from config import HEADERS_GO
from config import IVI
from config import MEGOGO

SEARCH_MEGOGO = "/search-extended?q="
URL_MEGOGO = "https://megogo.ru/ru"

SEARCH_IVI = "/search/?q="
URL_IVI = "https://www.ivi.tv"


class Movie(object):
    proxy = ProxyAssistant()

    def __init__(self):
        self.film_url = None

    def find(self, name, service):
        """
        The function is used to check the serviceability of services. Returns the web address.
        """
        if service == MEGOGO:
            url = URL_MEGOGO
            search = SEARCH_MEGOGO
            headers = HEADERS_GO
        else:
            url = URL_IVI
            search = SEARCH_IVI
            headers = HEADERS_IVI
        flag = True
        while True:
            try:
                req = get(url + search + name, headers=headers,
                          proxies=self.proxy.get_proxies(), timeout=5)
                assert req.status_code == 200, 'request failed'
                flag = True
            except requests.Timeout:
                flag = False
                print("Timeout Error")
                self.proxy.update_proxy()
            except requests.ConnectionError:
                print("Server not response")
                return None
            except AssertionError:
                print("Server not response")
                return None
            finally:
                if flag:
                    break

        return url + search + name
