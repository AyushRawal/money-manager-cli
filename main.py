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
    total_lent_money = Database.getTotal(database, "type='Loan'")
    total_borrowed_money = Database.getTotal(database, "type='Debt'")

    system("clear")
    table.header = False
    table.clear_rows()
    table.add_row(["Total Expenditure : ", expenditure])
    table.add_row(["Total Income : ", total_income])
    table.add_row(["Money Left : ", total_income - expenditure])
    table.add_row(["Total Lent Money : ", total_lent_money])
    table.add_row(["Total Borrowed Money : ", total_borrowed_money])
    print(table)

    print("\n1. Add Expense\
        \n2. Add Income\
        \n3. View Expenses\
        \n4. View Incomes\
        \n5. Add Loan\
        \n6. Add Debt\
        \n7. View Loans\
        \n8. View Debts\
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
    elif (choice == '5'):
        transactions.addLoan(database)
    elif (choice == '6'):
        transactions.addDebt(database)
    elif (choice == '7'):
        transactions.viewLoans(database)
    elif (choice == '8'):
        transactions.viewDebts(database)
    else:
        exit(0)