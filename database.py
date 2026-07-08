import sqlite3

class Database:
    def __init__(self):
        self.base = None

    def init_db(self):
        self.base = sqlite3.connect('accounting.db')
        self.base.row_factory = sqlite3.Row
        cursor = self.base.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounting (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, type TEXT NOT NULL, 
        color TEXT, stock INTEGER NOT NUll, 
        date TEXT, image_path TEXT)''')
        self.base.commit()

    def get_all(self, order_type=None):
        cursor = self.base.cursor()
        columns = ['id', 'name', 'type', 'color', 'stock', 'date', 'image_path']
        directions = ['ASC', 'DESC']
        query = '''SELECT * FROM accounting'''
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
        return cursor.fetchall()

    def delete_record(self, accounting_id):
        cursor = self.base.cursor()
        cursor.execute('''DELETE FROM accounting WHERE id=?''', (accounting_id,))
        self.base.commit()

    def insert_record(self, data):
        cursor = self.base.cursor()
        cursor.execute('''INSERT INTO accounting (name, type, color, stock, date, image_path) VALUES (?, ?, ?, ?, ?, ?)''', (data['name'], data['type'], data['color'], int(data['stock']), data['date'], data['image_path']))
        self.base.commit()

    def update_record(self, data):
        cursor = self.base.cursor()
        cursor.execute('''UPDATE accounting SET name=?, type=?, color=?, stock=?, date=?, image_path=? WHERE id=?''', (data['name'], data['type'], data['color'], int(data['stock']), data['date'], data['image_path'], data['id']))
        self.base.commit()

    def get_by(self, record_id):
        cursor = self.base.cursor()
        cursor.execute('''SELECT * FROM accounting WHERE id=?''', (record_id,))
        return cursor.fetchone()

    def close(self):
        if self.base:
            self.base.close()
            self.base = None