from genshin import *
from user_interface import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap

#tutorial: https://youtu.be/XXPNpdaK9WA
# 320, 1024

class Window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.updateParty.clicked.connect(self.updateParty)
    
    def updateParty(self):
        party = get_party_members_from_name()
        self.ui.character1.setPixmap(QPixmap(party[0].get_image_path()))
        self.ui.character2.setPixmap(QPixmap(party[1].get_image_path()))
        self.ui.character3.setPixmap(QPixmap(party[2].get_image_path()))
        self.ui.character4.setPixmap(QPixmap(party[3].get_image_path()))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())