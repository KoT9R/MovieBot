# Cinema Bot
Имя бота @Super_find_movie_bot

Бот обрабатывает запрос по названиею фильма, и выводит информацию о найденном фильме.

## Как работает

1. Поиск

Бот полностью основан на парсинге страницы кинопоиска. Он выходит на страницу поиска и находит фильм, который кинопоиск ему выдал самым верхнем в запросе. Но поиск кинопоиска работает по-разному и нужно обработать 4 случая:
    1. Это обычный случай, когда нашлись только фильмы. Тогда просто бот запоминает ссылку с верхнего фильма.
    2. Случай когда нашлись актеры, тогда бот находит самый верхний первый попавшийя фильм, запоминает его ссылку.
    3. Когда "Кинопоиск" не может найти фильм с подобным названием. 
    4. Когда "Кинопоиск" выдает сразу же запрошенный фильм.

2. Парсинг 

    Бот запоминает основную информацию для фильма:  
    1. Полное имя фильма.
    2. Год
    3. Страну
    4. Режисер
    5. Рейтинг "Кинопоиск" и "imdb"
    6. Длительность фильма
    7. Жанр фильма
    8. Один хороший и один плохой отзыв
    9. Ссылку на трейлер фильма

## Дополнительные возможности
 Командой /more - выведит, где можно посмотреть трейлер к фильму и сам фильм.
 С помощью высплывающих кнопок можно посмотреть хороший и плохой отзыв.
 
## Примечание
Так как все берется из сайта Кинопоиск, то некоторых данных может и не быть.