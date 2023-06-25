from models.converter.opencc import OpenCCModel
from opencc import OpenCC


def convert_opencc(content: str, model: OpenCCModel) -> str:
    opencc = OpenCC(model)
    return opencc.convert(content)
