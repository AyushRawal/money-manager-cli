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

def view_incomes():
    system("clear")
    transactions = get_all_incomes()
    if transactions:
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Amount", "Date-Time", "Note"]
        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[2], transaction[3]])
        print(table)
        
        print("\n01. Delete an Income")
        print("02. Modify an Income")
        print("00. Back to previous menu")
        choice = input("\n> ")
        try:
            choice = int(choice)
        except:
            pass

        if (choice == 1):
            id = input("Enter ID : ")
            try:
                id = int(id)
            except:
                print("Invalid input")
                input()
                return
            delete_income(id)

        elif (choice == 2):
            id = input("Enter ID : ")
            try:
                id = int(id)
            except:
                print("Invalid input")
                input()
                return
            transaction = get_all_transactions(tablename, "WHERE rowid={}".format(id))[0]
            print('\nIf no input is provided previous values will be taken.')
            amount = input("\nAmount : ")
            if (not amount):
                amount = transaction[1]
            note = input("\nNote : ")
            if (not note):
                note = transaction[3]
            with conn:
                curr.execute("UPDATE {} SET amount=:amount, note=:note WHERE rowid={}".format(tablename, id), {'amount': amount, 'note': note})
    else:
        print("No transactions found.")
        input()


