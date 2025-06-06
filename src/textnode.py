from enum import Enum
from htmlnode import LeafNode, HTMLNode


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

def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image text node must have a URL.")
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    if text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link text node must have a URL.")
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    raise ValueError(f"Unknown text type: {text_node.text_type}")
