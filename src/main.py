from textnode import TextNode, TextType

def main():

    node1 = TextNode("text test text", TextType.LINK, "https://example.com")
    print(node1)

main()