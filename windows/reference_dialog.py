from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from utils.form_managers import FormManager
from models.window_configs import ReferenceDialogConfig
from utils.enums import FieldTypes
from database_config import DatabaseManager
import logging


class ReferenceDialog(QDialog):
    """Диалог для работы со справочниками"""

    def __init__(self, db_manager: DatabaseManager, ref_type: str, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.ref_type = ref_type
        self.config = ReferenceDialogConfig()
        self.form_manager = FormManager(self.config)
        self.setup_ui()
        self.load_reference_data()

    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle(f"Справочник - {self.ref_type}")
        self.resize(self.config.width, self.config.height)

        # Создание элементов интерфейса
        self.create_widgets()
        self.create_buttons()
        self.setup_connections()

    def create_widgets(self):
        """Создание элементов формы"""
        # Метка и комбобокс для выбора существующего значения
        self.where_label = self.form_manager.create_label(
            self, "Существующее значение",
            QtCore.QRect(20, 10, 281, 25)
        )

        self.where_combo = self.form_manager.create_input_field(
            self, FieldTypes.COMBO, "where_combo",
            QtCore.QRect(20, 40, 281, 25)
        )

        # Метка и поле ввода для нового значения
        self.new_value_label = self.form_manager.create_label(
            self, "Новое значение",
            QtCore.QRect(20, 70, 281, 25)
        )

        self.new_value_edit = self.form_manager.create_input_field(
            self, FieldTypes.LINE, "new_value",
            QtCore.QRect(20, 100, 281, 25)
        )

    def create_buttons(self):
        """Создание кнопок"""
        button_width = 90
        button_height = 25
        spacing = 10
        total_width = (button_width * 3) + (spacing * 2)
        start_x = (self.config.width - total_width) // 2
        y = self.config.height - button_height - 20

        # Кнопки операций
        self.update_button = self.form_manager.create_button(
            self, "Обновить",
            QtCore.QRect(start_x, y, button_width, button_height)
        )

        self.delete_button = self.form_manager.create_button(
            self, "Удалить",
            QtCore.QRect(start_x + button_width + spacing, y, button_width, button_height)
        )

        self.insert_button = self.form_manager.create_button(
            self, "Добавить",
            QtCore.QRect(start_x + (button_width + spacing) * 2, y, button_width, button_height)
        )

    def setup_connections(self):
        """Настройка обработчиков событий"""
        self.update_button.clicked.connect(self.update_reference)
        self.delete_button.clicked.connect(self.delete_reference)
        self.insert_button.clicked.connect(self.insert_reference)

    def load_reference_data(self):
        """Загрузка данных справочника"""
        try:
            data = self.db.get_reference_data(self.ref_type)
            self.where_combo.clear()
            self.where_combo.addItems([item[1] for item in data])
        except Exception as e:
            logging.error(f"Error loading reference data: {e}")
            self.show_error("Ошибка загрузки данных справочника")

    def update_reference(self):
        """Обновление значения в справочнике"""
        try:
            old_value = self.where_combo.currentText()
            new_value = self.new_value_edit.text().strip()

            if not old_value or not new_value:
                self.show_error("Выберите значение для обновления и введите новое значение")
                return

            if self.confirm_operation("обновить"):
                self.db.update_reference(self.ref_type, old_value, new_value)
                self.load_reference_data()
                self.new_value_edit.clear()

        except Exception as e:
            logging.error(f"Error updating reference: {e}")
            self.show_error("Ошибка обновления значения")

    def delete_reference(self):
        """Удаление значения из справочника"""
        try:
            value = self.where_combo.currentText()
            if not value:
                self.show_error("Выберите значение для удаления")
                return

            if self.confirm_operation("удалить"):
                self.db.delete_reference(self.ref_type, value)
                self.load_reference_data()

        except Exception as e:
            logging.error(f"Error deleting reference: {e}")
            self.show_error("Ошибка удаления значения")

    def insert_reference(self):
        """Добавление нового значения в справочник"""
        try:
            value = self.new_value_edit.text().strip()
            if not value:
                self.show_error("Введите новое значение")
                return

            self.db.insert_reference(self.ref_type, value)
            self.load_reference_data()
            self.new_value_edit.clear()

        except Exception as e:
            logging.error(f"Error inserting reference: {e}")
            self.show_error("Ошибка добавления значения")

    def confirm_operation(self, operation: str) -> bool:
        """Подтверждение операции"""
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            f'Вы действительно хотите {operation} это значение?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def show_error(self, message: str):
        """Отображение сообщения об ошибке"""
        QMessageBox.critical(self, "Ошибка", message)