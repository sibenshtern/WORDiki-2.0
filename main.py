import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from wordiki_ui import Ui_MainWindow
from card import Card


# card from new deck
def get_new_card():
    return Card("ccc", "ddd")


# card from old deck
def get_old_card():
    return Card("aaa", "bbb")


# add card to old deck with new type
def util_card(card, type):
    pass


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.card = Card("word", "translation")
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.start_button.clicked.connect(self.open_main_page)
        self.settings_button.clicked.connect(self.open_settings)
        self.repeat_button.clicked.connect(self.open_old_word_page)
        self.learn_button.clicked.connect(self.open_new_word_page)
        self.finish_button.clicked.connect(self.open_main_page)
        self.next_button.clicked.connect(self.next_card)
        self.study_word.mousePressEvent = self.change_label
        self.bad_button.clicked.connect(self.bad_card)
        self.ok_button.clicked.connect(self.ok_card)
        self.good_button.clicked.connect(self.good_card)
        self.back_button.clicked.connect(self.open_main_page)
        self.show()

    def open_settings(self):
        self.stackedWidget.setCurrentIndex(1)

    def open_main_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def open_old_word_page(self):
        self.stackedWidget.setCurrentIndex(3)

    def open_new_word_page(self):
        self.stackedWidget.setCurrentIndex(4)

    def next_card(self):
        self.card = get_new_card()
        self.word.setText(self.card.word)
        self.translation.setText(self.card.translate)

    def old_card(self):
        self.card = get_old_card()
        self.study_word.setText(self.card.word)
        self.translation.setText(self.card.translate)

    def change_label(self, event):
        if self.study_word.text() != self.card.translate:
            self.study_word.setText(self.card.translate)
        else:
            self.study_word.setText(self.card.word)

    def bad_card(self):
        util_card(self.card, 0)
        self.old_card()

    def ok_card(self):
        util_card(self.card, 1)
        self.old_card()

    def good_card(self):
        util_card(self.card, 2)
        self.old_card()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
