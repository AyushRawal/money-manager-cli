from database import Database
from datetime import datetime
import prettytable

time_format = "%Y-%m-%d %H:%M:%S"

categories = {
    "1": "Food and Dining",
    "2": "Education",
    "3": "Gifts",
    "4": "Personal and Grooming"
}

def getCategory():
    print("\nCategory : ")
    for i, category in categories.items():
        print(i + ". ", category)
    category_no = input("\n> ")
    return category_no

def addIncome(database):
    amount = input("\nAmount : ")
    date = datetime.now().strftime(time_format)
    Database.addTransaction(database, amount, "Income", "Null", date)

def addExpense(database):
    amount = input("\nAmount : ")
    date = datetime.now().strftime(time_format)
    category_no = getCategory()
    Database.addTransaction(database, amount, "Expense", categories[category_no], date)

def viewIncomes(database):
    transactions = Database.getAllTransactions(database, "type='Income'")

    table = prettytable.PrettyTable()

    table.field_names = ["Amount", "Date-Time"]
    for transaction in transactions:
        table.add_row([transaction[1], transaction[4]])
    
    print(table)

def viewExpenses(database):
    while (True):
        print(
            "\n1. View all expenses\
            \n2. View by category\
            \n0. Back to previous menu"
        )
        choice = input("\n> ")

        table = prettytable.PrettyTable()

        if (choice == '1'):
            table.field_names = ["Amount", "Category", "Date-Time"]
            transactions = Database.getAllTransactions(database, "type='Expense'")
            for transaction in transactions:
                table.add_row([transaction[1], transaction[3], transaction[4]])

        elif (choice == '2'):
            table.field_names = ["Amount", "Date-Time"]
            category_no = getCategory()
            transactions = Database.getAllTransactions(database, "category='{}'".format(categories[category_no]))
            for transaction in transactions:
                table.add_row([transaction[1], transaction[4]])

        else:
            break

        print(table)