import pymorphy2
from PyQt5.QtCore import pyqtSignal, QObject
from user_dict import *
import logging as log
import debug

# Классы ключевых словарей
# A - вопросительные слова
# B - слова направления
# C - слова видов досуга
# D - слова видов мест отдыха
# E - слова названий стран
# F - слова, связанные со временем
# G - погода
# H - слова степеней погодных условий

dialog_sentence_patterns = [
    {
        # Ключевое слово в предложении - вид спорта
        # [A] [B] C [E]
        "required": [user_attract_sport_dict],
        "optional": [user_wish_dict, user_attract_travel_way_dict,
                     user_attract_country_dict]
    },
    {
        # Ключевое слово в предложении - вид отдыха
        # [A] [B] D [E]
        "required": [user_attract_place_dict],
        "optional": [user_wish_dict, user_attract_travel_way_dict,
                     user_attract_country_dict]
    },
    {
        # Ключевое слово в предложении - вид отдыха
        # [A] [B] D [E]
        "required": [user_attract_place_dict],
        "optional": [user_wish_dict, user_attract_travel_way_dict,
                     user_attract_country_dict]
    },
    {
        # Ключевое слово в предложении - погода в стране / странах
        # [A] [F] G
        "required": [user_attract_weather_dict],
        "optional": [user_wish_dict, user_attract_time_dict]
    },
    {
        # Ключевое слово в предложении - подобрать страну / страны
        # A [E]
        "required": [user_wish_dict],
        "optional": [user_attract_country_dict]
    }
]


class DialogSystem(QObject):
    send_answer_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        self.send_answer_signal.emit("Текст ответа.")


class UserDialog:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.morphs = None

    def process_text(self, text):
        self.morphs = self._process_text(text)
        self.print_info()

    # Обработка исходного текста
    def _process_text(self, text):
        self.text = text

        # Токенизация исходного текста
        # Результат: набор слов
        words = self.tokenization(text)

        # Морфологический анализ слов
        # Результат: набор нормализованных слов
        morphs = self.morph_analysis(words)

        # Синтаксический анализ нормализованных слов
        # TODO: Добавить синтаксический анализ

        # TODO: Исправить
        return morphs

    def tokenization(self, text):
        # Упрощение: объяединяем все слова в одно предложение
        for symbol in [".", ",", "?", "!"]:
            text = text.replace(symbol, " ")

        words = text.split()
        log.debug(f"Слова: {words}")
        return words

    def morph_analysis(self, words):
        # TODO: Учитывать несколько результатов (проблема омонимии)
        return list(map(lambda word: self.morph.parse(word)[0].normal_form, words))

    def syntactic_analysis(self, words):
        return None

    def print_info(self):
        if self.morphs is None:
            return

        print(f'Текст пользователя: {self.text}')
        print(f'Ключевые слова:')
        print(f'\t(А) вопрос. слова: {self.wish()}')
        print(f'\t(B) движение: {self.attract_travel_way()}')
        print(f'\t(C) досуг: {self.attract_sport()}')
        print(f'\t(D) места отдыха: {self.attract_place()}')
        print(f'\t(E) страна: {self.attract_country()}')
        print(f'\t(F) страна: {self.attract_time()}')
        print(f'\t(G) врем. промежуток: {self.weather()}')
        print(f'\t(H) погодные усл.: {self.attract_weather()}')

    def wish(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_wish_dict))

    def attract_country(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_attract_country_dict))

    def attract_sport(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_attract_sport_dict))

    def attract_travel_way(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_attract_travel_way_dict))

    def attract_place(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_attract_place_dict))

    def attract_time(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_attract_time_dict))

    def weather(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(weather_dict))

    def attract_weather(self):
        morphs = set(self.morphs)
        return list(morphs.intersection(user_attract_weather_dict))


class UserDialogFields:
    def __init__(self):
        self.time = None
        self.temperature = None
        self.location = None
        self.sport = None
        self.good_place = None
        self.move_type = None

    # def set_from(self, words):
