import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import Qt
from ui_main import Ui_mainWindow
import database

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Учёт художественных материалов')
        #так как дизайн может еще раз измениться, некоторые изменения к нему и вся логика пока пишется здесь
        self.resize(850, 650)
        self.setMinimumSize(850, 650)
        self.setMaximumSize(1700, 1300)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton.setFixedSize(100, 40)
        self.pushButton_2.setFixedSize(100, 40)
        self.pushButton_3.setFixedSize(100, 40)
        self.pushButton_4.setFixedSize(100, 40)
        self.pushButton_5.setFixedSize(100, 40)
        self.label_5.setFixedSize(200, 200)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.db = database.Database()
        self.db._init_db_()

        self._bind_signals()

    def _bind_signals(self):
        self.pushButton.clicked.connect(self._add_)
        self.pushButton_2.clicked.connect(self._delete_)
        self.pushButton_3.clicked.connect(self._upload_)
        self.pushButton_4.clicked.connect(self._close_)
        self.pushButton_5.clicked.connect(self._change_)
        self.lineEdit.returnPressed.connect(self._type_)
        self.lineEdit_2.returnPressed.connect(self._name_)
        self.lineEdit_3.returnPressed.connect(self._color_)
        self.lineEdit_4.returnPressed.connect(self._date_)
        self.spinBox.valueChanged.connect(self._stock_)
        self.comboBox.currentIndexChanged.connect(self._sort_)

    def _add_(self):
        print('добавить')

    def _delete_(self):
        print('удалить')

    def _upload_(self):
        print('загрузить')

    def _close_(self):
        print('закрыть')

    def _change_(self):
        print('изменить')

    def _type_(self):
        text = self.lineEdit.text()
        print(text)

    def _name_(self):
        text = self.lineEdit_2.text()
        print(text)

    def _color_(self):
        text = self.lineEdit_3.text()
        print(text)

    def _date_(self):
        text = self.lineEdit_4.text()
        print(text)

    def _stock_(self):
        text = self.spinBox.value()
        print(text)

    def _sort_(self):
        print('сортировка')

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Учёт художественных материалов')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
