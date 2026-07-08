import sys
import os
import logging

from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHeaderView,
    QMessageBox, QTableWidgetItem, QFileDialog, QShortcut
)
from PIL import Image

from ui_main import Ui_mainWindow
import database

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('main')

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image_path = None

        self.setWindowTitle('Учёт художественных материалов')
        self.resize(850, 650)
        self.setMinimumSize(850, 650)

        #подключаем базу данных
        self.db = database.Database()
        self.db.init_db()

        self._setup_ui()
        self._bind_signals()
        self._refresh_table()

        logger.info('Приложение успешно запущено')

    def _setup_ui(self):
        #доработка конвертированного интерфейса
        self.setStyleSheet('QMainWindow {background-color: #F0E68C;}'
                           'QTableWidget {gridline-color: #8DB76B;}'
                           )

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.btn_add.setFixedSize(100, 40)
        self.btn_delete.setFixedSize(100, 40)
        self.btn_load.setFixedSize(100, 40)
        self.btn_close.setFixedSize(100, 40)
        self.btn_edit.setFixedSize(100, 40)
        self.lbl_image.setFixedSize(200, 200)

        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def _bind_signals(self):
        #привязка сигналов
        self.btn_add.clicked.connect(self._on_add)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_load.clicked.connect(self._on_load_image)
        self.btn_close.clicked.connect(self._on_close)
        self.btn_edit.clicked.connect(self._on_edit)
        self.comboBox.currentIndexChanged.connect(self._on_sort)
        self.tableWidget.itemSelectionChanged.connect(self._on_select_row)

        #горячие клавиши
        QShortcut(QKeySequence('Ctrl+K'), self).activated.connect(self._on_add)
        QShortcut(QKeySequence('Del'), self).activated.connect(self._on_delete)
        QShortcut(QKeySequence('Ctrl+L'), self).activated.connect(self._on_load_image)
        QShortcut(QKeySequence('Ctrl+C'), self).activated.connect(self._on_close)
        QShortcut(QKeySequence('Ctrl+E'), self).activated.connect(self._on_edit)

    def _on_sort(self, index):
        #сортировка записей
        if index == 1:
            self._refresh_table(order_by='color ASC')
        elif index == 2:
            self._refresh_table(order_by='color DESC')
        elif index == 3:
            self._refresh_table(order_by='name')
        else:
            self._refresh_table()

    def _on_add(self):
        #добавление записи
        if not self.le_type.text().strip():
            QMessageBox.warning(self,
                                'ошибка!',
                                'поле должно быть заполнено!')
            self.le_type.setFocus()
            return

        if not self.le_name.text().strip():
            QMessageBox.warning(self,
                                'ошибка!',
                                'поле должно быть заполнено!')
            self.le_name.setFocus()
            return

        if self.sb_stock.value() < 0:
            QMessageBox.warning(self,
                                'ошибка!',
                                'количество не может быть отрицательным')
            self.sb_stock.setFocus()
            return
        date_match = self.le_date.text().strip()
        valid_date = None
        if date_match:
            fmt = '%Y-%m-%d'
            try:
                parsed_date = datetime.strptime(date_match, fmt)
                valid_date = parsed_date.strftime(fmt)
            except ValueError:
                QMessageBox.warning(self,
                                    'ошибка',
                                    'даты не существует')
                self.le_date.setFocus()
                return

        image_path = self.image_path
        data = {'name': self.le_name.text().strip(),
                'type': self.le_type.text().strip(),
                'color': self.le_color.text().strip(),
                'stock': self.sb_stock.value(),
                'date': valid_date,
                'image_path': image_path}
        try:
            self.db.insert_record(data)
            logger.info('Запись добавлена')
            self._refresh_table()
            if self.sb_stock.value() < 5:
                QMessageBox.warning(self,
                                    'низкий остаток',
                                    'пополните материал')
            else:
                QMessageBox.information(self,
                                        'ура!',
                                        'запись добавлена')
            self._clear_fields()
        except Exception as e:
            logger.error(f'Ошибка в добавлении записи: {e}')
            QMessageBox.critical(self,
                                 'ошибка',
                                 f'не удалось добавить запись:\n{e}')

    def _on_delete(self):
        #удаление записи
        select = self.tableWidget.selectionModel().selectedRows()
        if not select:
            QMessageBox.warning(self,
                                'внимание!',
                                'вы не выбрали строку!')
            return
        if QMessageBox.question(self,
                                'подтвердите выбор',
                                'вы точно хотите удалить данную запись?') == QMessageBox.Yes:
            row = select[0].row()
            self.db.delete_record(self.tableWidget.item(row, 0).data(Qt.UserRole))
            self._refresh_table()
            self._clear_fields()
            logger.info('Запись удалена')
            QMessageBox.information(self,
                                    'ура?',
                                    'запись удалена')

    def _on_load_image(self):
        #загрузка изображений
        path, _ = QFileDialog.getOpenFileName(self,
                                              'выберите фотокарточку',
                                              '',
                                              'Images (*.png *.jpg *.jpeg)')
        if not path:
            return
        filename = os.path.basename(path)
        try:
                img = Image.open(path).convert('RGBA')
                img.thumbnail((200, 200), Image.LANCZOS)
                qt_image = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qt_image)
                self.lbl_image.setPixmap(pixmap)
                logger.info('Изображение добавлено')
                self.image_path = os.path.join('images', filename)
        except Exception as e:
            logger.error(f'Ошибка в загрузке изображения: {e}')
            QMessageBox.critical(self,
                                 'ошибка(',
                                 f'не удалось загрузить фотокарточку:\n{e}')

    def _on_close(self):
        #закрытие через кнопку
        self.close()

    def _on_edit(self):
        #редактирование записи
        select = self.tableWidget.selectionModel().selectedRows()
        if not select:
            QMessageBox.warning(self,
                                'внимание!',
                                'вы не выбрали строку!')
            return
        row = select[0].row()
        current = self.db.get_by(self.tableWidget.item(row, 0).data(Qt.UserRole))
        if not current:
            return
        final_path = self.image_path if self.image_path is not None else current['image_path']

        date_text = self.le_date.text().strip()
        valid_date = None
        if date_text:
            fmt = '%Y-%m-%d'
            try:
                dt = datetime.strptime(date_text, fmt)
                valid_date = dt.strftime(fmt)
            except ValueError:
                QMessageBox.warning(self,
                                    'ошибка', f'даты не существует')
                self.le_date.setFocus()
                return

        data = {'id': self.tableWidget.item(row, 0).data(Qt.UserRole),
                'name': self.le_name.text().strip(),
                'type': self.le_type.text().strip(),
                'color': self.le_color.text().strip(),
                'stock': self.sb_stock.value(),
                'date': valid_date,
                'image_path': final_path}
        self.db.update_record(data)
        logger.info('Запись обновлена')
        self._refresh_table()
        if self.sb_stock.value() < 5:
            QMessageBox.warning(self,
                                'низкий остаток',
                                'пополните материал')
        else:
            QMessageBox.information(self,
                                    'успешно',
                                    'запись обновлена')

    def _on_select_row(self):
        #заполнение формы при выборе строки
        select = self.tableWidget.selectionModel().selectedRows()
        if not select:
            return
        row = select[0].row()
        item = self.tableWidget.item(row, 0)
        record_id = item.data(Qt.UserRole)
        record = self.db.get_by(record_id)
        if not record:
            return
        self.image_path = None
        img_path = record['image_path'] or ''
        if img_path and os.path.isfile(img_path):
            try:
                img = Image.open(img_path).convert('RGBA')
                img.thumbnail((200, 200), Image.LANCZOS)
                qt_image = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qt_image)
                self.lbl_image.setPixmap(pixmap)
            except Exception:
                logger.error('Изображение не добавлено на экран')
                self.lbl_image.clear()
        else:
            self.lbl_image.clear()
        self.le_type.setText(record['type'])
        self.le_name.setText(record['name'])
        self.le_color.setText(record['color'])
        self.le_date.setText(record['date'])

        item = self.tableWidget.item(row, 2)
        if item:
            try:
                self.sb_stock.setValue(int(item.text()))
            except ValueError:
                self.sb_stock.setValue(0)
        else:
            self.sb_stock.setValue(0)

    def _refresh_table(self, order_by=None):
        #обновление таблицы
        self.tableWidget.setRowCount(0)
        items = self.db.get_all(order_by)
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

    def _clear_fields(self):
        #очистка полей
        self.le_type.clear()
        self.le_name.clear()
        self.le_date.clear()
        self.le_color.clear()
        self.sb_stock.setValue(0)
        self.lbl_image.clear()

    def closeEvent(self, event):
        #закрытие через крестик
        reply = QMessageBox.question(self,
                                     'выход',
                                     'вы точно хотите закрыть приложение?')
        if reply == QMessageBox.Yes:
            logger.info('Приложение закрыто')
            if hasattr(self, 'db'):
                self.db.close()
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
