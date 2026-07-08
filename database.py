import sqlite3
import logging

logger = logging.getLogger('database')

class Database:
    def __init__(self):
        self.base = None

    def init_db(self):
        #инициализация бд
        try:
            logger.info('Инициализация базы данных')
            self.base = sqlite3.connect('accounting.db')
            self.base.row_factory = sqlite3.Row
            cursor = self.base.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS accounting (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, type TEXT NOT NULL, 
            color TEXT, stock INTEGER NOT NUll, 
            date TEXT, image_path TEXT)''')
            self.base.commit()
            logger.info('База данных инициализарована успешно')
        except sqlite3.Error as e:
            logger.error(f'Ошибка инициализации: {e}')
            raise

    def get_all(self, order_type=None):
        #получение всех записей
        try:
            cursor = self.base.cursor()
            if order_type:
                parts = order_type.strip().split()
                if len(parts) == 2:
                    col, dir = parts
                    if col == 'color' and dir == 'ASC':
                        cursor.execute('''SELECT * FROM accounting ORDER BY color ASC''')
                    elif col == 'color' and dir == 'DESC':
                        cursor.execute('''SELECT * FROM accounting ORDER BY color DESC''')
                    else:
                        cursor.execute('''SELECT * FROM accounting ORDER BY type''')
                else:
                    cursor.execute('''SELECT * FROM accounting ORDER BY name''')
            else:
                cursor.execute('''SELECT * FROM accounting ORDER BY type''')
            logger.debug('Получение записей')
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Ошибка получения записей: {e}')
            return []

    def delete_record(self, accounting_id):
        #удаление записи
        try:
            cursor = self.base.cursor()
            cursor.execute('''DELETE FROM accounting WHERE id=?''', (accounting_id,))
            self.base.commit()
            logger.info(f'Запись {accounting_id} удалена')
        except sqlite3.Error as e:
            logger.error(f'Ошибка удаления записи: {e}')

    def insert_record(self, data):
        #добавление записи
        try:
            cursor = self.base.cursor()
            cursor.execute('''INSERT INTO accounting 
            (name, type, color, stock, date, image_path) 
            VALUES (?, ?, ?, ?, ?, ?)''',
                           (data['name'], data['type'], data['color'],
                            int(data['stock']), data['date'], data['image_path']))
            self.base.commit()
            logger.info('Запись добавлена')
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f'Ошибка в добавление записи: {e}')
            raise

    def update_record(self, data):
        #обновление записи
        try:
            cursor = self.base.cursor()
            cursor.execute('''UPDATE accounting
            SET name=?, type=?, color=?, stock=?, date=?, image_path=?
            WHERE id=?''',
                           (data['name'], data['type'], data['color'],
                            int(data['stock']), data['date'], data['image_path'], data['id']))
            self.base.commit()
            logger.info('Запись обновлена')
        except sqlite3.Error as e:
            logger.error(f'Ошибка в обновлении записи: {e}')
            raise

    def get_by(self, record_id):
        #получение одной записи
        try:
            cursor = self.base.cursor()
            cursor.execute('''SELECT * FROM accounting WHERE id=?''', (record_id,))
            result = cursor.fetchone()
            if result:
                logger.debug('Получена запись')
            else:
                logger.warning('Запись не найдена')
            return result
        except sqlite3.Error as e:
            logger.error(f'Ошибка получения записи: {e}')
            return None

    def close(self):
        #закрытие бд
        if self.base:
            try:
                self.base.close()
                logger.info('Соединение с бд закрыто')
            except sqlite3.Error as e:
                logger.error(f'Ошибка закрытия бд: {e}')
        self.base = None