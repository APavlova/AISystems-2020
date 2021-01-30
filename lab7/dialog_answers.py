# Начальное сообщение от диалоговой системы
initial_message = "Я помогу подобрать страны для путешествия. Задавай" \
                          " вопрос. "

# Шаблоны ответов диалоговой системы
common_dialog_answers = [
    {
        "answer_types": ["sport", "place"],
        "answers": [
            {
                "template":
                    "{sport_name} доступны {location_prefix} {location_name}.",
                "inflect": {
                    "location_name": {"loct"},
                    "country_word": {"loct"},
                    "sport_name": {"nomn"}
                }
            },
            {
                "template":
                    "Присмотрите {location_name}. Здесь можно "
                    "найти {sport_name}.",
                "inflect": {
                    "location_name": {"accs"},
                    "country_word": {"nomn"},
                    "sport_name": {"nomn"}
                }
            },
            {
                "template":
                    "Для {sport_name} присмотрите {country_word}: "
                    "{location_name}.",
                "inflect": {
                    "location_name": {"nomn"},
                    "country_word": {"nomn"},
                    "sport_name": {"accs"}
                }
             }
        ]
    },
    {
        "answer_types": ["country", "weather"],
        "answers": [
            {
                "template":
                    "Мы рекомендуем Вам посетить {location_name}.",
                "inflect": {
                    "location_name": {"accs"}
                }
            },
            {
                "template":
                    "Мы можем предложить Вам {location_name}.",
                "inflect": {
                    "location_name": {"accs"}
                }
            },
            {
                "template":
                    "Советуем Вам посетить {location_name}.",
                "inflect": {
                    "location_name": {"accs"}
                }
             }
        ]
    }
]

yes_no_dialog_answers = [
    {
        "template": "{yes_no_word}, {location_prefix} {location_name} "
                    "{has_hasnt_word} {sport_name}.",
        "inflect": {
            "yes_no_word": {"nomn"},
            "location_prefix": {"nomn"},
            "location_name": {"loct"}
        }
    }
]
