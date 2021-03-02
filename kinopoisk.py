import requests

from proxy_manager import ProxyAssistant
from config import HEADERS_KINO
from bs4 import BeautifulSoup
from requests import get


class KinopoiskInfo(object):
    url_kinopoisk = "https://www.kinopoisk.ru"
    check_name_movie = True
    check_is_film = "актеры"
    url = "https://www.kinopoisk.ru/index.php"
    proxy = ProxyAssistant()
    query = "?kp_query="

    def clear_data(self):
        self.__init__()

    def __init__(self):
        """
        The main characteristics of the film
        """
        self.film_name = None
        self.image = None
        self.info = None
        self.url_watch = None
        self.url_trailer = None
        self.good_review = None
        self.bad_review = None
        self.time = None
        self.rating = {}
        self.money = None
        self.url_film = None
        self.country = None
        self.genre = None
        self.director = None
        self.actors = None
        self.year = None

    def __get_url__(self, soup) -> str:
        """
        Gets a link to the found movie.
        """
        name = soup.find("p", {"class": "name"})
        attributes = name.find("a").attrs
        url_film = attributes.get("href")
        return url_film

    def fast_finded_movie_case(self, soup) -> bool:
        """
        Handles the case when "Kinopoisk" immediately opened the page of the requested
        """
        fast_find = soup.find("title")
        if fast_find is not None:
            title = fast_find.contents[0].lower()
            if self.film_name in title:
                if not title.startswith(self.film_name):
                    self.check_name_movie = False
                self.url_film = ""
                self.url_film = self.url + self.query + self.film_name
                return True
        return False

    def check_section(self, soup) -> bool:
        """
        Checks if the block is a block with a movie, not a block with an actor.
        """
        try:
            if self.check_is_film in soup.find("a") or\
                    self.check_is_film in soup.find("li"):
                return True
            else:
                return False
        except TypeError:
            return False

    def search(self):
        """
        Searches for the most popular movie request on the Kinopoisk search site.
        Returns a link to a movie if there is a movie on the page, otherwise None.
        """
        global req
        flag = True
        count = 0
        while True:
            try:
                count += 1
                req = get(self.url, params={'kp_query': self.film_name}, headers=HEADERS_KINO,
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
        soup = BeautifulSoup(req.text, "lxml")
        most_wanted = soup.find('div', {'class': "element most_wanted"})

        if most_wanted is None:
            ans = self.fast_finded_movie_case(soup)
        else:
            ans = False

        if most_wanted is None and not ans:
            return False
        elif ans:
            return True

        if self.check_section(most_wanted):
            self.url_film = self.url_kinopoisk + self.__get_url__(most_wanted)
        else:
            self.check_name_movie = False
            search_result = soup.find("div", {"class": "search_results search_results_last"})
            first_find = search_result.find("div", {"class": "element"})
            if self.check_section(first_find):
                self.url_film = self.url_kinopoisk + self.__get_url__(first_find)
            else:
                return False
        return True

    def check_name(self) -> bool:
        """
        Checks if the request from the user matches the movie found.
        """
        return self.check_name_movie

    def parse_image(self, poster):
        """
        Looking for a poster on the site Kinopoisk
        """
        imag = poster.find("img")
        if imag is None:
            self.image = poster.attrs.get("src")
        else:
            self.image = imag.attrs.get("src")

    def find_poster(self, soup):
        """
        This function is needed to handle the case when there is no movie poster.
        """
        poster = soup.find("a", {"class": "popupBigImage"})
        if poster is None:
            poster = soup.find("img", {"itemprop": "image"})
        return poster

    def parse_original_name(self, soup):
        """
        Finds the name of the full movie.
        """
        title = soup.find("div", {"class": "movie-info__content"})
        title = title.find("div", {"id": "headerFilm"})
        title = title.find("h1", {"class": "moviename-big"})
        self.film_name = title.text.strip()

    def parse_info(self, soup):
        """
        Finds and saves a movie description.
        """
        table = soup.find("td", {"colspan": "3"})
        div = table.find("div")
        if div is not None:
            self.info = div.contents[0]

    def parse_raiting(self, soup):
        """
        Finds and saves movie ratings.
        """
        try:
            table = soup.find("div", {"class": "block_2"})
            kino = table.find("span")
            imdb = table.find("div", {"style": "color:#999;font:100 11px tahoma, verdana"})
            self.rating.update({"kino": kino.text})
            imdb = imdb.text[5:10].strip()
            self.rating.update({"imdb": imdb})
        except AttributeError:
            self.rating.update({"kino": "Отсутсвует"})
            self.rating.update({"imdb": "Отсутсвует"})

    def parse_review(self, soup):
        """
        Finds and remembers the most popular good review and the most popular bad review of the film.
        """
        try:
            response_bad = soup.find("div", {"class": "response bad"})
            response_good = soup.find("div", {"class": "response good"})
            if response_bad is not None:
                response_bad = response_bad.find("span", {"class": "_reachbanner_"})
            if response_good is not None:
                response_good = response_good.find("span", {"class": "_reachbanner_"})
            if response_bad is not None:
                self.bad_review = response_bad.text
            if response_good is not None:
                self.good_review = response_good.text
        except AttributeError:
            return

    def parse_trailer(self, soup):
        """
        Searches for and remembers a movie trailer link.
        """
        try:
            table = soup.find("table", {"id": "trailerinfo"})
            trailer = table.find("a", {"class": "all"})
            if trailer is not None:
                self.url_trailer = self.url_kinopoisk + trailer.attrs.get('href')
        except AttributeError:
            return

    def parse_movie_info(self, soup):
        """
        Fills in the basic information about the film, such as country, year, director, etc.
        """
        table = soup.find("table", {"class": "info"})
        for i in table.find_all("tr"):
            try:
                if self.year is None:
                    if i.contents[1].text == 'год':
                        self.year = i.contents[3].text.strip()
                        continue

                if self.country is None:
                    if i.contents[1].text == 'страна':
                        self.country = i.contents[3].text.strip()
                        continue

                if self.director is None:
                    if i.contents[0].text == 'режиссер':
                        self.director = i.contents[1].text.strip()
                        continue
                    else:
                        continue

                if self.genre is None:
                    if i.contents[0].text == 'жанр':
                        genre = i.contents[1].text.strip().split()
                        if len(genre) == 1:
                            self.genre = genre
                        else:
                            self.genre = i.contents[1].text.strip().split()[:-1]
                        continue
                    else:
                        continue

                if self.time is None:
                    if i.contents[0].text == "время":
                        self.time = i.contents[1].text.strip()
                        continue
                    else:
                        continue
            except AttributeError:
                continue

    def fill_info(self, film_name):
        """
        The main function that fills all the fields of the class and calls all the parsings of the movie page.
        """
        self.clear_data()
        global req
        self.film_name = film_name
        ans = self.search()
        if ans is None:
            return None
        if not ans:
            return False
        else:
            while True:
                try:
                    req = get(self.url_film, headers=HEADERS_KINO, proxies=self.proxy.get_proxies(), timeout=5)
                    assert req.status_code == 200, 'request failed'
                except requests.Timeout as e:
                    print("Timeout Error")
                    self.proxy.update_proxy()
                except requests.ConnectionError:
                    print("Server not response")
                    return None
                except AssertionError:
                    print("Server not response")
                    return None
                finally:
                    soup = BeautifulSoup(req.text, "lxml")
                    poster = self.find_poster(soup)
                    if poster is not None:
                        break
                    else:
                        print("Captcha")
                        self.proxy.update_proxy()

            movie_info_table = soup.find("div", {"class": "movie-info__table-container"})
            self.parse_trailer(soup)
            self.parse_review(soup)
            self.parse_raiting(soup)
            self.parse_movie_info(movie_info_table)
            self.parse_image(poster)
            self.parse_info(soup)
            self.parse_original_name(soup)
        return True

    def get_main_info(self) -> dict:
        """
        Returns a movie data dictionary.
        """
        if self.info is None or self.info == "\n":
            self.info = "Описание отсутсвует"

        ans = {"image": self.image, "info": self.info, "name": self.film_name,
               "year": self.year, "genre": self.genre, "country": self.country,
               "raiting": self.rating, "time": self.time, "director": self.director,
               "bad_review": self.bad_review, "good_review": self.good_review, "trailer": self.url_trailer}
        return ans
