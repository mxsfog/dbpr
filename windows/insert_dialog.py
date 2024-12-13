from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from utils.form_managers import FormManager
from models.window_configs import InsertDialogConfig
from models.data_models import FormField, PersonData
from utils.enums import FieldTypes, FieldLabels
from database_config import DatabaseManager
import logging


class InsertDialog(QDialog):
    """Диалог добавления новой записи"""

    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.config = InsertDialogConfig()
        self.form_manager = FormManager(self.config)
        self.setup_ui()
        self.load_reference_data()

    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle(self.config.title)
        self.resize(self.config.width, self.config.height)

        # Создание полей формы
        self.create_form_fields()

        # Создание кнопок
        self.create_buttons()

        # Подключение обработчиков
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        for button in self.ref_buttons:
            button.clicked.connect(self.open_reference_dialog)

    def create_form_fields(self):
        """Создание полей формы"""
        self.fields = [
            FormField("fam", FieldLabels.FAM.value, FieldTypes.COMBO, 40, 30, 200, 25),
            FormField("name", FieldLabels.NAME.value, FieldTypes.COMBO, 40, 70, 200, 25),
            FormField("second_name", FieldLabels.SECOND_NAME.value, FieldTypes.COMBO, 40, 110, 200, 25),
            FormField("street", FieldLabels.STREET.value, FieldTypes.COMBO, 40, 150, 200, 25),
            FormField("building", FieldLabels.BUILDING.value, FieldTypes.LINE, 40, 190, 200, 25),
            FormField("building_korp", FieldLabels.BUILDING_KORP.value, FieldTypes.LINE, 40, 230, 200, 25),
            FormField("apartment", FieldLabels.APARTMENT.value, FieldTypes.LINE, 40, 270, 200, 25),
            FormField("phone", FieldLabels.PHONE.value, FieldTypes.LINE, 40, 310, 200, 25),
        ]

        for field in self.fields:
            self.form_manager.create_input_field(
                self, field.field_type, field.name,
                QtCore.QRect(field.x, field.y, field.width, field.height)
            )

    def load_reference_data(self):
        """Загрузка данных для справочников"""
        try:
            for field in self.fields:
                if field.field_type == FieldTypes.COMBO:
                    data = self.db.get_reference_data(field.name)
                    combo = self.form_manager.widgets[field.name]
                    combo.addItems([""] + [str(item[1]) for item in data])
        except Exception as e:
            logging.error(f"Error loading reference data: {e}")
            self.show_error("Ошибка загрузки справочных данных")

    def accept(self):
        """Обработка принятия диалога"""
        try:
            data = self.collect_form_data()
            if self.validate_data(data):
                self.db.insert_record(data)
                super().accept()
            else:
                self.show_error("Заполните все обязательные поля")
        except Exception as e:
            logging.error(f"Error inserting record: {e}")
            self.show_error("Ошибка добавления записи")

    def collect_form_data(self) -> PersonData:
        """Сбор данных с формы"""
        data = {}
        for field in self.fields:
            widget = self.form_manager.widgets[field.name]
            if field.field_type == FieldTypes.COMBO:
                data[field.name] = widget.currentText()
            else:
                data[field.name] = widget.text()
        return PersonData(**data)

    def validate_data(self, data: PersonData) -> bool:
        """Валидация данных формы"""
        required_fields = ['fam', 'name', 'street', 'building']
        return all(getattr(data, field) for field in required_fields)

    def show_error(self, message: str):
        """Отображение сообщения об ошибке"""
        QMessageBox.critical(self, "Ошибка", message)