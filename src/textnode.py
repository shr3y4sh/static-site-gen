from enum import Enum


class TextType(Enum):
    TEXT = "plain_text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    CODE = "code_text"
    LINK = "link"
    IMAGE = "embedded_image"


class TextNode:
    def __init__(self, text, t_type, link=None):
        self.text = text
        self.text_type = t_type
        self.url = link

    def __eq__(self, other):
        return (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
