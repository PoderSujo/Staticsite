from enum import Enum

class TextType(Enum):
    """
    Enum for text node types.
    """
    TEXT = "text"
    CODE = "code"
    BOLD = "bold"
    ITALIC = "italic"
    IMAGE = "image"
    LINK = "link"

class TextNode:
    """
    Class representing a text node with a type and content.
    """
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"