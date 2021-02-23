import sqlite3
from datetime import datetime
from os import system
import prettytable
from transaction import DATABASE_NAME, delete_transaction, get_all_transactions, get_total, TIME_FORMAT

conn = sqlite3.connect(DATABASE_NAME)
curr = conn.cursor()

tablename = "lent"

with conn:
    curr.execute("CREATE TABLE IF NOT EXISTS {} (amount DOUBLE, date TEXT, note TEXT, to_ TEXT)".format(tablename))

def add_loan():
    system("clear")
    amount = input("\nAmount : ")
    to_ = input("\nLent to : ")
    note = input("\nNote : ")
    with conn:
        curr.execute("INSERT INTO {} VALUES (:amount, :date, :note, :to_)".format(tablename),
                    {'amount': amount, 'date': datetime.now().strftime(TIME_FORMAT), 'note': note, 'to_': to_})

def delete_loan(id):
    delete_transaction(tablename, id)

def total_loan():
    return get_total(tablename)

def get_all_loans():
    return get_all_transactions(tablename)

def viewLoans():
    system("clear")
    transactions = get_all_loans()

    if transactions:
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Amount", "Lent to", "Date-Time", "Note"]
        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[4], transaction[2], transaction[3]])
        print(table)
    else:
        print("No transactions found.")

    input()