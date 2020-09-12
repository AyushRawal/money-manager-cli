import sqlite3


class Database:
    schema = {
        "id": "id",
        "amount": "amount",
        "type": "type",
        "category": "category",
        "date": "date",
        "note": "note"
    }
    TableName = "transactions"
    DatabaseName = "transactions.db"
    rows_in_table = 0

    def __init__(self):
        try:
            self.connection = sqlite3.connect(self.DatabaseName)
            self.cursor = self.connection.cursor()
            self.create_table()
            self.rows_in_table = self.count_rows()
        except ValueError:
            print("Unable to initialise or read from database")

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {}
            ({} INT, {} DOUBLE, {} TEXT, {} TEXT, {} TEXT, {} TEXT)""".format(
            self.TableName, *self.schema))
        self.connection.commit()

    def count_rows(self):
        return len(
            self.cursor.execute("SELECT * FROM {}".format(
                self.TableName)).fetchall())

    def addTransaction(self, amount, Type, category, date, note):
        self.rows_in_table = self.rows_in_table + 1
        self.cursor.execute(
            """INSERT INTO {}
            ({}, {}, {}, {}, {}, {}) VALUES (?, ?, ?, ?, ?, ?)""".format(
                self.TableName, *self.schema),
            (self.rows_in_table, amount, Type, category, date, note))
        self.connection.commit()

    def deleteTransaction(self, ID):
        self.rows_in_table = self.rows_in_table - 1
        self.cursor.execute("DELETE FROM {} WHERE id={}".format(
            self.TableName, ID))
        self.connection.commit()

    def getAllTransactions(self, filters="type='Expense' OR type='Income'"):
        transactions = []
        for transaction in self.cursor.execute(
                "SELECT * FROM {} WHERE {}".format(self.TableName, filters)):
            transactions.append(transaction)
        return transactions

    def getTotal(self, filters):
        transactions = []
        for transaction in self.cursor.execute(
                "SELECT amount FROM {} WHERE {}".format(
                    self.TableName, filters)):
            transactions.append(transaction[0])
        return sum(transactions)