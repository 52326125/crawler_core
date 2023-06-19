from time import sleep
from typing import Callable


def retry(func: Callable):
    def wrapper(*args, **kwargs):
        retry_times = 0
        while retry_times < 3:
            try:
                result = func(*args, **kwargs)
                return result
            except:
                retry_times += 1
                print("failed")
                sleep(0.5)

    return wrapper
