# Шаблоны ответов диалоговой системы
dialog_answers = [
    {
        "answer_types": ["sport", "place"],
        "answers": [
            {
                "template":
                    "{sport_name} доступны в {country_name}.",
                "inflect": {
                    "country_name": {"loct"},
                    "country_word": {"loct"},
                    "sport_name": {"nomn"}
                }
            },
            {
                "template":
                    "Присмотрите {country_name}. Здесь можно "
                    "найти {sport_name}.",
                "inflect": {
                    "country_name": {"accs"},
                    "country_word": {"nomn"},
                    "sport_name": {"nomn"}
                }
            },
            {
                "template":
                    "Для {sport_name} присмотрите {country_word}: "
                    "{country_name}.",
                "inflect": {
                    "country_name": {"nomn"},
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
                    "Мы рекомендуем Вам {country_name}.",
                "inflect": {
                    "country_name": {"accs"}
                }
            },
            {
                "template":
                    "Мы можем предложить Вам {country_name}.",
                "inflect": {
                    "country_name": {"accs"}
                }
            },
            {
                "template":
                    "Советуем Вам посетить {country_name}.",
                "inflect": {
                    "country_name": {"accs"}
                }
             }
        ]
    }
]

