from textnode import TextNode, TextType


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
    current_text = ""
    for node in old_nodes:
        if node.text == delimiter:
            if current_text:
                new_nodes.append(TextNode(current_text, text_type))
                current_text = ""
        else:
            current_text += node.text
    if current_text:
        new_nodes.append(TextNode(current_text, text_type))
    
    if len(new_nodes) == 1 and new_nodes[0].text == "":
        raise ValueError(f"Invalid Markdown syntax: '{delimiter}' delimiter found without content.")
    
    return new_nodes
        
        
        
        