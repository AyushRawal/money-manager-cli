import sqlite3
from datetime import datetime
from os import system
from sqlite3.dbapi2 import connect
import prettytable
from transaction import DATABASE_NAME, delete_transaction, get_all_transactions, get_total, TIME_FORMAT

conn = sqlite3.connect(DATABASE_NAME)
curr = conn.cursor()

tablename = "expenses"

categories = {
    "1": "Food and Dining",
    "2": "Education",
    "3": "Gifts",
    "4": "Personal and Grooming",
    "5": "Travel and Transportation",
    "6": "Other"
}

with conn:
    curr.execute("CREATE TABLE IF NOT EXISTS {} (amount DOUBLE, date TEXT, note TEXT, category TEXT)".format(tablename))

def get_category():
    print("\nCategory : ")
    for i, category in categories.items():
        print(i + ". ", category)
    category_no = input("\n> ")
    return category_no

def add_expense():
    system("clear")
    amount = input("\nAmount : ")
    category_no = get_category()
    note = input("\nNote : ")
    with conn:
        curr.execute("INSERT INTO {} VALUES (:amount, :date, :note, :category)".format(tablename),
                    {'amount': amount, 'date': datetime.now().strftime(TIME_FORMAT),'note': note, 'category': categories[category_no]})

def delete_expense(id):
    delete_transaction(tablename, id)

def total_expenditure():
    return get_total(tablename)

def total_expenditure_by_category(category):
    return get_total(tablename, 'WHERE category="{}"'.format(category))

def get_all_expenses():
    return get_all_transactions(tablename)

def get_all_expenses_by_category(category):
    return get_all_transactions(tablename, 'WHERE category="{}"'.format(category))

def view_expenses():
    while (True):
        system("clear")
        expenditure = total_expenditure()

        if expenditure:
            table = prettytable.PrettyTable()
            table.field_names = ["Category", "Percentage", "Amount"]
            for category in categories.values():
                category_total = total_expenditure_by_category(category)
                percentage = category_total * 100 / expenditure
                table.add_row([category, '%.2f' % percentage, category_total])
            print(table)
        else:
            print("No transactions found.")
            input()
            break

        print("\n01. View all expenses\
            \n02. View by category\
            \n00. Back to previous menu")

        choice = input("\n> ")
        try:
            choice = int(choice)
        except:
            pass
        system("clear")

        if (choice == 1):
            transactions = get_all_expenses()
            if transactions:
                table = prettytable.PrettyTable()
                table.field_names = ["ID", "Amount", "Category", "Date-Time", "Note"]
                for transaction in transactions:
                    table.add_row([transaction[0], transaction[1], transaction[4], transaction[2], transaction[3]])
                print(table)
            else:
                print("No transactions found.")
                input()
                continue

        elif (choice == 2):
            category_no = get_category()
            system("clear")
            transactions = get_all_expenses_by_category(categories[category_no])
            if transactions:
                table = prettytable.PrettyTable()
                table.field_names = ["ID", "Amount", "Date-Time", "Note"]
                for transaction in transactions:
                    table.add_row([transaction[0], transaction[1], transaction[2], transaction[3]])
                print(table)
            else:
                print("No transactions found.")
                input()
                continue

        else:
            break

        print("\n01. Delete an Expense")
        print("02. Modify an Expense")
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
                break
            delete_expense(id)

        elif (choice == 2):
            id = input("Enter ID : ")
            try:
                id = int(id)
            except:
                print("Invalid input")
                break
            transaction = get_all_transactions(tablename, "WHERE rowid={}".format(id))[0]
            print('\nIf no input is provided previous values will be taken.')
            amount = input("\nAmount : ")
            if (not amount):
                amount = transaction[1]
            category_no = get_category()
            if (not category_no):
                category = transaction[4]
            else:
                category = categories[category_no] 
            note = input("\nNote : ")
            if (not note):
                note = transaction[3]
            with conn:
                curr.execute("UPDATE {} SET amount=:amount, note=:note, category=:category WHERE rowid={}".format(tablename, id), {'amount': amount, 'note': note, 'category': category})