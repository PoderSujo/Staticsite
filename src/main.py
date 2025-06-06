from textnode import TextNode, TextType
from copystatic import copy_static_to_public
from generatepage import generate_page
                
dir_path_static = "./static"
dir_path_public = "./public"

def main():
    copy_static_to_public(dir_path_static, dir_path_public)
    generate_page(
        from_path="./content/index.md",
        template_path="./template.html",
        dest_path="./public/index.html"
    )
    

main()