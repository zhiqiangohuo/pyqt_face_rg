import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QLineEdit

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 textbox'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
        self.name = ''

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.button = QPushButton('show text', self)
        self.button.move(20, 80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.button.clicked.connect(self.close)
        self.show()
    def __str__(self):
        return self.name
    @pyqtSlot()
    def on_click(self):
        self.name = self.textbox.text()
        QMessageBox.question(self, "Message", 'You typed:' + self.name, 
                             QMessageBox.Ok, QMessageBox.Ok)
        """打印完毕之后清空文本框"""
        return self.name
        # self.textbox.setText('')
    
def get_name():
    # app = QApplication(sys.argv)
    ex = App()
    # app.exit(app.exec_())
    name = ex.name
    return name
# if __name__ == '__main__':
    
#     print(get_name())
    
