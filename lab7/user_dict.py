# Словари для синтаксического анализа #

# Словарь слов и их синонимов, обозначающие направление
user_wish_dict = {
    "где", "где-нибудь", "где-то",
    "есть",
    "куда", "куда-нибудь", "куда-либо",
    "найти", "найтись",
    "нравиться", "любить"
}

# Словарь стран
# TODO: удалить!
# user_attract_country_dict = [
#     {"name": "куба", "preposition": "на"},
#     {"name": "мальдивы", "preposition": "на"},
#     {"name": "шри-ланка", "preposition": "на"},
#     {"name": "франция", "preposition": "в"}
# ]

user_attract_country_dict = {
    "куба", "мальдивы", "шри-ланка", "франция"
}

# Словарь слов и их синонимов, обозначающие достопримечательности
user_attract_place_dict = {
    "курорт", "курортный",
    "пляж", "пляжный", "песок", "песчаный",
    "море", "озеро", "река", "речка",
    "горы", "горный"
}

# Словарь слов и их синонимов, обозначающие виды спорта / досуга
user_attract_sport_dict = {
    "горный", "лыжа"
}

# Словарь слов и их синонимов, обозначающие действие
user_attract_travel_way_dict = {
    "поехать", "сгонять", "махнуть",
    "отдохнуть",
    "покататься"
}

# Словарь слов и их синонимов, обозначающие погоду
weather_dict = {
    "погода"
}

# Словарь слов и их синонимов, обозначающие температуру воздуха
user_attract_weather_dict = {
    "тёплый", "тепло", "жаркий", "жарко",  # : [20, 40],
    "холодный", "холодно", "морозный", "морозно"  # : [-20, 10]
}

user_attract_time_dict = {
    "сейчас"
}
