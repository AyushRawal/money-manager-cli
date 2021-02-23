import sqlite3
from datetime import datetime
from os import system
import prettytable
from transaction import DATABASE_NAME, delete_transaction, get_all_transactions, get_total, TIME_FORMAT

conn = sqlite3.connect(DATABASE_NAME)
curr = conn.cursor()

tablename = "borrowed"

with conn:
    curr.execute("CREATE TABLE IF NOT EXISTS {} (amount DOUBLE, date TEXT, note TEXT, from_ TEXT)".format(tablename))

def add_debt():
    system("clear")
    amount = input("\nAmount : ")
    from_ = input("\nBorrowed from : ")
    note = input("\nNote : ")
    with conn:
        curr.execute("INSERT INTO {} VALUES (:amount, :date, :note, :from_)".format(tablename),
                    {'amount': amount, 'date': datetime.now().strftime(TIME_FORMAT), 'note': note, 'from_': from_})

def delete_debt(id):
    delete_transaction(tablename, id)

def total_debt():
    return get_total(tablename)

def get_all_debts():
    return get_all_transactions(tablename)

def viewDebts():
    system("clear")
    transactions = get_all_debts()

    if transactions:
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Amount", "Borrowed from", "Date-Time", "Note"]
        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[4], transaction[2], transaction[3]])
        print(table)
    else:
        print("No transactions found.")

    input()