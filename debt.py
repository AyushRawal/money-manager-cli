import sqlite3
from datetime import datetime
from os import system
import prettytable
from transaction import DATABASE_NAME, delete_transaction, get_all_transactions, get_total, TIME_FORMAT

conn = sqlite3.connect(DATABASE_NAME)
curr = conn.cursor()

tablename = "borrowed"

with conn:
    curr.execute("CREATE TABLE IF NOT EXISTS {} (amount DOUBLE, date TEXT, note TEXT, from_ TEXT, settled INTEGER)".format(tablename))

def add_debt():
    system("clear")
    amount = input("\nAmount : ")
    from_ = input("\nBorrowed from : ")
    note = input("\nNote : ")
    with conn:
        curr.execute("INSERT INTO {} VALUES (:amount, :date, :note, :from_, :settled)".format(tablename),
                    {'amount': amount, 'date': datetime.now().strftime(TIME_FORMAT), 'note': note, 'from_': from_, 'settled': 0})

def delete_debt(id):
    delete_transaction(tablename, id)

def total_debt():
    return get_total(tablename, "WHERE settled={}".format(0))

def get_all_unsettled_debts():
    return get_all_transactions(tablename, "WHERE settled={}".format(0))

def get_all_settled_debts():
    return get_all_transactions(tablename, "WHERE settled={}".format(1))

def view_debts():
    is_empty = True
    system("clear")
    transactions = get_all_unsettled_debts()
    print("\nUnsettled debts :")
    if transactions:
        is_empty = False
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Amount", "Borrowed from", "Date-Time", "Note"]
        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[4], transaction[2], transaction[3]])
        print(table)
    else:
        print("No transactions found.")

    transactions = get_all_settled_debts()
    print("\nSettled debts :")
    if transactions:
        is_empty = False
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Amount", "Borrowed from", "Date-Time", "Note"]
        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[4], transaction[2], transaction[3]])
        print(table)
    else:
        print("No transactions found.")

    if (not is_empty):
        print("\n01. Delete a Debt")
        print("02. Modify a Debt")
        print("03. Mark as settled / unsettled")
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
            delete_debt(id)

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
            from_ = input("\nLent to : ")
            if (not from_):
                from_ = transaction[4]
            note = input("\nNote : ")
            if (not note):
                note = transaction[3]
            with conn:
                curr.execute("UPDATE {} SET amount=:amount, note=:note, from_=:from_ WHERE rowid={}".format(tablename, id), {'amount': amount, 'note': note, 'from_': from_})

        elif (choice == 3):
            id = input("Enter ID : ")
            try:
                id = int(id)
            except:
                print("Invalid input")
                input()
                return
            transaction = get_all_transactions(tablename, "WHERE rowid={}".format(id))[0]
            if (transaction[5] == 0):
                settled = 1
            else:
                settled = 0
            with conn:
                curr.execute("UPDATE {} SET settled=:settled WHERE rowid={}".format(tablename, id), {'settled': settled})

    else:
        input()