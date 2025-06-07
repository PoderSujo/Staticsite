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

def generate_page(from_path, template_path, dest_path, basepath):
    """
    Generate a page from a Markdown file using a template.

    Args:
        from_path (str): The path to the Markdown file.
        template_path (str): The path to the HTML template file.\
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
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    template_content = template_content.replace('src="/', 'src="' + basepath)
    template_content = template_content.replace('href="/', 'href="' + basepath)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    print(f"Page generated at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """
    Recursively generate pages from Markdown files in a directory.

    Args:
        dir_path_content (str): The path to the directory containing Markdown files.
        template_path (str): The path to the HTML template file.
        dest_dir_path (str): The destination directory for the generated HTML files.
    
    Returns:
        None
    """
    dir_path_content = pathlib.Path(dir_path_content)
    for item in dir_path_content.iterdir():
        if item.is_dir():
            next_dest_dir_path = pathlib.Path(dest_dir_path) / item.relative_to(dir_path_content)
            generate_pages_recursive(item, template_path, next_dest_dir_path, basepath)
        elif item.suffix == '.md':
            dest_path = pathlib.Path(dest_dir_path) / item.with_suffix('.html').relative_to(dir_path_content)
            generate_page(item, template_path, dest_path, basepath)
    