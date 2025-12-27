import sqlite3



class Database:
    def __init__(self, db_name= 'words.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread= False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_settings_table() 


    def create_settings_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main TEXT,
                transcription TEXT,
                translate TEXT,
                tag TEXT)
            ''')
        self.conn.commit()

    def add_word(self, main, transcription, translate, tag='default'):
        self.cursor.execute('''
            INSERT INTO words (main, transcription, translate, tag)
            VALUES (?, ?, ?, ?)
            ''', (main, transcription, translate, tag))
        self.conn.commit()

    def get_random(self, active_tags=None):
        if active_tags and len(active_tags) > 0:
            placeholders = ','.join('?' for _ in active_tags)
            query = f'SELECT main, transcription, translate, tag FROM words WHERE tag IN ({placeholders}) ORDER BY RANDOM() LIMIT 1'
            self.cursor.execute(query, active_tags)
        else:
            self.cursor.execute('SELECT main, transcription, translate, tag FROM words ORDER BY RANDOM() LIMIT 1')

        row = self.cursor.fetchone()
        if row:
            return {'main': row[0], 'transcription': row[1], 'translate': row[2], 'tag': row[3]}
        return None
    
    def get_all_tags(self):
        self.cursor.execute('SELECT DISTINCT tag FROM words')
        return [row[0] for row in self.cursor.fetchall() if row[0]]

    def get_all(self):
        self.cursor.execute('''
            SELECT id, main, transcription, translate, tag FROM words
            ''')
        return self.cursor.fetchall()

    def delete(self, word_id):
        self.cursor.execute('''
            DELETE FROM words WHERE id = ?
            ''', (word_id,))
        self.conn.commit()

    def get_setting(self, key, default=None):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else default

    def set_setting(self, key, value):
        self.cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value))
        )
        self.conn.commit() 

    def update_word(self, word_id, main, trans, translate, tag):
        self.cursor.execute('''
            UPDATE words 
            SET main = ?, transcription = ?, translate = ?, tag = ?
            WHERE id = ?
        ''', (main, trans, translate, tag, word_id))
        self.conn.commit()
