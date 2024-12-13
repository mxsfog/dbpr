from dataclasses import dataclass
from typing import Optional
from utils.enums import FieldTypes

@dataclass
class FormField:
    """Модель поля формы"""
    name: str
    label_text: str
    field_type: FieldTypes
    x: int
    y: int
    width: int
    height: int
    required: bool = False
    default_value: Optional[str] = None

@dataclass
class PersonData:
    """Модель данных о человеке"""
    fam_id: Optional[int]
    name_id: Optional[int]
    second_name_id: Optional[int]
    street_id: Optional[int]
    building: Optional[str]
    building_korp: Optional[str]
    apartment: Optional[str]
    phone: Optional[str]

@dataclass
class QueryResult:
    """Модель результата запроса"""
    success: bool
    data: Optional[list] = None
    error: Optional[str] = None