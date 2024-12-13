from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from utils.form_managers import FormManager
from models.window_configs import UpdateDialogConfig
from models.data_models import PersonData
from utils.enums import FieldTypes, FieldLabels
from database_config import DatabaseManager
import logging


class UpdateDialog(QDialog):
    """Диалог обновления записи"""

    def __init__(self, db_manager: DatabaseManager, current_data: list, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.current_data = current_data
        self.config = UpdateDialogConfig()
        self.form_manager = FormManager(self.config)
        self.setup_ui()
        self.load_reference_data()
        self.fill_current_data()

    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle(self.config.title)
        self.resize(self.config.width, self.config.height)

        # Создание меток "Старые значения" и "Новые значения"
        self.create_headers()

        # Создание полей формы
        self.create_form_fields()

        # Создание кнопок
        self.create_buttons()

        # Подключение обработчиков
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def create_headers(self):
        """Создание заголовков для старых и новых значений"""
        self.old_values_label = self.form_manager.create_label(
            self, "Текущие значения",
            QtCore.QRect(180, 10, 200, 30),
            font_size=11
        )
        self.new_values_label = self.form_manager.create_label(
            self, "Новые значения",
            QtCore.QRect(370, 10, 200, 30),
            font_size=11
        )

    def fill_current_data(self):
        """Заполнение текущих значений"""
        for i, field in enumerate(self.fields):
            if i < len(self.current_data):
                old_widget = self.form_manager.widgets[f"{field.name}_old"]
                if field.field_type == FieldTypes.COMBO:
                    index = old_widget.findText(self.current_data[i])
                    old_widget.setCurrentIndex(index if index >= 0 else 0)
                else:
                    old_widget.setText(self.current_data[i])

    def accept(self):
        """Обработка принятия диалога"""
        try:
            old_data = self.collect_form_data("old")
            new_data = self.collect_form_data("new")

            if self.validate_changes(old_data, new_data):
                self.db.update_record(old_data, new_data)
                super().accept()
            else:
                self.show_error("Нет изменений для сохранения")
        except Exception as e:
            logging.error(f"Error updating record: {e}")
            self.show_error("Ошибка обновления записи")

    def validate_changes(self, old_data: PersonData, new_data: PersonData) -> bool:
        """Проверка наличия изменений"""
        return any(
            getattr(old_data, field) != getattr(new_data, field)
            for field in vars(old_data)
        )

    def show_error(self, message: str):
        """Отображение сообщения об ошибке"""
        QMessageBox.critical(self, "Ошибка", message)