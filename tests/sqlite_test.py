import sqlite3

if __name__ == '__main__':
    db = sqlite3.connect("../luna_scripts/listing_mail/mailing_list.db")
    cursor = db.cursor()
    try:
        cursor.execute('''INSERT INTO emails(email, valid) values(?,?)''', ("adsfs", 1))
        db.commit()
    except:
        pass
    cursor.close()
    db.close()

    db = sqlite3.connect("../luna_scripts/listing_mail/mailing_list.db")
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM emails WHERE valid == 1''')
    print(cursor.fetchall())
    cursor.close()
    db.close()
