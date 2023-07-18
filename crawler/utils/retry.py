from time import sleep
from typing import Callable


def retry(func: Callable):
    def wrapper(*args, **kwargs):
        retry_times = 0
        while retry_times < 3:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as err:
                retry_times += 1
                print("failed")
                if retry_times == 3:
                    print("retry failed, reason:\n" + str(err))
                sleep(0.5)

    return wrapper
