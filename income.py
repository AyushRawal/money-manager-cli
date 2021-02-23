import sqlite3
from datetime import datetime
from os import system
import prettytable
from transaction import DATABASE_NAME, delete_transaction, get_all_transactions, get_total, TIME_FORMAT

conn = sqlite3.connect(DATABASE_NAME)
curr = conn.cursor()

tablename = "incomes"

with conn:
    curr.execute("CREATE TABLE IF NOT EXISTS {} (amount DOUBLE, date TEXT, note TEXT)".format(tablename))

def add_income():
    system("clear")
    amount = input("\nAmount : ")
    note = input("\nNote : ")
    with conn:
        curr.execute("INSERT INTO {} VALUES (:amount, :date, :note)".format(tablename),
                    {'amount': amount, 'date': datetime.now().strftime(TIME_FORMAT), 'note': note})

def delete_income(id):
    delete_transaction(tablename, id)

def total_income():
    return get_total(tablename)

def get_all_incomes():
    return get_all_transactions(tablename)

def viewIncomes():
    system("clear")
    transactions = get_all_incomes()

    if transactions:
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Amount", "Date-Time", "Note"]
        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[2], transaction[3]])
        print(table)
    else:
        print("No transactions found.")

    input()
