import sqlite3
from datetime import datetime
from os import system
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

def getCategory():
    print("\nCategory : ")
    for i, category in categories.items():
        print(i + ". ", category)
    category_no = input("\n> ")
    return category_no

def add_expense():
    system("clear")
    amount = input("\nAmount : ")
    category_no = getCategory()
    note = input("\nNote : ")
    with conn:
        curr.execute("INSERT INTO {} VALUES (:amount, :date, :note, :category)".format(tablename),
                    {'amount': amount, 'date': datetime.now().strftime(TIME_FORMAT),'note': note, 'category': categories[category_no]})

def delete_expense(id):
    delete_transaction(tablename, id)

def total_expenditure():
    return get_total(tablename)

def total_expenditure_by_category(category):
    total = 0
    with conn:
        curr.execute("SELECT amount FROM {} WHERE category=:category".format(tablename), {'category': category})
        entries = curr.fetchall()
        for entry in entries:
            total += entry[0]
    return total

def get_all_expenses():
    return get_all_transactions(tablename)

def get_all_expenses_by_category(category):
    curr.execute("SELECT rowid, * FROM {} WHERE category=:category".format(tablename), {'category': category})
    return curr.fetchall()

def viewExpenses():
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
            table = prettytable.PrettyTable()
            table.field_names = ["ID", "Amount", "Category", "Date-Time", "Note"]
            transactions = get_all_expenses()
            for transaction in transactions:
                table.add_row([transaction[0], transaction[1], transaction[4], transaction[2], transaction[3]])
            print(table)

        elif (choice == 2):
            category_no = getCategory()
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

        else:
            break

        # print("\n01. Delete an Expense")
        # print("02. Modify an Expense")
        # print("00. Back to previous menu")
        # choice = input("\n> ")
        # try:
        #     choice = int(choice)
        # except:
        #     pass

        # if (choice == 1):
        #     id = input("Enter ID : ")
        #     delete_expense(id)