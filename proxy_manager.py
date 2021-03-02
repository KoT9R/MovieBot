import requests


class ProxyAssistant:
    def __init__(self):
        self.proxy = ""
        self.proxy_index = -1
        self.proxy_list = []
        self.get_proxy_list()

    def get_proxies(self):
        proxies = {
            "http": self.proxy,
            "https": self.proxy
        }
        return proxies

    def update_proxy(self):
        """Function changes proxy server"""
        self.proxy_index += 1
        if self.proxy_index == len(self.proxy_list):
            print("Прокси закончились")
            print("Попробуем найти новые")
            proxy_ip_with_port = self.get_another_proxy()
            print("Прокси обновлен " + proxy_ip_with_port)

            self.proxy = f'http://{proxy_ip_with_port}'
            return self.proxy

        proxy_ip_with_port = self.proxy_list[self.proxy_index]

        print("Прокси обновлен " + proxy_ip_with_port)

        self.proxy = f'http://{proxy_ip_with_port}'
        return self.proxy

    @staticmethod
    def get_another_proxy():
        """When the proxy list is over, the function asks for new ones from another service"""
        proxy_response = requests.get("https://api.getproxylist.com/proxy?protocol[]=http", headers={
            'Content-Type': 'application/json'
        }).json()

        ip = proxy_response['ip']
        port = proxy_response['port']
        proxy = f'{ip}:{port}'

        return proxy

    def get_proxy_list(self):
        """Gets a proxy list."""
        proxy_response = requests.get("http://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo")
        self.proxy_list = proxy_response.text.split("\n")
