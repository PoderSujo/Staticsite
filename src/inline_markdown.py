from textnode import TextNode, TextType
import re

def has_valid_markdown_syntax(text):
    """
    Check if the given text has valid Markdown syntax.
    
    Args:
        text (str): The text to check for valid Markdown syntax.
        
    Returns:
        bool: True if the text has valid Markdown syntax, False otherwise.
    """
    bold = re.search(r'\*\*([^\n]+?)\*\*', text)
    italic = re.search(r'_([^\n]+?)_', text)
    code = re.search(r'`([^\n]+?)`', text)
    if bold or italic or code:
        return True
    return False 




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split a list of TextNodes into multiple TextNodes based on a delimiter.
    If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.
    
    Args:
        old_nodes (list): List of TextNode objects to be split.
        delimiter (str): The delimiter string to split the nodes.
        text_type (TextType): The type of the new TextNode created from the split.
        
    Returns:
        list: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if not has_valid_markdown_syntax(node.text) and delimiter in node.text:
            raise ValueError(f"Invalid Markdown syntax in node: {node.text}")
        parts = node.text.split(delimiter)
        inside_nodes = []
        for i in range(len(parts)):
            if parts[i] == '':
                # Skip empty parts
                continue            
            if i % 2 == 0:
                # Even index parts are plain text, odd index parts are wrapped in the delimiter
                inside_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                # Odd index parts are wrapped in the delimiter
                inside_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(inside_nodes)
    return new_nodes


def extract_markdown_images(text):
    """
    Extract Markdown image links from the given text.
    
    Args:
        text (str): The text to extract image links from.
        
    Returns:
        list: A list of tuples containing the image link and alt text.
    """
    image_pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return image_pattern.findall(text)
def extract_markdown_links(text):
    """
    Extract Markdown links from the given text.
    
    Args:
        text (str): The text to extract links from.
        
    Returns:
        list: A list of tuples containing the link text and URL.
    """
    link_pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return link_pattern.findall(text)
        
              
def split_nodes_image(old_nodes):
    """
    Split a list of TextNodes into multiple TextNodes based on Markdown image syntax.
    
    Args:
        old_nodes (list): List of TextNode objects to be split.
        
    Returns:
        list: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        parts = re.split(r'!\[[^\[\]]*\]\([^\(\)]*\)', node.text)
        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(images):
                alt_text, url = images[i]
                new_nodes.append(TextNode(f"{alt_text}", TextType.IMAGE, url))
    return new_nodes
        
        
def split_nodes_link(old_nodes):
    """
    Split a list of TextNodes into multiple TextNodes based on Markdown link syntax.
    
    Args:
        old_nodes (list): List of TextNode objects to be split.
        
    Returns:
        list: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue        
        links = extract_markdown_links(node.text)

        # If no links are found, just append the original node
        if not links:
            new_nodes.append(node)
            continue
        parts = re.split(r'\[[^\[\]]*\]\([^\(\)]*\)', node.text)
        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(links):
                link_text, url = links[i]
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
    return new_nodes


def text_to_textnodes(text):
    """
    Convert a text string to a list of TextNode objects.
    
    Args:
        text (str): The text to convert.
        
    Returns:
        list: A list of TextNode objects representing the text.
    """
    if not text:
        return []
    node = []
    node.append(TextNode(text, TextType.TEXT))
    first_transformation = split_nodes_link(split_nodes_image(node))
    second_transformation = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(first_transformation, '**', TextType.BOLD), '_', TextType.ITALIC), '`', TextType.CODE)
    return second_transformation