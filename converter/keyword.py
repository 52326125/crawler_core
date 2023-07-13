from converter.models.converter import KeywordDict


def convert_keyword(content: str, dicts: list[KeywordDict]) -> str:
    for dict in dicts:
        content.replace(dict["origin"], dict["converted"])

    return content
