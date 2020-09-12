from database import Database
from datetime import datetime
from os import system
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
    system("clear")
    amount = input("\nAmount : ")
    date = datetime.now().strftime(time_format)
    Database.addTransaction(database, amount, "Income", "Null", date, "Null")


def addExpense(database):
    system("clear")
    amount = input("\nAmount : ")
    date = datetime.now().strftime(time_format)
    category_no = getCategory()
    note = input("\nNote : ")
    Database.addTransaction(database, amount, "Expense",
                            categories[category_no], date, note)


def viewIncomes(database):
    system("clear")
    transactions = Database.getAllTransactions(database, "type='Income'")

    if transactions:
        table = prettytable.PrettyTable()

        table.field_names = ["Amount", "Date-Time"]
        for transaction in transactions:
            table.add_row([transaction[1], transaction[4]])

        print(table)
    else:
        print("No transactions found.")

    input()


def viewExpenses(database):
    while (True):
        system("clear")
        expenditure = Database.getTotal(database, "type='Expense'")

        if expenditure:
            table = prettytable.PrettyTable()
            table.field_names = ["Category", "Percentage", "Amount"]
            for category in categories.values():
                category_total = Database.getTotal(
                    database, "category='{}'".format(category))
                percentage = category_total * 100 / expenditure
                table.add_row([category, '%.2f' % percentage, category_total])

            print(table)
        else:
            print("No transactions found.")
            input()
            break

        print("\n1. View all expenses\
            \n2. View by category\
            \n0. Back to previous menu")
        choice = input("\n> ")
        system("clear")

        if (choice == '1'):
            table = prettytable.PrettyTable()
            table.field_names = ["Amount", "Category", "Date-Time", "Note"]
            transactions = Database.getAllTransactions(database,
                                                       "type='Expense'")
            for transaction in transactions:
                table.add_row([
                    transaction[1], transaction[3], transaction[4],
                    transaction[5]
                ])
            print(table)

        elif (choice == '2'):
            category_no = getCategory()
            system("clear")
            transactions = Database.getAllTransactions(
                database, "category='{}'".format(categories[category_no]))
            if transactions:
                table = prettytable.PrettyTable()
                table.field_names = ["Amount", "Date-Time", "Note"]
                for transaction in transactions:
                    table.add_row(
                        [transaction[1], transaction[4], transaction[5]])
                print(table)
            else:
                print("No transactions found.")

        else:
            break

        input()