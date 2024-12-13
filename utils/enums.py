from enum import Enum

class FieldTypes(Enum):
    """Типы полей ввода"""
    COMBO = "comboBox"
    LINE = "lineEdit"

class FieldLabels(Enum):
    """Метки полей"""
    FAM = "Фамилия"
    NAME = "Имя"
    SECOND_NAME = "Отчество"
    STREET = "Улица"
    BUILDING = "Дом"
    BUILDING_KORP = "Корпус"
    APARTMENT = "Квартира"
    PHONE = "Телефон"

class Operations(Enum):
    """Операции с базой данных"""
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    DEFAULT = "DEFAULT"

class TableColumns(Enum):
    """Колонки основной таблицы"""
    SURNAME = ("fam", "Фамилия", 0)
    NAME = ("names", "Имя", 1)
    PATRONYMIC = ("second_name", "Отчество", 2)
    STREET = ("street", "Улица", 3)
    HOUSE = ("bldng", "Дом", 4)
    BUILDING = ("bldng_k", "Корпус", 5)
    APARTMENT = ("appr", "Квартира", 6)
    PHONE = ("telef", "Телефон", 7)

    def __init__(self, db_field: str, title: str, index: int):
        self.db_field = db_field
        self.title = title
        self.index = index