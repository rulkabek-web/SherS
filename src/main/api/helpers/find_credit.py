from typing import Any
from src.main.api.models.credit_history_response_model import Credits

def find_credit(
    credits: list[Credits],
    **expected_fields: Any,
) -> Credits:
    for credit in credits:
        if all(
            getattr(credit, field_name) == expected_value
            for field_name, expected_value in expected_fields.items()
        ):
            return credit

    raise AssertionError(
        f"Кредит с параметрами {expected_fields} не найден. "
        f"Полученные кредиты: {credits}"
    )