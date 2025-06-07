from textnode import TextNode, TextType
from copystatic import copy_static_to_public
from generatepage import generate_pages_recursive
import sys
                
dir_path_static = "./static"


from_path_content = "./content"
template_path = "./template.html"
dest_path = "./docs"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"




def main():
    copy_static_to_public(dir_path_static, dest_path)
    generate_pages_recursive(from_path_content, template_path, dest_path, basepath)
    
    

main()