from enum import Enum, auto


class Sport(Enum):
    SKIING = auto()


class GoodPlace(Enum):
    BEACH = auto()


place_dict = [
    {
        "name": "Германия",
        "temperature": -5,
        "sport": [
            Sport.SKIING
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "Мальдивы",
        "temperature": 25,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
    {
        "name": "Исландия",
        "temperature": 10,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "Италия",
        "temperature": 15,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "Куба",
        "temperature": 20,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
    {
        "name": "Норвегия",
        "temperature": -10,
        "sport": [
            Sport.SKIING
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "Сочи",
        "temperature": 26,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": False
    },
    {
        "name": "Тайланд",
        "temperature": 27,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
    {
        "name": "Франция",
        "temperature": 5,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": True
    },
    {
        "name": "Хибины",
        "temperature": -15,
        "sport": [
        ],
        "good_place": [
        ],
        "visa_required": False
    },
    {
        "name": "Шри-Ланка",
        "temperature": 28,
        "sport": [
        ],
        "good_place": [
            GoodPlace.BEACH
        ],
        "visa_required": True
    },
]
