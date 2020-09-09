import sqlite3

class Database:
    schema = {
        "id" : "id",
        "amount" : "amount",
        "type" : "type",
        "category" : "category",
        "date" : "date"
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
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS {}
            ({} INT, {} DOUBLE, {} TEXT, {} TEXT, {} TEXT)""".format(
                self.TableName, *self.schema
            )
        )
        self.connection.commit()

    def count_rows(self):
        return len(
            self.cursor.execute("SELECT * FROM {}".format(self.TableName)).fetchall()
        )

    def addTransaction(self, amount, Type, category, date):
        self.rows_in_table = self.rows_in_table + 1
        self.cursor.execute(
            """INSERT INTO {}
            ({}, {}, {}, {}, {}) VALUES (?, ?, ?, ?, ?)""".format(self.TableName, *self.schema),
            (self.rows_in_table, amount, Type, category, date)
        )
        self.connection.commit()

    def deleteTransaction(self, ID):
        self.rows_in_table = self.rows_in_table - 1
        self.cursor.execute("DELETE FROM {} WHERE id={}".format(self.TableName, ID))
        self.connection.commit()

    def getAllTransactionsByType(self, Type):
        transactions = []
        for transaction in self.cursor.execute("SELECT * FROM {} WHERE type='{}'".format(self.TableName, Type)):
            transactions.append(transaction)
        return transactions

    def getTotalByType(self, Type):
        transactions = []
        for transaction in self.cursor.execute("SELECT amount FROM {} WHERE type='{}'".format(self.TableName, Type)):
            transactions.append(transaction[0])
        return sum(transactions)