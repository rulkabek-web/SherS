import uuid
import random
from typing import Any, get_type_hints, get_origin, Annotated, get_args
import rstr
from src.main.api.models.base_model import BaseModel

from src.main.api.generators.creation_rule import CreationRule


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type, **overrides) -> BaseModel:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():

            # Если поле передано вручную
            if field_name in overrides:
                override_value = overrides[field_name]

                if get_origin(override_value) is Annotated:
                    actual_type, rule = RandomModelGenerator._extract_rule(override_value)

                    if rule is not None:
                        init_data[field_name] = RandomModelGenerator._generate_by_rule(
                            field_type=actual_type,
                            rule=rule
                        )
                    else:
                        init_data[field_name] = RandomModelGenerator.generate_value(actual_type)

                else:
                    init_data[field_name] = override_value

                continue


            actual_type, rule = RandomModelGenerator._extract_rule(annotated_type)

            if rule is not None:
                value = RandomModelGenerator._generate_by_rule(
                    field_type=actual_type,
                    rule=rule
                )
            else:
                value = RandomModelGenerator.generate_value(actual_type)

            init_data[field_name] = value

        return cls(**init_data)

    @staticmethod
    def _extract_rule(annotated_type):
        actual_type = annotated_type
        rule = None

        if get_origin(annotated_type) is Annotated:
            actual_type, *annotations = get_args(annotated_type)

            for annotation in annotations:
                if isinstance(annotation, CreationRule):
                    rule = annotation
                    break

        return actual_type, rule

    @staticmethod
    def _generate_by_rule(field_type: type, rule: CreationRule) -> Any:
        if rule.regex is not None:
            return RandomModelGenerator._generate_from_regex(rule.regex, field_type)

        if field_type is int:
            min_value = rule.min_int if rule.min_int is not None else 1
            max_value = rule.max_int if rule.max_int is not None else 9999

            return random.randint(min_value, max_value)

        if field_type is float:
            min_value = rule.min_float if rule.min_float is not None else 0
            max_value = rule.max_float if rule.max_float is not None else 100

            return round(random.uniform(min_value, max_value), 2)

        # Если rule есть, но он не подходит под тип поля
        return RandomModelGenerator.generate_value(field_type)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type):
        generated = rstr.xeger(regex)

        if field_type is int:
            return int(generated)

        if field_type is float:
            return float(generated)

        return generated

    @staticmethod
    def generate_value(
        field_type: type,
        min_int: int = 1,
        max_int: int = 9999,
        min_float: float = 0,
        max_float: float = 100
    ) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]

        elif field_type is int:
            return random.randint(min_int, max_int)

        elif field_type is float:
            return round(random.uniform(min_float, max_float), 2)

        elif field_type is bool:
            return random.choice([True, False])

        elif field_type is list:
            return [str(uuid.uuid4())[:5]]

        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)

        return None