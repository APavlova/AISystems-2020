import pymorphy2
from PyQt5.QtCore import pyqtSignal, QObject
from state_machine import DialogStateMachine, DialogState
from user_dict import *
from dialog_answers import *
import random
from string import Template, Formatter
from place_dict import place_dict, Sport
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

# Паттерны распознавания текста в зависимости от состояния диалога
dialog_sentence_patterns = [
    {
        # Пользователь задает вопросы
        "state": [DialogState.user_ask_questions],
        "patterns": [
            {
                # Ключевое слово в предложении - вид спорта
                # [A] [B] C [E]
                "required": [user_attract_sport_dict],
                "optional": [user_wish_dict, user_attract_travel_way_dict,
                             user_attract_country_dict],
                "type": "sport"
            },
            {
                # Ключевое слово в предложении - вид отдыха
                # [A] [B] D [E]
                "required": [user_attract_place_dict],
                "optional": [user_wish_dict, user_attract_travel_way_dict,
                             user_attract_country_dict],
                "type": "place"
            },
            {
                # Ключевое слово в предложении - погода в стране / странах
                # [A] [F] G
                "required": [user_attract_weather_dict],
                "optional": [user_wish_dict, user_attract_time_dict],
                "type": "weather"
            },
            {
                # Ключевое слово в предложении - подобрать страну / страны
                # [A] B [E]
                "required": [user_attract_travel_way_dict],
                "optional": [user_attract_country_dict, user_wish_dict],
                "type": "country"
            }
        ]
    },
    {
        # Пользователь выбирает страны из списка предложенных
        "state": [DialogState.user_choosing_country],
        "patterns": [
            {
                "required": [user_attract_country_dict],
                "type": "user_choose"
            }
        ]
    },
    {
        # Пользователь отвечает на оформление путевки или визы
        # TODO: Предусмотреть наличие частички "не" в ответе
        "state": [DialogState.user_approving_travel,
                  DialogState.user_thinking_about_visa],
        "patterns": [
            {
                "required": [user_confirmation_dict],
                "type": "user_confirm"
            },
            {
                "required": [user_rejection_dict],
                "type": "user_reject"
            }
        ]
    }
]


# Память ключевых слов, упоминаемых в диалоге
class DialogMemory:
    dialog_memory = {
        "country": None,
        "place": None,
        "sport": None,
        "time": None,
        "weather": None,
        "travel_way": None,
        "user_like_visa": None,
        "last_system_message": None
    }

    def __init__(self):
        pass

    def save(self, key, value):
        if key in self.dialog_memory:
            if value is not None:
                if len(value):
                    # FIXME: Учитывается только одно слово из списка
                    log.debug(f"Запомнить: {key} = {value[0]}")
                    self.dialog_memory[key] = value

    def restore(self, key):
        if key in self.dialog_memory:
            return self.dialog_memory[key]
        return None

    def reset(self):
        for key in self.dialog_memory:
            self.dialog_memory[key] = None
        log.debug(f"Память диалога очищена!")
        log.debug(self.dialog_memory)


# Класс диалоговой системы
class DialogSystem(QObject):
    dialog_memory = DialogMemory()
    state_machine = DialogStateMachine()
    send_answer_signal = pyqtSignal(str)
    send_analysis_report = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.morph = pymorphy2.MorphAnalyzer()
        self.morphs = None

    def process_text(self, text):
        answer_text, answer_type, prob, self.morphs = self._process_text(text)

        # Отправить сигнал с результатами анализа текста
        self.send_syntactic_analysis_report(self.morphs, answer_type, prob)

        # Отправить сигнал с текстом ответа системы
        self.send_answer_signal.emit(answer_text)

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
        # и определение смысла контекста
        answer_type, prob = self.syntactic_analysis(morphs)

        # Формирование ответа системы на основе смысла контекста
        # с учетом выделения уточняющих слов
        answer_text = self.generate_answer(answer_type, morphs)

        # Сменить состояние диалога
        if answer_type == "user_reject":
            self.state_machine.user_reject()
        else:
            # TODO: Подтвердить только если была выбрана страна!
            self.state_machine.user_accept()

        # XXX: Убрать как только заработает конечный автомат
        self.state_machine.user_reject()

        return answer_text, answer_type, prob, morphs

    def tokenization(self, text):
        # Упрощение: объяединяем все слова в одно предложение
        for symbol in [".", ",", "?", "!"]:
            text = text.replace(symbol, " ")

        words = text.split()
        log.debug(f"Слова: {words}")
        return words

    def morph_analysis(self, words):
        # TODO: Учитывать несколько результатов (проблема омонимии)
        return list(
            map(lambda word: self.morph.parse(word)[0].normal_form, words))

    def syntactic_analysis(self, words):
        pattern_max_prob = 0.0
        pattern_ans_type = None

        # Текущее состояние диалога
        dialog_state = self.state_machine.get_state()

        # Набор паттернов на основе состояния диалога
        patterns = None
        for pattern in dialog_sentence_patterns:
            if dialog_state in pattern["state"]:
                patterns = pattern["patterns"]

        # Перебор всех заложенных паттернов сообщений для текущего состояния
        for pattern in patterns:
            answer_type, prob = self.apply_pattern(words, pattern)
            if pattern_max_prob < prob:
                pattern_max_prob = prob
                pattern_ans_type = answer_type

        print(f"Максимальная вероятность: {pattern_max_prob};"
              f" Тип ответа: {pattern_ans_type}")

        return pattern_ans_type, pattern_max_prob

    def apply_pattern(self, words, pattern):
        # Вес частей паттерна для подсчета вероятности совпадения
        required_dict_weight = 10.0
        optional_dict_weight = 1.0

        # Суммы весов
        weight_sum = 0
        weight_total = 0

        # Проверка обязательных совпадений со словарем
        for required in pattern["required"]:
            if len(self.intersect_with_dict(words, required)) > 0:
                weight_sum += required_dict_weight
            weight_total += required_dict_weight

        # Проверка необязательных совпадений со словарем
        if "optional" in pattern:
            for optional in pattern["optional"]:
                if len(self.intersect_with_dict(words, optional)) > 0:
                    weight_sum += optional_dict_weight
                weight_total += optional_dict_weight

        pattern_apply_prob = weight_sum / weight_total
        answer_type = pattern["type"]

        print(f"Вероятность применения паттерна '{answer_type}':"
              f" {weight_sum} / {weight_total} = {pattern_apply_prob}\n")

        return answer_type, pattern_apply_prob

    def generate_answer(self, answer_type, words):
        answer_text = None

        # Формирование ответа на вопрос пользователя
        if self.state_machine.get_state() == DialogState.user_ask_questions:
            answer_text = self.generate_user_ask_answer(answer_type, words)

        # Страна выбрана. Формирование вопроса про оформление или визу
        if self.state_machine.get_state() == DialogState.user_choosing_country:
            answer_text = self.generate_user_choose_country_answer(answer_type,
                                                                   words)

        # Ответ на оформление визы получен. Вопрос про подтверждения оформления
        if self.state_machine.get_state() == DialogState.user_thinking_about_visa:
            answer_text = self.generate_user_thinking_about_visa(answer_type,
                                                                 words)

        # Ответ на подверждение оформления получен. Выдать результаты.
        if self.state_machine.get_state() == DialogState.user_approving_travel:
            answer_text = self.generate_user_approving_travel(answer_type,
                                                              words)

        # Завершение диалога какой-то фразой
        if self.state_machine.get_state() == DialogState.user_approved_travel:
            answer_text = self.generate_user_approved_travel(answer_type, words)

        # Вопрос или ответ не распознаны
        if answer_type is None or answer_text is None:
            answer_text = "Я не понимаю."

        return answer_text

    def generate_user_ask_answer(self, answer_type, words):
        answer_text = None

        # Формирование ответа на вопрос про досуг
        if answer_type == "sport" or answer_type == "place":
            answer_text = self.apply_answer_template(answer_type, words)
        if answer_type == "country" or answer_type == "weather":
            answer_text = self.apply_answer_template(answer_type, words)

        # Выделить полезные слова из набора слов
        # и запомнить в памяти диалоговой системы
        self.filter_useful_words_and_save_to_dialog_memory(words)

        return answer_text

    def apply_answer_template(self, answer_type, words):
        if set(words).intersection(user_want_yes_no_answer_dict) \
                and not len(set(words).intersection(user_wish_dict)):
            # Ответ в формате "Да", "Нет"
            template_answer = random.choice(yes_no_dialog_answers)
        else:
            # Общий ответ
            template_answer = self.find_common_dialog_template(answer_type)

        # Заполнить идентификаторы шаблона
        answer_text = self.fill_answer_template(template_answer, answer_type,
                                                words)
        return answer_text

    def find_common_dialog_template(self, answer_type):
        for dialog_answer in common_dialog_answers:
            for a_type in dialog_answer["answer_types"]:
                # Найдены шаблоны ответов по типу ответа
                if a_type == answer_type:
                    # Выбрать шаблон ответа случайным образом
                    return random.choice(dialog_answer["answers"])
        return None

    def fill_answer_template(self, template_answer, answer_type, words):
        # Создать словарь замен для шаблонов
        # TODO: Улучшить реализацию
        replace_dict = {}

        user_want_common_answer = \
            not len(set(words).intersection(user_want_yes_no_answer_dict)) \
            or len(set(words).intersection(user_wish_dict))

        # Если пользователь ждет общего ответа (рекомендация)
        if user_want_common_answer:
            # Найти подходящие страны и поместить в список
            location_names_list = self.find_suitable_countries(answer_type,
                                                               words)
        # Если пользователь ждет ответа "да" или "нет"
        else:
            # Выделить из слов страну, интересующую пользователя
            user_attract_country = \
                set(words).intersection(user_attract_country_dict)
            user_attract_country = list(user_attract_country)
            # Поместить в список
            location_names_list = user_attract_country

            # Дать ответ на вопрос пользователя
            is_correct = self.check_country_parameter(user_attract_country[0],
                                                      answer_type, words)

            replace_dict["yes_no_word"] = "Да" if is_correct else "Нет"
            replace_dict["has_hasnt_word"] = "есть" if is_correct else "нет"

        # Досуг или место отдыха
        name = self.get_dict_phrase_from_filter_words(answer_type, words)

        if name is not None:
            # FIXME: Досуг или место отдыха всегда в множественном числе.
            #  Исправить!
            phrase = name
            name = []
            for word in phrase:
                name.append(self.morph.parse(word)[0].inflect({'plur'}))

            str = ""
            if "sport_name" in template_answer["inflect"]:
                inflect = template_answer["inflect"]["sport_name"]
                for i in range(0, len(name)):
                    name[i] = name[i].inflect(inflect)

            # Меняем падеж для вопросов "да" и "нет"
            if not user_want_common_answer:
                inflect = {'nomn'} if is_correct else {'gent'}
                for i in range(0, len(name)):
                    name[i] = name[i].inflect(inflect)

            # Набор поставленных слов в падеж в строку
            str += name[0].word
            for i in range(1, len(name)):
                str += " " + name[i].word

            # Это не ошибка!
            replace_dict["sport_name"] = str

        # Страна
        case = "nomn"
        if "location_name" in template_answer["inflect"]:
            case = template_answer["inflect"]["location_name"]

        # Список из одной и более стран в читабельный вид
        location_names_str = self.countries_list_to_str(location_names_list,
                                                        answer_type, case)

        if "country_word" in template_answer["inflect"]:
            country_word = self.morph.parse("страна")[0].inflect({
                'plur' if len(location_names_list) else 'sing'
            })
            inflect = template_answer["inflect"]["country_word"]
            country_word = country_word.inflect(inflect)

            replace_dict["country_word"] = country_word.word

        # Список стран в читабельном виде
        replace_dict["location_name"] = location_names_str
        replace_dict["location_prefix"] = \
            self.generate_location_prefix(location_names_list[0])

        # Результирующая строка
        answer_text = Formatter().format(template_answer["template"],
                                         **replace_dict)
        answer_text = answer_text[0].upper() + answer_text[1:]

        return answer_text

    def get_dict_phrase_from_filter_words(self, answer_type, words):
        if answer_type == "sport":
            filter_words = list(
                set(words).intersection(user_attract_sport_dict))
            valid_dict = "sport"
        elif answer_type == "place":
            filter_words = list(
                set(words).intersection(user_attract_place_dict))
            valid_dict = "good_place"
        else:
            return None

        name = self.find_in_place_dict(answer_type, filter_words, valid_dict)

        if len(name):
            return name[0][0].value.split()
        return None

    def check_country_parameter(self, country_name, answer_type, words):
        results = None
        filter_words = {}
        if answer_type == "sport":
            results = self.find_parameter_in_place_dict(country_name, "sport")
            filter_words = set(words).intersection(user_attract_sport_dict)
        elif answer_type == "place":
            results = self.find_parameter_in_place_dict(country_name,
                                                        "good_place")
            filter_words = set(words).intersection(user_attract_place_dict)
        # TODO: Добавить про погоду

        for result in results:
            words = set(result.value.split())
            if words.intersection(filter_words):
                return True
        return False

    def find_suitable_countries(self, answer_type, words):
        dictionary = None

        # Фильтр стран по досугу
        if answer_type == "sport":
            dictionary = user_attract_sport_dict
        # Список стран по месту отдыха
        elif answer_type == "place":
            dictionary = user_attract_place_dict
        # Список стран рандомно
        elif answer_type == "country":
            dictionary = user_attract_country_dict
        # Список стран по погоде
        elif answer_type == "weather":
            dictionary = user_attract_weather_dict

        filter_words = list(set(words).intersection(dictionary))

        # Получен список подходящих стран
        countries_list = self.find_in_place_dict(answer_type, filter_words,
                                                 "name")

        return countries_list

    def countries_list_to_str(self, countries_list, answer_type, case):
        # Список стран пуст
        if not len(countries_list):
            return "", None

        # Установить список стран в правильный падеж
        for i in range(0, len(countries_list)):
            countries_list[i] = self.morph.parse(countries_list[i])[0].inflect(
                set(case)
            ).word
            countries_list[i] = countries_list[i][0].upper() + countries_list[
                                                                   i][1:]

        # Перевести в читабельный вид
        countries_string = self.append_param(countries_list[0], answer_type)

        for i in range(1, len(countries_list) - 1):
            countries_string += ", " + self.append_param(countries_list[i],
                                                         answer_type)

        if len(countries_list) > 1:
            countries_string += " и " + self.append_param(countries_list[-1],
                                                          answer_type)

        return countries_string

    # Сгенерировать приставки "в, во, на" на основе названия
    def generate_location_prefix(self, location_name):
        # если первые две буквы слова - согласные, то приставка "во"
        consonants = ['бвгджзйклмнпрстфхцчшщ']
        if location_name[0] in consonants and location_name[1] in consonants:
            return "во"

        # если Куба, то приставка "на"
        if self.morph.parse(location_name)[0].normal_form == "куба":
            return "на"

        return "в"

    # Добавить параметр к объекту в скобках (например температура)
    def append_param(self, location_name, answer_type):
        location_name_normal = self.morph.parse(location_name)[0].normal_form
        phrase = ""

        # Добавить температуру
        if answer_type == "weather":
            temperature = self.find_parameter_in_place_dict(
                location_name_normal,
                "temperature")
            temperature_word = "градус"

            # Согласование с числетельным
            temperature_word = self.morph.parse(temperature_word)[
                0].make_agree_with_number(temperature).word

            temperature_phrase = f" (температура {temperature}" \
                                 f" {temperature_word})"
            phrase = temperature_phrase

        location_name = location_name[0].upper() + location_name[1:]
        return location_name + phrase

    def find_in_place_dict(self, key, values, field, limit=5):
        if key is None:
            return None

        result = []
        limit_country_num = limit
        for country in place_dict:
            is_valid_country = False

            if key == "sport":
                for sport in country["sport"]:
                    country_sport_set = set(sport.value.split())
                    country_sport_set_n = set({})
                    for word in country_sport_set:
                        country_sport_set_n.add(
                            self.morph.parse(word)[0].normal_form)

                    if len(country_sport_set_n.intersection(values)):
                        is_valid_country = True

            if key == "place":
                for place in country["good_place"]:
                    if len(set(place.value.split()).intersection(values)):
                        is_valid_country = True

            if key == "weather":
                # FIXME: Исправить дублирование словарей
                warm_set = {"тёплый", "тепло", "жаркий", "жарко"}
                cold_set = {"холодный", "холодно", "морозный", "морозно"}

                if set(values).intersection(warm_set) \
                        and country["temperature"] in range(20, 40):
                    is_valid_country = True

                if set(values).intersection(cold_set) \
                        and country["temperature"] in range(-30, 5):
                    is_valid_country = True

            if key == "country":
                is_valid_country = True

                if len(result) > limit_country_num:
                    del result[random.randint(0, len(result) - 1)]

            if is_valid_country:
                result.append(country[field])

        return result

    def find_parameter_in_place_dict(self, location_name, param_name):
        for country in place_dict:
            if country["name"] == location_name:
                return country[param_name]

    def generate_user_choose_country_answer(self, answer_type, words):
        answer_text = None

        if answer_type == "user_choose":
            answer_text = "Страна выбрана.Вопрос про согласие оформления " \
                          "визы."
        elif answer_type == "user_reject":
            answer_text = "Пользователь не выбрал страну."

        return answer_text

    def generate_user_thinking_about_visa(self, answer_type, words):
        answer_text = None

        if answer_type == "user_confirm":
            answer_text = "Пользователь согласен на визу.Вопрос на " \
                          "подтверждение оформления. "
        elif answer_type == "user_reject":
            answer_text = "Пользователь не согласен на визу."

        return answer_text

    def generate_user_approving_travel(self, answer_type, words):
        answer_text = None

        if answer_type == "user_confirm":
            answer_text = "Пользователь согласился на оформление. Ура!"
        elif answer_type == "user_reject":
            answer_text = "Пользователь не стал соглашаться на оформление."

        return answer_text

    def generate_user_approved_travel(self, answer_type, words):
        answer_text = "Хорошего дня!"

        return answer_text

    def filter_useful_words_and_save_to_dialog_memory(self, words):
        # Поиск пересечений со словарем действия
        travel_way_intersect = \
            self.intersect_with_dict(words, user_attract_travel_way_dict)
        # Запомнить
        self.dialog_memory.save("travel_way", travel_way_intersect)

        # Поиск пересечений со словарем досуга
        sport_intersect = self.intersect_with_dict(words,
                                                   user_attract_sport_dict)
        # Запомнить
        self.dialog_memory.save("sport", sport_intersect)

        # Поиск пересечений со словарем мест отдыха
        place_intersect = self.intersect_with_dict(words,
                                                   user_attract_place_dict)
        # Запомнить
        self.dialog_memory.save("place", place_intersect)

        # Поиск пересечений со словарем стран
        country_intersect = self.intersect_with_dict(words,
                                                     user_attract_country_dict)
        # Запомнить
        self.dialog_memory.save("country", country_intersect)

        # Поиск пересечений со словарем времени
        time_intersect = self.intersect_with_dict(words,
                                                  user_attract_time_dict)
        # Запомнить
        self.dialog_memory.save("time", time_intersect)

        # Поиск пересечений со словарем погодных условий
        weather_intersect = self.intersect_with_dict(words, weather_dict)
        # Запомнить
        self.dialog_memory.save("weather", weather_intersect)

    def send_syntactic_analysis_report(self, words, answer_type, prob):
        if not len(words):
            return

        # Поиск пересечений со словарем вопросительных слов
        wish_intersect = self.intersect_with_dict(words, user_wish_dict)

        # Поиск пересечений со словарем действия
        travel_way_intersect = \
            self.intersect_with_dict(words, user_attract_travel_way_dict)

        # Поиск пересечений со словарем досуга
        sport_intersect = self.intersect_with_dict(words,
                                                   user_attract_sport_dict)

        # Поиск пересечений со словарем мест отдыха
        place_intersect = self.intersect_with_dict(words,
                                                   user_attract_place_dict)

        # Поиск пересечений со словарем стран
        country_intersect = self.intersect_with_dict(words,
                                                     user_attract_country_dict)

        # Поиск пересечений со словарем времени
        time_intersect = self.intersect_with_dict(words, user_attract_time_dict)

        # Поиск пересечений со словарем погоды
        weather_intersect = self.intersect_with_dict(words, weather_dict)

        # Поиск пересечений со словарем погодных условий
        weather_wish_intersect = \
            self.intersect_with_dict(words, user_attract_weather_dict)

        # Поиск пересечений со словарем подтверждения от пользователя
        confirmation_intersect = self.intersect_with_dict(words,
                                                          user_confirmation_dict
                                                          )

        # Поиск пересечений со словарем отказа пользователя
        rejection_intersect = self.intersect_with_dict(words,
                                                       user_rejection_dict)

        # Отчет синтаксического анализа
        syntactic_report = f'Слова из словаря:\n'
        syntactic_report += f'(А) {wish_intersect}\n'
        syntactic_report += f'(B) {travel_way_intersect}\n'
        syntactic_report += f'(C) {sport_intersect}\n'
        syntactic_report += f'(D) {place_intersect}\n'
        syntactic_report += f'(E) {country_intersect}\n'
        syntactic_report += f'(F) {time_intersect}\n'
        syntactic_report += f'(G) {weather_intersect}\n'
        syntactic_report += f'(H) {weather_wish_intersect}\n'
        syntactic_report += f'(I) {confirmation_intersect}\n'
        syntactic_report += f'(J) {rejection_intersect}\n'

        syntactic_report += f'\nКонтекст ответа:\n'
        syntactic_report += f'{answer_type}\n'

        syntactic_report += f'\nВероятность:\n'
        prob_normalized = format(prob, '.2f')
        syntactic_report += f'{prob_normalized}'

        self.send_analysis_report.emit(syntactic_report)

    def intersect_with_dict(self, words, dictionary):
        words_set = set(words)
        return list(words_set.intersection(dictionary))

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
