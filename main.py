import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())