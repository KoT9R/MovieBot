import os
import re
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

from kinopoisk import KinopoiskInfo
from config import IVI
from config import MEGOGO
from movie_service import Movie

TOKEN = "934935672:AAHMxTnG1AeVDnofdZjlPECDU9WWBSHZW8o"
bot = telebot.TeleBot(TOKEN)

chat_id = None

BUTTON_BAD = 'bad_review'
BUTTON_GOOD = 'good_review'
BUTTON_TRAILER = 'trailer'
BUTTON_WATCH = 'watch'
BUTTON_MEGOGO = 'megogo'
BUTTON_IVI = "ivi"

TITLES = {
    BUTTON_BAD: 'Плохой отзыв',
    BUTTON_GOOD: 'Хороший отзывы',
    BUTTON_TRAILER: 'Трейлер',
    BUTTON_WATCH: 'Посмотреть',
    BUTTON_IVI: IVI,
    BUTTON_MEGOGO: MEGOGO,
}


def get_base_inline_keyboard():
    """
    Creates a keyboard with first requests.
    """
    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(
        InlineKeyboardButton(text=TITLES[BUTTON_BAD], callback_data=BUTTON_BAD),
        InlineKeyboardButton(text=TITLES[BUTTON_GOOD], callback_data=BUTTON_GOOD)
    )

    keyboard.row(
        InlineKeyboardButton(text=TITLES[BUTTON_TRAILER], url=url_trailer, callback_data=BUTTON_TRAILER),
    )

    keyboard.row(
        InlineKeyboardButton(text=TITLES[BUTTON_WATCH], callback_data=BUTTON_WATCH)
    )

    return keyboard


def get_keyboard2():
    """
    Creates a keyboard with movie services.
    """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text=TITLES[BUTTON_IVI], url=url_watch[1], callback_data=BUTTON_IVI),
        InlineKeyboardButton(text=TITLES[BUTTON_MEGOGO], url=url_watch[0], callback_data=BUTTON_MEGOGO),
    )
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """
    The function handles button presses.
    """
    if call.data == BUTTON_GOOD:
        if review_good is not None:
            try:
                bot.send_message(chat_id, text="Хороший отзыв:\n" + review_good)
            except Exception:
                bot.send_message(chat_id, text="Отзыв слишком большой, Telegram не разрешает его отправить :(")
        else:
            bot.send_message(chat_id, text="Отзыва об этом фильме нет :(")
    if call.data == BUTTON_BAD:
        if review_bad is not None:
            try:
                bot.send_message(chat_id, text="Плохой отзыв:\n" + review_bad)
            except Exception:
                bot.send_message(chat_id, text="Отзыв слишком большой, Telegram не разрешает его отправить :(")
        else:
            bot.send_message(chat_id, text="Отзыва об этом фильме нет :(")
    if call.data == BUTTON_TRAILER:
        if url_trailer is not None:
            bot.send_video(chat_id, url_trailer)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="Трейлера нет")
    if call.data == BUTTON_WATCH:
        if url_watch[0] is None:
            bot.send_message(chat_id, text="К сожалению сервис Megogo не доступен")
            return
        if url_watch[1] is None:
            bot.send_message(chat_id, text="К сожалению сервис IvI не доступен")
            return
        keyboard = get_keyboard2()
        bot.send_message(chat_id, text="Выберите на какой площадке будете смотреть фильм.\n"
                                       "P.S.: Примите к сведению,что данного фильма может "
                                       "и не быть на выбранной площадке", reply_markup=keyboard)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Function to send greetings.
    """
    bot.send_message(message.chat.id, "Привет! " + message.from_user.first_name + " Я бот для поиска фильмов,"
                                                                                  "я работаю на основе поиска "
                                                                                  "кинопоиска "
                                                                                  "и выдаю самый популярный запрос, "
                                                                                  "а также "
                                                                                  "информацию о фильме")
    bot.send_message(message.chat.id, "Команда /more - позволяет посмотреть трейлер фильма и сам фильм\n"
                                      "Команда /good_review - показывает хороший отзыв о фильме\n"
                                      "Команда /bad_review - показывает плохой отзыв о фильме")


@bot.message_handler(commands=["good_review"])
def good_review(message):
    if review_good is not None:
        bot.send_message(message.chat.id, text="Хороший отзыв:\n" + good_review)
    else:
        bot.send_message(message.chat.id, text="Отзыва об этом фильме нет :(")


@bot.message_handler(commands=["bad_review"])
def bad_review(message):
    if review_bad is not None:
        bot.send_message(message.chat.id, text="Плохой отзыв:\n" + review_bad)
    else:
        bot.send_message(message.chat.id, text="Отзыва об этом фильме нет :(")


def create_message(info: dict) -> str:
    """
    The function creates a full description of the movie.
    """
    ans = "{}, {}, {} \n" \
          "{}\n\n" \
          "{}\n\n" \
          "Рейтинг Кинопоиск: {} \n" \
          "Рейтинг IMDB: {} \n" \
          "Длительность: {} \n" \
          "Режисер: {} \n".format(info.get("name"), info.get("year"),
                                  info.get("country"), *info.get("genre"),
                                  info.get("info"), info.get("raiting").get("kino"),
                                  info.get("raiting").get("imdb"),
                                  info.get("time"), info.get("director"))
    return ans


def Send_URL(info):
    """
    Gets the url of web services.
    """
    ans = []
    movie = Movie()
    url_meg = movie.find(info.get("name"), MEGOGO)
    url_ivi = movie.find(info.get("name"), IVI)

    if url_ivi is not None and url_meg is not None:
        re.sub(" ", "+", url_ivi)
        re.sub(" ", "+", url_meg)
    ans.append(url_meg)
    ans.append(url_ivi)

    return ans


url_trailer, url_watch = None, None
review_bad, review_good = None, None


@bot.message_handler(commands=['more'])
def show_buttons_movie(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        ivi_but = types.InlineKeyboardButton(text="Посмотреть на IvI", url=url_watch[0])
        meg_but = types.InlineKeyboardButton(text="Посмотреть на Megogo", url=url_watch[1])

        if url_trailer is not None:
            trailer_but = types.InlineKeyboardButton(text="Посмотреть Трейлер", url=url_trailer)
            keyboard.add(trailer_but)

        keyboard.add(ivi_but)
        keyboard.add(meg_but)
        bot.send_message(message.chat.id, "Выберите где будете смотреть фильм.", reply_markup=keyboard)
    except TypeError:
        bot.send_message(message.chat.id, "Вы не выбрали фильм!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    global url_trailer, url_watch
    global review_bad, review_good
    global chat_id

    film = KinopoiskInfo()
    ans = film.fill_info(message.text.lower())
    if ans is None:
        bot.send_message(message.chat.id, "Бот не может достучаться до Кинопоиска, повторите попытку позже (примерно "
                                          "5 минут)")
        return
    if not ans:
        bot.send_message(message.chat.id, "Такого фильма не существует")
    else:
        if film.check_name():
            bot.send_message(message.chat.id, "Ваш фильм")
        else:
            bot.send_message(message.chat.id, "Такой фильм не был найден, может быть вы имели ввиду:")

        info = film.get_main_info()
        ans = create_message(info)

        url_trailer = film.url_trailer
        url_watch = Send_URL(info)
        review_bad = info.get("bad_review")
        review_good = info.get("good_review")

        keyboard = get_base_inline_keyboard()
        chat_id = message.chat.id
        bot.send_photo(message.chat.id, info.get("image"))
        bot.send_message(message.chat.id, ans, reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling()
