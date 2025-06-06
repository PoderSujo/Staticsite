import os
import pathlib
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    """
    Extract the title from a Markdown string.

    Args:
        markdown (str): The Markdown string to extract the title from.
    
    Returns:
        str: The extracted title, or an empty string if no title is found.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()  # Return the title without the '# ' prefix
    raise Exception("No title'# header'")   #raise an exception if no title is found

def generate_page(from_path, template_path, dest_path):
    """
    Generate a page from a Markdown file using a template.

    Args:
        from_path (str): The path to the Markdown file.
        template_path (str): The path to the HTML template file.
        dest_path (str): The destination path for the generated HTML file.
    
    Returns:
        None
    """

    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    title = extract_title(markdown_content)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    print(f"Page generated at {dest_path}")
