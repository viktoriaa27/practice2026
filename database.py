import sqlite3

class Database:
    def __init__(self):
        self.base = None

    def _init_db_(self):
        self.base = sqlite3.connect('accounting.db')
        self.base.row_factory = sqlite3.Row
        cursor = self.base.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounting (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, type TEXT NOT NULL, color TEXT NOT NULL, stock INTEGER NOT NULL, date TEXT NOT NULL, image_path TEXT NOT NULL)''')

    def _get_(self):
        cursor = self.base.cursor()
        cursor.execute('''SELECT id, name, type, color, stock, date, image_path FROM accounting OTDER BY name''')
        return cursor.fetchall()

    def _delete_(self, accounting_id):
        cursor = self.base.cursor()
        cursor.execute('''DELETE FROM accounting WHERE id=?''', (accounting_id))
        self.base.commit()

    def _insert_(self, data):
        cursor = self.base.cursor()
        cursor.execute('''INSERT INTO accounting (name, type, color, stock, date, image_path) VALUES (?, ?, ?, ?, ?, ?)''', (data['name'], data['type'], data['color'], int(data['stock']), data['date'], data['image_path']))
        self.base.commit()

    def _update_(self, data):
        cursor = self.base.cursor()
        cursor.execute('''UPDATE accounting SET name=?, type=?, color=?, stock=?, date=?, image_path=? WHERE id=?''', (data['name'], data['type'], data['color'], int(data['stock']), data['date'], data['image_path'], data['id']))
        self.base.commit()