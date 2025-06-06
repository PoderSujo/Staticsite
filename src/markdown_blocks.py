from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    """
    Enum representing different types of Markdown blocks.
    """
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"  

def block_to_block_type(block):
    """
    Convert a Markdown block string to its corresponding BlockType.

    Args:
        block (str): The Markdown block string.
    Returns:
        BlockType: The type of the block.
    """
    lines = block.split("\n")

    if re.match(r'^\s*#{1,6}\s', block):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") or line == "" for line in lines):
        return BlockType.QUOTE
    elif all(re.match(r'^\s*-\s', line) for line in lines):
        return BlockType.U_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.O_LIST
  
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    """
    Convert a Markdown string into a list of blocks.

    Args:
        markdown (str): The Markdown string to convert.
    Returns:
        list: A list of blocks.
    """
    list_of_blocks = []
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        list_of_blocks.append(line)
    return list_of_blocks

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = block.count("#")
            content = block[level:].strip()
            html_nodes.append(ParentNode(f"h{level}", list(map(text_node_to_html_node, text_to_textnodes(content)))))
        elif block_type == BlockType.PARAGRAPH:
            html_nodes.append(ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(block)))))
        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.split("\n")[1:-1])
            html_nodes.append(ParentNode("pre", [LeafNode("code", code_content)]))
        elif block_type == BlockType.QUOTE:
            quote_content = "\n".join(line[2:] for line in block.split("\n"))
            html_nodes.append(ParentNode("blockquote",list(map(text_node_to_html_node, text_to_textnodes(quote_content)))))
        elif block_type == BlockType.U_LIST:
            items = [ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(item[2:])))) for item in block.split("\n") if item.startswith("-")]
            html_nodes.append(ParentNode("ul", items))
        elif block_type == BlockType.O_LIST:
            items = [ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(item[3:])))) for item in block.split("\n") if re.match(r'^\d+\.\s', item)]
            html_nodes.append(ParentNode("ol", items))
        else:
            html_nodes.append(ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(block)))))
    return ParentNode("div", html_nodes)
