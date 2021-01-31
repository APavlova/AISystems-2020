from enum import Enum, auto


class Sport(Enum):
    SKIING = "горные лыжи"


class GoodPlace(Enum):
    BEACH = "пляжный курорт"
    SEA = "море"
    OCEAN = "океан"


place_dict = [
    {
        "name": "германия",
        "temperature": -5,
        "sport": [
            Sport.SKIING
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "мальдивы",
        "temperature": 25,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
    {
        "name": "исландия",
        "temperature": 10,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "италия",
        "temperature": 15,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "куба",
        "temperature": 20,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
    {
        "name": "норвегия",
        "temperature": -10,
        "sport": [
            Sport.SKIING
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "сочи",
        "temperature": 26,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH,
            GoodPlace.SEA
        ],
        "visa_required": False
    },
    {
        "name": "таиланд",
        "temperature": 27,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
    {
        "name": "франция",
        "temperature": 5,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "хибины",
        "temperature": -15,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": False
    },
    {
        "name": "шри-ланка",
        "temperature": 28,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
]
