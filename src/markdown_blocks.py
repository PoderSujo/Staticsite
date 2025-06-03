from enum import Enum
import re

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
    elif lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in lines):
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


