from enum import Enum

class TextNode(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    def __init__(self):
        super().__init__()
    