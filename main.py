import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from addEditCoffeeForm import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()
        self.load_data()

    def initUI(self):
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        self.addButton = QPushButton('Добавить')
        self.editButton = QPushButton('Изменить')

        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.editButton)
        button_layout.addStretch()

        layout = QVBoxLayout(self.centralWidget())
        self.tableWidget.setParent(None)
        layout.addWidget(self.tableWidget)
        layout.addWidget(button_widget)

        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)

    def load_data(self):
        conn = sqlite3.connect('cofee.db')
        cur = conn.cursor()
        data = cur.execute("""
            SELECT id, name, roast, been, 
                   taste, price, size 
            FROM names_cofee
        """).fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Название', 'Степень обжарки', 'Тип',
            'Описание вкуса', 'Цена', 'Объем упаковки'
        ])

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

        self.tableWidget.resizeColumnsToContents()
        conn.close()

    def add_record(self):
        dialog = AddEditCoffeeForm()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def edit_record(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите запись для редактирования')
            return

        record_id = int(self.tableWidget.item(row, 0).text())
        dialog = AddEditCoffeeForm(record_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())
