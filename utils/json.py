import json
from typing import Type, TypeVar
from pydantic import parse_obj_as


T = TypeVar("T")


def str_2_pydantic(json_str: str, Model: Type[T]) -> T:
    json_obj = json.loads(json_str)
    return json_2_pydantic(json_obj, Model)


def json_2_pydantic(json_obj: dict, Model: Type[T]) -> T:
    instance = parse_obj_as(Model, json_obj)
    return instance
