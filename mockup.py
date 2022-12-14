
from PyQt5 import QtCore, QtGui, QtWidgets
from api import DictionaryRestClient
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc, threading

class Vocabulary:
    def __init__(self, word, ipa, pronunciation, meanings):
        self.word = word
        self.pronunciation = pronunciation
        self.meanings = meanings
        self.ipa = ipa

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(470, 273)
        MainWindow.setMaximumSize(500, 280)
        MainWindow.setMinimumSize(500, 280)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.word_label = QtWidgets.QLabel(self.centralwidget)
        self.word_label.setGeometry(QtCore.QRect(10, 65, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.word_label.setFont(font)
        self.word_label.setObjectName("word_label")
        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setGeometry(QtCore.QRect(10, 10, 210, 30))
        self.search_bar.setObjectName("search_bar")
        self.meanings_label = QtWidgets.QLabel(self.centralwidget)
        self.meanings_label.setGeometry(QtCore.QRect(10, 190, 100, 30))
        self.meanings_label.setFont(font)
        self.meanings_label.setObjectName("meanings_label")
        self.pronunciation_label = QtWidgets.QLabel(self.centralwidget)
        self.pronunciation_label.setGeometry(QtCore.QRect(10, 110, 150, 23))
        self.pronunciation_label.setFont(font)
        self.pronunciation_label.setObjectName("pronunciation_label")
        self.word_content = QtWidgets.QLineEdit(self.centralwidget)
        self.word_content.setFont(font)
        self.word_content.setGeometry(QtCore.QRect(150, 60, 321, 30))
        self.word_content.setReadOnly(True)
        self.word_content.setObjectName("word_content")
        self.pronouns_button = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.pronouns_button.setGeometry(QtCore.QRect(150, 100, 321, 41))
        self.pronouns_button.setBaseSize(QtCore.QSize(20, 20))
        self.pronouns_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pronouns_button.setFont(font)
        self.pronouns_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icon/Speaker_Icon.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pronouns_button.setIcon(icon)
        self.pronouns_button.setAutoRepeatInterval(50)
        self.pronouns_button.setObjectName("pronouns_button")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(380, 10, 90, 30))
        self.search_button.setObjectName("search_button")
        self.search_button.setFont(font)
        self.meanings_content = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.meanings_content.setFont(font)
        self.meanings_content.setGeometry(QtCore.QRect(150, 150, 321, 100))
        self.meanings_content.setReadOnly(True)
        self.meanings_content.setObjectName("meanings_content")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 470, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.dictionary = QtWidgets.QComboBox(self.centralwidget)

        self.dictionary.setFont(font)
        self.dictionary.setGeometry(QtCore.QRect(230, 10, 140, 30))
        self.dictionary.setObjectName("dictionary")
        self.dictionary.setCurrentIndex(1)
        self.dictionary.addItem("Cambridge")
        self.dictionary.addItem("Oxford")
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.setUp()


    def setUp(self):
        self.search_button.clicked.connect(self.search)

        self.pronouns_button.clicked.connect(self.pronouns)

        self.vocabulary = Vocabulary('', '', '', '')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.word_label.setText(_translate("MainWindow", "Word"))
        self.meanings_label.setText(_translate("MainWindow", "Meanings"))
        self.pronunciation_label.setText(_translate("MainWindow", "Pronunciation"))

    def reset_view(self):
        self.meanings_content.setPlainText("")
        self.vocabulary = Vocabulary('', '', '', '')
        self.meanings_content.setPlainText("")
        self.pronouns_button.setText("")

    def search(self):
        client = DictionaryRestClient("http://localhost:8082/api/vocabulary/")
        word = client.get(self.dictionary.currentText().upper(), self.search_bar.text())

        if word is None:
            self.reset_view()
            self.word_content.setText("NOT FOUND")
            return

        vocabulary_class = None if word['vocabularyClass'] is None else '(' + word['vocabularyClass'] + ')'
        self.word_content.setText(word['word'] + vocabulary_class)
        pronunciation = word['pronunciation']

        first_pronunciation = list(pronunciation)[0] if list(pronunciation).__len__() >= 1 else None
        self.pronouns_button.setText(first_pronunciation)
        meanings = word['meanings']
        self.meanings_content.setPlainText(self.get_meanings(meanings))
        prouncation_path = pronunciation[first_pronunciation][1] if first_pronunciation is not None and pronunciation[first_pronunciation] is not None else ""
        self.vocabulary = Vocabulary(word['word'], first_pronunciation, prouncation_path, meanings)

    def get_meanings(self, meanings):
        meanings_as_string = ''
        for meaning in meanings:
            meanings_as_string += '-' + meaning + '\n'
        return meanings_as_string

    def pronouns(self):
        thread = threading.Thread(target=self.play_audio, args=("PRONOUNS ERROR", self.vocabulary.pronunciation))
        thread.start()
        thread.join()

    def play_audio(self, error, url):
        try:
            if(url == ""):
                return
            p = vlc.MediaPlayer(url)
            p.play()
        except:
            print(error)
            return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
