# -*- coding: utf-8 -*-

#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_form(object):
    def setupUi(self, dialog_form):
        dialog_form.setObjectName("dialog_form")
        dialog_form.resize(449, 421)
        font = QtGui.QFont()
        font.setPointSize(12)
        dialog_form.setFont(font)
        self.dialog_widget = QtWidgets.QListWidget(dialog_form)
        self.dialog_widget.setGeometry(QtCore.QRect(9, 10, 431, 301))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dialog_widget.sizePolicy().hasHeightForWidth())
        self.dialog_widget.setSizePolicy(sizePolicy)
        self.dialog_widget.setFrameShape(QtWidgets.QFrame.Panel)
        self.dialog_widget.setLineWidth(1)
        self.dialog_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dialog_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.dialog_widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.dialog_widget.setMovement(QtWidgets.QListView.Static)
        self.dialog_widget.setFlow(QtWidgets.QListView.TopToBottom)
        self.dialog_widget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.dialog_widget.setViewMode(QtWidgets.QListView.ListMode)
        self.dialog_widget.setBatchSize(100)
        self.dialog_widget.setWordWrap(True)
        self.dialog_widget.setSelectionRectVisible(False)
        self.dialog_widget.setObjectName("dialog_widget")
        self.message_edit = QtWidgets.QLineEdit(dialog_form)
        self.message_edit.setGeometry(QtCore.QRect(9, 340, 331, 21))
        self.message_edit.setObjectName("message_edit")
        self.send_message_button = QtWidgets.QPushButton(dialog_form)
        self.send_message_button.setGeometry(QtCore.QRect(345, 335, 101, 32))
        self.send_message_button.setObjectName("send_message_button")
        self.text_label = QtWidgets.QLabel(dialog_form)
        self.text_label.setGeometry(QtCore.QRect(9, 320, 141, 16))
        self.text_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.text_label.setObjectName("text_label")
        self.fixed_questions_box = QtWidgets.QComboBox(dialog_form)
        self.fixed_questions_box.setGeometry(QtCore.QRect(9, 384, 331, 32))
        self.fixed_questions_box.setObjectName("fixed_questions_box")
        self.fixed_questions_box.addItem("")
        self.fixed_questions_box.addItem("")
        self.fixed_questions_box.addItem("")
        self.fixed_questions_box.addItem("")
        self.fixed_questions_box.addItem("")
        self.fixed_questions_box.addItem("")
        self.fixed_questions_label = QtWidgets.QLabel(dialog_form)
        self.fixed_questions_label.setGeometry(QtCore.QRect(10, 370, 151, 16))
        self.fixed_questions_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.fixed_questions_label.setObjectName("fixed_questions_label")
        self.new_chat_button = QtWidgets.QPushButton(dialog_form)
        self.new_chat_button.setGeometry(QtCore.QRect(345, 385, 101, 32))
        self.new_chat_button.setObjectName("new_chat_button")

        self.retranslateUi(dialog_form)
        self.dialog_widget.setCurrentRow(-1)
        self.fixed_questions_box.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(dialog_form)

    def retranslateUi(self, dialog_form):
        _translate = QtCore.QCoreApplication.translate
        dialog_form.setWindowTitle(_translate("dialog_form", "Диалоговая система"))
        self.send_message_button.setText(_translate("dialog_form", "Отправить"))
        self.text_label.setText(_translate("dialog_form", "Текст:"))
        self.fixed_questions_box.setItemText(0, _translate("dialog_form", "Куда я могу поехать?"))
        self.fixed_questions_box.setItemText(1, _translate("dialog_form", "Где сейчас теплее всего?"))
        self.fixed_questions_box.setItemText(2, _translate("dialog_form", "Где я могу покататься на горных лыжах?"))
        self.fixed_questions_box.setItemText(3, _translate("dialog_form", "Мне нравилось на Мальдивах. Найди что-то похожее."))
        self.fixed_questions_box.setItemText(4, _translate("dialog_form", "На Кубе есть пляжные курорты?"))
        self.fixed_questions_box.setItemText(5, _translate("dialog_form", "Я могу покататься на горных лыжах на Шри-Ланке?"))
        self.fixed_questions_label.setText(_translate("dialog_form", "Заготовленный вопрос:"))
        self.new_chat_button.setText(_translate("dialog_form", "Новый чат"))