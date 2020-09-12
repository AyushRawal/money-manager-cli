#!/usr/bin/python3

from database import Database
import transactions
from os import system
import prettytable

database = Database()
table = prettytable.PrettyTable()

while (True):
    expenditure = Database.getTotal(database, "type='Expense'")
    total_income = Database.getTotal(database, "type='Income'")

    system("clear")
    table.header = False
    table.clear_rows()
    table.add_row(["Total Expenditure : ", expenditure])
    table.add_row(["Total Income : ", total_income])
    table.add_row(["Money left : ", total_income - expenditure])
    print(table)

    print("\n1. Add Expense\
        \n2. Add Income\
        \n3. View Expenses\
        \n4. View Incomes\
        \n0. Exit")

    choice = input("\n> ")

    if (choice == '1'):
        transactions.addExpense(database)
    elif (choice == '2'):
        transactions.addIncome(database)
    elif (choice == '3'):
        transactions.viewExpenses(database)
    elif (choice == '4'):
        transactions.viewIncomes(database)
    else:
        exit(0)