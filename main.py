#!/usr/bin/python3

import expense, income, loan, debt
from os import system
import prettytable

table = prettytable.PrettyTable()

while (True):
    expenditure = expense.total_expenditure()
    total_income = income.total_income()
    total_lent_money = loan.total_loan()
    total_borrowed_money = debt.total_debt()

    system("clear")
    table.header = False
    table.clear_rows()
    table.add_row(["Total Expenditure : ", expenditure])
    table.add_row(["Total Income : ", total_income])
    table.add_row(["Money Left : ", total_income - expenditure])
    table.add_row(["Total Lent Money : ", total_lent_money])
    table.add_row(["Total Borrowed Money : ", total_borrowed_money])
    table.add_row(["Money at hand : ", total_income + total_borrowed_money - expenditure - total_lent_money])
    print(table)

    print("\n01. Add Expense\
        \n02. Add Income\
        \n03. View Expenses\
        \n04. View Incomes\
        \n05. Add Loan\
        \n06. Add Debt\
        \n07. View Loans\
        \n08. View Debts\
        \n00. Exit")

    choice = input("\n> ")
    try:
        choice = int(choice)
    except:
        pass

    if (choice == 1):
        expense.add_expense()
    elif (choice == 2):
        income.add_income()
    elif (choice == 3):
        expense.view_expenses()
    elif (choice == 4):
        income.view_incomes()
    elif (choice == 5):
        loan.add_loan()
    elif (choice == 6):
        debt.add_debt()
    elif (choice == 7):
        loan.view_loans()
    elif (choice == 8):
        debt.view_debts()
    else:
        exit(0)