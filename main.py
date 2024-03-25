import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QDialog,
)
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_Dialog
import sqlite3


class EditCoffeeForm(QDialog, Ui_Dialog):
    def __init__(self, coffee_id=None):
        super(EditCoffeeForm, self).__init__()
        self.setupUi(self)
        self.coffee_id = coffee_id
        self.initUI()

    def initUI(self):
        self.saveButton.clicked.connect(self.save_coffee)

    def save_coffee(self):
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        type_ = self.typeComboBox.currentText()
        description = self.descriptionEdit.toPlainText()
        price = self.priceEdit.value()
        volume = self.volumeEdit.value()

        connection = sqlite3.connect("data/coffee.sqlite")
        cursor = connection.cursor()

        if self.coffee_id is None:  # Добавление новой записи
            cursor.execute(
                """INSERT INTO coffee (name, roast_degree, ground_or_beans, flavor_description, price, volume)
                              VALUES (?, ?, ?, ?, ?, ?)""",
                (name, roast, type_, description, price, volume),
            )
        else:  # Редактирование существующей записи
            cursor.execute(
                """UPDATE coffee SET name=?, roast_degree=?, ground_or_beans=?, flavor_description=?, price=?, volume=?
                              WHERE id=?""",
                (
                    name,
                    roast,
                    type_,
                    description,
                    price,
                    volume,
                    int(self.coffee_id),
                ),
            )

        connection.commit()
        connection.close()
        self.accept()


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        self.setupUi(self)
        self.load_coffee_data()
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_coffee_data(self):
        connection = sqlite3.connect("data/coffee.sqlite")
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

    def add_coffee(self):
        editor = EditCoffeeForm()
        if editor.exec_():
            self.load_coffee_data()

    def edit_coffee(self):
        selected = self.tableWidget.currentRow()
        if selected >= 0:
            coffee_id = self.tableWidget.item(selected, 0).text()
            editor = EditCoffeeForm(coffee_id=coffee_id)
            if editor.exec_():
                self.load_coffee_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    app.exec_()
