import sqlite3

DATABASE_NAME = "transactions.db"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

conn = sqlite3.connect(DATABASE_NAME)
curr = conn.cursor()

def delete_transaction(tablename, id):
    with conn:
        curr.execute("DELETE FROM {} WHERE rowid=:id".format(tablename), {'id': id})

def get_total(tablename):
    total = 0
    curr.execute("SELECT amount FROM {}".format(tablename))
    entries = curr.fetchall()
    for entry in entries:
        total += entry[0]
    return total

def get_all_transactions(tablename):
    curr.execute("SELECT rowid, * FROM {}".format(tablename))
    return curr.fetchall()
