from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
import logging as log
from gui import Ui_dialog_form
import sys
from user_dialog import DialogSystem, initial_message
import debug


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        # Создаем GUI
        self.ui = Ui_dialog_form()
        self.ui.setupUi(self)

        # Устанавливаем связи между элементами GUI
        self.setup_ui()

        # Создаем диалогововую систему
        self.dialog_system = DialogSystem()

        # Связь диалоговой системы с GUI
        self.setup_dialog_system()
        self.setup_state_machine()

        # В GUI задаем начальное состояние конечного автомата диалога
        self.dialog_system.state_machine.send_new_state.emit(
            self.dialog_system.state_machine.get_state().name
        )

        # Отправить начальное сообщение диалоговой системы
        self.send_dialog_system_start_message()

    def setup_ui(self):
        self.ui.send_message_button.clicked.connect(
            self.send_message
        )
        self.ui.new_chat_button.clicked.connect(self.new_chat_button_clicked)
        self.ui.fixed_questions_box.currentTextChanged.connect(
            self.fixed_questions_box_text_changed
        )
        self.ui.message_edit.setFocus()
        self.ui.dialog_widget.model().rowsInserted.connect(
            self.dialog_widget_scroll_down
        )

    def setup_dialog_system(self):
        self.dialog_system.send_answer_signal.connect(
            self.dialog_system_answer_message_received
        )
        self.dialog_system.send_analysis_report.connect(
            self.dialog_system_analysis_report_received
        )

    def send_dialog_system_start_message(self):
        self.dialog_system_answer_message_received(initial_message)

    def setup_state_machine(self):
        self.dialog_system.state_machine.send_new_state.connect(
            self.state_machine_state_changed
        )

    def send_message(self):
        message = self.ui.message_edit.text()

        if not len(message):
            QMessageBox.warning(self.ui.dialog_widget, "Предупреждение",
                                "Введите сообщение!")
            return
        log.debug(f'Сообщение пользователя: {message}')

        # Отправить сообщение пользователя в чат
        new_message_item = QListWidgetItem(message)
        new_message_item.setTextAlignment(Qt.AlignRight)
        new_message_item.setForeground(Qt.red)
        self.ui.dialog_widget.addItem(new_message_item)

        # Обработать сообщение пользователя в диалоговой системе
        self.dialog_system.process_text(message)

        # Очистить поле ввода
        self.clear_message_edit()

    def clear_dialog_widget(self):
        self.ui.dialog_widget.clear()
        self.ui.ais_result_view.clear()
        self.send_dialog_system_start_message()
        # TODO: Перезапустить чат

    def clear_message_edit(self):
        self.ui.message_edit.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.send_message()
        else:
            QtWidgets.QMainWindow.keyPressEvent(self, event)

    @pyqtSlot()
    def send_message_button_clicked(self):
        self.send_message()

    @pyqtSlot()
    def new_chat_button_clicked(self):
        self.clear_dialog_widget()

    @pyqtSlot(str)
    def fixed_questions_box_text_changed(self, string):
        if not len(string):
            return

        log.debug(f"Заготовленный текст: {string}")
        self.ui.fixed_questions_box.setCurrentIndex(-1)
        self.ui.message_edit.setText(string)

    @pyqtSlot(str)
    def dialog_system_answer_message_received(self, message):
        log.debug(f"Текст от системы: {message}")

        # Отправить ответ системы в чат
        new_message_item = QListWidgetItem(message)
        new_message_item.setTextAlignment(Qt.AlignLeft)
        self.ui.dialog_widget.addItem(new_message_item)

    @pyqtSlot()
    def dialog_widget_scroll_down(self):
        self.ui.dialog_widget.scrollToBottom()

    @pyqtSlot(str)
    def state_machine_state_changed(self, state):
        self.ui.state_machine_edit.setText(state)

    @pyqtSlot(str)
    def dialog_system_analysis_report_received(self, text):
        self.ui.ais_result_view.setText(text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
