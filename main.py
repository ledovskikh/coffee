import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_coffee_data()

    def load_coffee_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()

        connection.close()

        self.tableWidget.setRowCount(len(coffee_data))

        for row_index, row_data in enumerate(coffee_data):
            for column_index, cell_data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_index, column_index, QTableWidgetItem(str(cell_data))
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    app.exec_()
