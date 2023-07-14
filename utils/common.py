import os
import sys
from typing import Callable, List, Optional, TypeVar


T = TypeVar("T")
V = TypeVar("V")


def exec_with_description(fn: Callable[[V], T], description: str = "", **kwargs) -> T:
    if description:
        print(description + " 中...")

    result = fn(**kwargs)

    if description:
        print(description + " 成功")

    return result


def get_int_input(description: str, min: Optional[int], max: Optional[int]) -> int:
    while True:
        try:
            result = input(description)
            transferred_result = int(result)
            if (min is not None and transferred_result < min) or (
                max is not None and transferred_result > max
            ):
                raise ValueError("Out of giving range")
            return int(result)
        except ValueError:
            print("無效的輸入，請重新輸入")


def get_bool_input(description: str, acceptance_key: List[str]) -> bool:
    result = input(description)
    for key in acceptance_key:
        if result == key:
            return True
    return False


def get_real_path(file_path: str) -> str:
    app_path = ""
    if getattr(sys, "frozen", False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.getcwd()
    return os.path.join(app_path, file_path)
