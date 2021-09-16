from functions import *
from genshin import *
from user_interface import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PIL import ImageQt

#tutorial: https://youtu.be/XXPNpdaK9WA
# 320, 1024

class Window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.updateParty.clicked.connect(self.updateParty)
        self.ui.updateCurrentCharacter.clicked.connect(self.updateCurrentCharacter)
    
    def updateParty(self):
        party = get_party_members_from_name()
        self.ui.character1.setPixmap(ImageQt.toqpixmap(party[0].get_gacha_card_image()))
        self.ui.character2.setPixmap(ImageQt.toqpixmap(party[1].get_gacha_card_image()))
        self.ui.character3.setPixmap(ImageQt.toqpixmap(party[2].get_gacha_card_image()))
        self.ui.character4.setPixmap(ImageQt.toqpixmap(party[3].get_gacha_card_image()))
    
    def updateCurrentCharacter(self):
        current_character = get_current_character()
        factor = 0.5
        if current_character == 1:
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.ui.character1.pixmap())
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawLine(10, 10, self.rect().width() -10 , 10)
        elif current_character == 2:
            image = darken_pixmap(self.ui.character1.pixmap(), factor)
            self.ui.character1.setPixmap(image)
            image = darken_pixmap(self.ui.character3.pixmap(), factor)
            self.ui.character3.setPixmap(image)
            image = darken_pixmap(self.ui.character4.pixmap(), factor)
            self.ui.character4.setPixmap(image)
        elif current_character == 3:
            image = darken_pixmap(self.ui.character1.pixmap(), factor)
            self.ui.character1.setPixmap(image)
            image = darken_pixmap(self.ui.character2.pixmap(), factor)
            self.ui.character2.setPixmap(image)
            image = darken_pixmap(self.ui.character4.pixmap(), factor)
            self.ui.character4.setPixmap(image)
        elif current_character == 4:
            image = darken_pixmap(self.ui.character1.pixmap(), factor)
            self.ui.character1.setPixmap(image)
            image = darken_pixmap(self.ui.character2.pixmap(), factor)
            self.ui.character2.setPixmap(image)
            image = darken_pixmap(self.ui.character3.pixmap(), factor)
            self.ui.character3.setPixmap(image)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())