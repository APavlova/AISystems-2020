from PyQt5.QtCore import QObject, pyqtSignal
from transitions import Machine
from enum import Enum


# Состояния конечного автомата
class DialogState(Enum):
    user_ask_questions = "user_ask_questions",
    user_choosing_country = "user_choosing_country",
    user_thinking_about_visa = "user_thinking_about_visa",
    user_approving_travel = "user_approving_travel",
    user_approved_travel = "user_approved_travel"


# Конечный автомат для развития сценария диалога по триггерам
class DialogStateMachine(QObject):
    # Сигнал смены состояния
    send_new_state = pyqtSignal(str)

    # Возможные состояния диалога
    states = [
                # Пользователь задает вопросы
                DialogState.user_ask_questions,
                # Пользователь выбирает страну из списка
                DialogState.user_choosing_country,
                # Пользователь думает по поводу оформления визы
                DialogState.user_thinking_about_visa,
                # Пользователь думает над подтверждением поездки
                DialogState.user_approving_travel,
                # Пользователь подтвердил поездку. Диалог завершен
                DialogState.user_approved_travel
                ]

    # Возможные переходы диалога
    transitions = [
        # Система представила варианты; Пользователь выбирает страну из списка
        {
            "source": DialogState.user_ask_questions,
            "dest": DialogState.user_choosing_country,
            "trigger": "user_accept",
            "after":  "send_signal"
        },
        # Система представила варианты; Пользователь не выбрал страну из списка
        {
            "source": DialogState.user_choosing_country,
            "dest": DialogState.user_ask_questions,
            "trigger": "user_reject",
            "after":  "send_signal"
        },
        # Пользователь выбрал страну из списка; Спрашиваем про визу
        # (виза в стране требуется)
        {
            "source": DialogState.user_choosing_country,
            "dest": DialogState.user_thinking_about_visa,
            "trigger": "user_accept",
            "conditions": ['is_visa_required'],
            "after":  "send_signal"
        },
        # Пользователь выбрал страну из списка; Просим подтвердить согласие
        # на оформление (виза в стране не требуется)
        {
            "source": DialogState.user_choosing_country,
            "dest": DialogState.user_approving_travel,
            "trigger": "user_accept",
            "after":  "send_signal"
        },
        # Пользователь согласился оформлять визу;
        # Переходим к подтверждению оформления
        {
            "source": DialogState.user_thinking_about_visa,
            "dest": DialogState.user_approving_travel,
            "trigger": "user_accept",
            "after": "send_signal"
        },
        # Пользователь отказался оформлять визу;
        # Переходим обратно к выбору стран
        {
            "source": DialogState.user_thinking_about_visa,
            "dest": DialogState.user_choosing_country,
            "trigger": "user_reject",
            "after":  "send_signal"
        },
        # Пользователь подтвердил согласил на оформление
        {
            "source": DialogState.user_approving_travel,
            "dest": DialogState.user_approved_travel,
            "trigger": "user_accept",
            "after":  "send_signal"
        },
        # Пользователь отказался оформлять
        {
            "source": DialogState.user_approving_travel,
            "dest": DialogState.user_ask_questions,
            "trigger": "user_reject",
            "after":  "send_signal"
        }
    ]

    def __init__(self):
        super().__init__()
        self.machine = Machine(model=self, states=DialogStateMachine.states,
                               initial=DialogState.user_ask_questions)
        # Настроить все переходы между состояниями конечного автомата
        self.setup_transitions()

    def setup_transitions(self):
        # Задать возможные переходы
        self.machine.add_transitions(self.transitions)

    def get_transitions(self):
        return self.machine.get_transitions()

    def get_state(self):
        return self.state

    def is_visa_required(self):
        # TODO: Добавить проверку на наличие визы в стране
        return True

    def send_signal(self):
        self.send_new_state.emit(self.state.name)
