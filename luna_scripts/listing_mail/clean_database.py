import sqlite3
import os

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(__file__)
    DATABASE_PATH = os.path.join(THIS_FOLDER, "mailing_list.db")
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()
    cursor.execute('''DELETE FROM emails WHERE valid = ?''', [0])
    db.commit()
    cursor.close()
    db.close()
