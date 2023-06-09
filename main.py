import sys
from datetime import datetime
import csv

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

import config
from wordiki_ui import Ui_MainWindow

from sqlalchemy import exc

from database import init, create_session
from database.models import Card
from card import SessionManager
from config import runtime


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.card = None
        self.session_manager = SessionManager()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.start_button.clicked.connect(self.open_main_page)
        self.settings_button.clicked.connect(self.open_settings)
        self.repeat_button.clicked.connect(self.open_old_word_page)
        self.learn_button.clicked.connect(self.open_new_word_page)
        self.finish_button.clicked.connect(self.open_main_page)
        self.next_button.clicked.connect(self.learn_next_card)
        self.study_word.mousePressEvent = self.change_label
        self.bad_button.clicked.connect(self.bad_card)
        self.ok_button.clicked.connect(self.ok_card)
        self.good_button.clicked.connect(self.good_card)
        self.back_button.clicked.connect(self.open_main_page)
        self.load_button.clicked.connect(self.load_new_words)
        self.change_labels_button.clicked.connect(self.open_labels_page)
        self.settings_button.clicked.connect(self.open_settings)
        self.bad_line_button.clicked.connect(self.bad_label)
        self.good_line_button.clicked.connect(self.good_label)
        self.ok_line_button.clicked.connect(self.ok_label)
        self.return_button.clicked.connect(self.open_settings)
        self.return_setting_button.clicked.connect(self.open_start_page)
        self.return_main_button.clicked.connect(self.open_start_page)
        self.remove_words_button.clicked.connect(self.remove_all_words)
        self.show()

    def remove_all_words(self):
        self.session_manager.session.query(Card).delete()
        self.session_manager.session.commit()

    def bad_label(self):
        self.bad_button.setText(self.bad_line.text())

    def ok_label(self):
        self.ok_button.setText(self.ok_line.text())

    def good_label(self):
        self.good_button.setText(self.good_line.text())

    def open_start_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def open_settings(self):
        self.stackedWidget.setCurrentIndex(1)

    def open_main_page(self):
        self.session_manager.finish_session()
        self.stackedWidget.setCurrentIndex(2)

    def open_old_word_page(self):
        self.session_manager.repeat_session()
        self.stackedWidget.setCurrentIndex(3)
        self.next_repeat_card()

    def open_new_word_page(self):
        self.session_manager.learn_session(30)
        self.learn_next_card()
        self.stackedWidget.setCurrentIndex(4)

    def set_card_text(self, card):
        self.word.setText(card.word)
        self.translation.setText(card.translate)

    def next_repeat_card(self):
        if len(self.session_manager.current_cards) == 0:
            self.open_main_page()
        else:
            self.card = self.session_manager.current_cards.pop()
            if runtime == config.DEBUG:
                print(self.card)
            self.study_word.setText(self.card.word)

    def learn_next_card(self):
        if self.card is not None:
            self.card.card_type = 1
            self.card.last_time = datetime.now()
            self.session_manager.session.add(self.card)
            self.session_manager.session.commit()

        if len(self.session_manager.current_cards) != 0:
            self.card = self.session_manager.current_cards.pop()
        elif len(self.session_manager.current_cards) == 0 and self.card is not None:
            self.card.card_type = 1
            self.card.last_time = datetime.now()
            self.session_manager.session.add(self.card)
            self.session_manager.session.commit()
            self.open_main_page()
        if self.card is not None:
            self.set_card_text(self.card)

    def change_label(self, event):
        if self.study_word.text() != self.card.translate:
            self.study_word.setText(self.card.translate)
        else:
            self.study_word.setText(self.card.word)

    def bad_card(self):
        self.card.learning_type = 0
        self.card.last_time = datetime.now()
        self.session_manager.session.add(self.card)
        self.session_manager.session.commit()
        self.next_repeat_card()

    def ok_card(self):
        self.next_repeat_card()

    def good_card(self):
        self.card.learning_type += 1
        if self.card.learning_type == 6:
            self.card.card_type = 2
        self.card.last_time = datetime.now()
        self.session_manager.session.add(self.card)
        self.session_manager.session.commit()
        self.next_repeat_card()

    def load_new_words(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Load new words", "",
                                                  "All Files (*);;CSV Files (.csv);;TXT Files (.txt)", options=options)
        if file_name:
            session = create_session()
            with open(file_name, 'r', newline='\n') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    session.add(Card(word=row[0], translate=row[1], learning_type=0, card_type=0))
                    try:
                        session.commit()
                    except exc.SQLAlchemyError:
                        pass
                session.close()

    def open_labels_page(self):
        self.stackedWidget.setCurrentIndex(5)


if __name__ == '__main__':
    init('./database.sql')
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
