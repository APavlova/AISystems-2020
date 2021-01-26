from PyQt5.QtCore import QObject, pyqtSignal
from transitions import Machine


# Конечный автомат для развития сценария диалога по триггерам
class DialogStateMachine(QObject):
    # Сигнал смены состояния
    send_new_state = pyqtSignal(str)

    # Возможные состояния диалога
    states = [
                # Пользователь задает вопросы
                "user_ask_questions",
                # Пользователь выбирает страну из списка
                "user_choosing_country",
                # Пользователь думает по поводу оформления визы
                "user_thinking_about_visa",
                # Пользователь думает над подтверждением поездки
                "user_approving_travel",
                # Пользователь подтвердил поездку. Диалог завершен
                "user_approved_travel"
                ]

    # Возможные переходы диалога
    transitions = [
        # Система представила варианты; Пользователь выбирает страну из списка
        {
            "source": "user_ask_questions",
            "dest": "user_choosing_country",
            "trigger": "user_accept",
            "after":  "send_signal"
        },
        # Система представила варианты; Пользователь не выбрал страну из списка
        {
            "source": "user_choosing_country",
            "dest": "user_ask_questions",
            "trigger": "user_reject",
            "after":  "send_signal"
        },
        # Пользователь выбрал страну из списка; Спрашиваем про визу
        # (виза в стране требуется)
        {
            "source": "user_choosing_country",
            "dest": "user_thinking_about_visa",
            "trigger": "user_accept",
            "conditions": ['is_visa_required'],
            "after":  "send_signal"
        },
        # Пользователь выбрал страну из списка; Просим подтвердить согласие
        # на оформление (виза в стране не требуется)
        {
            "source": "user_choosing_country",
            "dest": "user_approving_travel",
            "trigger": "user_accept",
            "after":  "send_signal"
        },
        # Пользователь отказался оформлять визу;
        # Переходим обратно к выбору стран
        {
            "source": "user_thinking_about_visa",
            "dest": "user_choosing_country",
            "trigger": "user_reject",
            "after":  "send_signal"
        },
        # Пользователь подтвердил согласил на оформление
        {
            "source": "user_approving_travel",
            "dest": "user_approved_travel",
            "trigger": "user_accept",
            "after":  "send_signal"
        },
        # Пользователь отказался оформлять
        {
            "source": "user_approving_travel",
            "dest": "user_ask_questions",
            "trigger": "user_reject",
            "after":  "send_signal"
        },
    ]

    def __init__(self):
        super().__init__()
        self.machine = Machine(model=self, states=DialogStateMachine.states,
                               initial=DialogStateMachine.states[0])
        # Настроить все переходы между состояниями конечного автомата
        self.setup_transitions()

    def setup_transitions(self):
        self.machine.add_transitions(self.transitions)

    def get_transitions(self):
        return self.machine.get_transitions()

    def get_state(self):
        return self.state

    def is_visa_required(self):
        # TODO: Добавить проверка на наличие визы в стране
        return True

    def send_signal(self):
        self.send_new_state.emit(self.state)
