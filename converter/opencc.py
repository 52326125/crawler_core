from converter.models.opencc import OpenCCModel
from opencc import OpenCC


def convert_opencc(content: str, model: OpenCCModel | None) -> str:
    if model is None:
        return content
    opencc = OpenCC(model)
    return opencc.convert(content)
