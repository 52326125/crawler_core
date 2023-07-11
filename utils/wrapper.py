from models.htmlParser import HTMLParser
from utils.common import get_int_input


def select_parser(parser_key: str = "parser"):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            default_parser = HTMLParser.DEFAULT
            current_parser = default_parser
            parser_length = len(HTMLParser)
            while True:
                kwargs[parser_key] = current_parser
                result = fn(*args, **kwargs)
                parser_str = ""
                for index, value in enumerate(HTMLParser):
                    parser_str += f"{index})更改編碼器：{value}\n"
                action = get_int_input(
                    description=f"請確認是否正確獲取書本資料，如果有誤，請輸入對應代號切換編碼器，當前編碼器：{current_parser}\n{parser_str}{parser_length})下一步",
                    min=0,
                    max=parser_length,
                )
                if action == parser_length:
                    return result
                else:
                    current_parser = list(HTMLParser)[action]

        return wrapper

    return decorator
