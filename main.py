import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from ui_main import Ui_mainWindow
import database
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
import os

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

        self._image_path_ = None

        self._bind_signals()

        self._refresh_()

    def _bind_signals(self):
        self.pushButton.clicked.connect(self._add_)
        self.pushButton_2.clicked.connect(self._delete_)
        self.pushButton_3.clicked.connect(self._upload_)
        self.pushButton_4.clicked.connect(self._close_)
        self.pushButton_5.clicked.connect(self._change_)
        self.comboBox.currentIndexChanged.connect(self._sort_)
        self.tableWidget.itemSelectionChanged.connect(self._row_select_)

    def _sort_(self, index):
        if index == 1:
            self._refresh_(order_by='color ASC')
        elif index == 2:
            self._refresh_(order_by='color DESC')
        elif index == 3:
            self._refresh_(order_by='name')
        else:
            self._refresh_()

    def _add_(self):
        if not self.lineEdit.text().strip():
            QMessageBox.warning(self, 'ошибка!', 'поле должно быть заполнено!')
            self.lineEdit.setFocus()
            return

        if not self.lineEdit_2.text().strip():
            QMessageBox.warning(self, 'ошибка!', 'поле должно быть заполнено!')
            self.lineEdit_2.setFocus()
            return

        if self.spinBox.value() < 0:
            QMessageBox.warning(self, 'ошибка!', 'количество не может быть отрицательным')
            self.spinBox.setFocus()
            return

        data = {'name': self.lineEdit_2.text().strip(), 'type': self.lineEdit.text().strip(), 'color': self.lineEdit_4.text().strip(), 'stock': self.spinBox.value(), 'date': self.lineEdit_3.text().strip(), 'image_path': self._image_path_}
        try:
            self.db._insert_(data)
            self._refresh_()
            if self.spinBox.value() < 5:
                QMessageBox.warning(self, 'низкий остаток', 'пополните материал')
            else:
                QMessageBox.information(self, 'ура!', 'запись добавлена')
            self._clear_()
        except Exception as e:
            QMessageBox.critical(self, 'ошибка', f'не удалось добавить запись:\n{e}')

    def _delete_(self):
        select = self.tableWidget.selectionModel().selectedRows()
        if not select:
            QMessageBox.warning(self, 'внимание!', 'вы не выбрали строку!')
            return
        if QMessageBox.question(self, 'подтвердите выбор', 'вы точно хотите удалить данную запись?') == QMessageBox.Yes:
            row = select[0].row()
            self.db._delete_(self.tableWidget.item(row, 0).data(Qt.UserRole))
            self._refresh_()
            self._clear_()
            QMessageBox.information(self, 'ура?', 'запись удалена')

    def _upload_(self):
        path, _ = QFileDialog.getOpenFileName(self, 'выберите фотокарточку', '', 'Images (*.png *.jpg *.jpeg)')
        if not path:
            return
        filename = os.path.basename(path)
        try:
            img = Image.open(path).convert('RGBA')
            img.thumbnail((200, 200), Image.LANCZOS)
            qt_image = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label_5.setPixmap(pixmap)
            self._image_path_ = os.path.join('images', filename)
        except Exception as e:
            QMessageBox.critical(self, 'ошибка(', f'не удалось загрузить фотокарточку:\n{e}')

    def _close_(self):
        self.close()

    def _change_(self):
        select = self.tableWidget.selectionModel().selectedRows()
        if not select:
            QMessageBox.warning(self, 'внимание!', 'вы не выбрали строку!')
            return
        row = select[0].row()
        current = self.db._image_(self.tableWidget.item(row, 0).data(Qt.UserRole))
        if not current:
            return
        final_path = self._image_path_ if self._image_path_ is not None else current['image_path']
        data = {'id': self.tableWidget.item(row, 0).data(Qt.UserRole), 'name': self.lineEdit_2.text().strip(), 'type': self.lineEdit.text().strip(),
                'color': self.lineEdit_4.text().strip(), 'stock': self.spinBox.value(),
                'date': self.lineEdit_3.text().strip(), 'image_path': final_path}
        self.db._update_(data)
        self._refresh_()
        if self.spinBox.value() < 5:
            QMessageBox.warning(self, 'низкий остаток', 'пополните материал')
        else:
            QMessageBox.information(self, 'успешно', 'запись обновлена')

    def _row_select_(self):
        select = self.tableWidget.selectionModel().selectedRows()
        if not select:
            return
        row = select[0].row()
        item = self.tableWidget.item(row, 0)
        record_id = item.data(Qt.UserRole)
        record = self.db._image_(record_id)
        if not record:
            return
        img_path = record['image_path'] or ''
        if img_path and os.path.isfile(img_path):
            try:
                img = Image.open(img_path).convert('RGBA')
                img.thumbnail((200, 200), Image.LANCZOS)
                qt_image = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qt_image)
                self.label_5.setPixmap(pixmap)
            except Exception:
                self.label_5.clear()
        else:
            self.label_5.clear()
        self.lineEdit.setText(self.tableWidget.item(row, 0).text())
        self.lineEdit_2.setText(self.tableWidget.item(row, 1).text())
        self.lineEdit_4.setText(self.tableWidget.item(row, 3).text())
        self.lineEdit_3.setText(self.tableWidget.item(row, 4).text())

        item = self.tableWidget.item(row, 2)
        if item:
            try:
                self.spinBox.setValue(int(item.text()))
            except ValueError:
                self.spinBox.setValue(0)
        else:
            self.spinBox.setValue(0)

    def _refresh_(self, order_by=None):
        self.tableWidget.setRowCount(0)
        items = self.db._get_(order_by)
        if items is None:
            items = []
        for i, j in enumerate(items):
            self.tableWidget.insertRow(i)
            item = QTableWidgetItem(j['type'])
            item.setData(Qt.UserRole, j['id'])
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(j['name']))
            stock_item = QTableWidgetItem(str(j['stock']))
            if j['stock'] < 5:
                stock_item.setBackground(Qt.yellow)
            self.tableWidget.setItem(i, 2, stock_item)
            self.tableWidget.setItem(i, 3, QTableWidgetItem(j['color']))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(j['date']))

    def _clear_(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.spinBox.setValue(0)
        self.label_5.clear()

    def closeEvent(self, event):
        asking = QMessageBox.question(self, 'выход', 'вы точно хотите закрыть приложение?')
        if asking == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Учёт художественных материалов')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
