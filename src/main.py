from textnode import TextNode, TextType
from copystatic import copy_static_to_public
                
dir_path_static = "./static"
dir_path_public = "./public"

def main():
    copy_static_to_public(dir_path_static, dir_path_public)

    

main()