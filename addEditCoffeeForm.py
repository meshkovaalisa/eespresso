import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox


class AddEditCoffeeForm(QDialog):
    def __init__(self, record_id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.record_id = record_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавление/Редактирование кофе')
        self.saveButton.clicked.connect(self.save_record)
        self.cancelButton.clicked.connect(self.reject)

        if self.record_id:
            self.setWindowTitle('Редактирование записи')
            self.load_record()
        else:
            self.setWindowTitle('Добавление записи')

    def load_record(self):
        try:
            conn = sqlite3.connect('cofee.db')
            cur = conn.cursor()
            cur.execute("SELECT name, roast, been, taste, price, size FROM names_cofee WHERE id = ?",
                        (self.record_id,))
            record = cur.fetchone()
            conn.close()

            if record:
                self.nameEdit.setText(record[0])
                self.roastSpin.setValue(record[1])

                index = self.typeCombo.findText(record[2])
                if index >= 0:
                    self.typeCombo.setCurrentIndex(index)

                self.tasteEdit.setText(record[3] if record[3] else '')
                self.priceSpin.setValue(record[4])
                self.sizeSpin.setValue(record[5])
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки записи: {str(e)}')

    def save_record(self):
        name = self.nameEdit.text().strip()
        if not name:
            QMessageBox.warning(self, 'Предупреждение', 'Введите название кофе')
            return

        taste = self.tasteEdit.toPlainText().strip()
        roast = self.roastSpin.value()
        been = self.typeCombo.currentText()
        price = self.priceSpin.value()
        size = self.sizeSpin.value()

        if price <= 0:
            QMessageBox.warning(self, 'Предупреждение', 'Цена должна быть больше 0')
            return

        if size <= 0:
            QMessageBox.warning(self, 'Предупреждение', 'Объем упаковки должен быть больше 0')
            return

        try:
            conn = sqlite3.connect('cofee.db')
            cur = conn.cursor()

            if self.record_id:
                cur.execute("""
                    UPDATE names_cofee 
                    SET name=?, roast=?, been=?, taste=?, price=?, size=?
                    WHERE id=?
                """, (name, roast, been, taste, price, size, self.record_id))
            else:
                cur.execute("""
                    INSERT INTO names_cofee (name, roast, been, taste, price, size)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, roast, been, taste, price, size))

            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка сохранения: {str(e)}')