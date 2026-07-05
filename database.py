import sqlite3

class Database:
    def __init__(self):
        self.base = None

    def _init_db_(self):
        self.base = sqlite3.connect('accounting.db')
        self.base.row_factory = sqlite3.Row
        cursor = self.base.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounting (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, type TEXT NOT NULL, color TEXT , stock INTEGER NOT NUll, date TEXT, image_path TEXT)''')
        self.base.commit()

    def _get_(self, order_type=None):
        cursor = self.base.cursor()
        if order_type:
            parts = order_type.strip().split()
            if len(parts) == 2:
                col, dir = parts
                cursor.execute(
                    f'''SELECT id, name, type, color, stock, date, image_path FROM accounting ORDER BY {col} {dir}''')
            else:
                cursor.execute(
                    f'''SELECT id, name, type, color, stock, date, image_path FROM accounting ORDER BY name''')
        else:
            cursor.execute(
                f'''SELECT id, name, type, color, stock, date, image_path FROM accounting ORDER BY type''')
        return cursor.fetchall()

    def _delete_(self, accounting_id):
        cursor = self.base.cursor()
        cursor.execute('''DELETE FROM accounting WHERE id=?''', (accounting_id,))
        self.base.commit()

    def _insert_(self, data):
        cursor = self.base.cursor()
        cursor.execute('''INSERT INTO accounting (name, type, color, stock, date, image_path) VALUES (?, ?, ?, ?, ?, ?)''', (data['name'], data['type'], data['color'], int(data['stock']), data['date'], data['image_path']))
        self.base.commit()

    def _update_(self, data):
        cursor = self.base.cursor()
        cursor.execute('''UPDATE accounting SET name=?, type=?, color=?, stock=?, date=?, image_path=? WHERE id=?''', (data['name'], data['type'], data['color'], int(data['stock']), data['date'], data['image_path'], data['id']))
        self.base.commit()

    def _image_(self, im_id):
        cursor = self.base.cursor()
        cursor.execute('''SELECT * FROM accounting WHERE id=?''', (im_id,))
        return cursor.fetchone()