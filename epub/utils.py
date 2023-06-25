from models.epub.metadata import EpubDirection


def create_vertical_writing_style(direction: EpubDirection):
    direction_value = "lr" if direction == EpubDirection.LTR else "rl"

    return f"""
        body {{
        writing-mode: vertical-{direction_value};
        -webkit-writing-mode: vertical-{direction_value};
        -epub-writing-mode: vertical-{direction_value};
        -epub-word-break: normal;
        word-break: normal;
        -epub-line-break: strict;
        line-break: strict;
    }}"""
