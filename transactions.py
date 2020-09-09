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

def addIncome(database):
    amount = input("\nAmount : ")
    date = datetime.now().strftime(time_format)
    Database.addTransaction(database, amount, "Income", "Null", date)

def addExpense(database):
    amount = input("\nAmount : ")
    print("\nCategory : ")
    for i, category in categories.items():
        print(i + ". ", category)
    category_no = input("\n> ")
    date = datetime.now().strftime(time_format)
    Database.addTransaction(database, amount, "Expense", categories[category_no], date)

def viewTransactionsByType(database, Type):
    transactions = Database.getAllTransactionsByType(database, Type)

    table = prettytable.PrettyTable()

    if (Type == "Income"):
        table.field_names = ["Amount", "Date-Time"]
        for transaction in transactions:
            table.add_row([transaction[1], transaction[4]])
    
    elif (Type == "Expense"):
        table.field_names = ["Amount", "Category", "Date-Time"]
        for transaction in transactions:
            table.add_row([transaction[1], transaction[3], transaction[4]])

    print(table)


