import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image, 
    split_nodes_link, 
    text_to_textnodes
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    
    def test_delim_bold(self):
        nodes = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )
       
    def test_delim_italic(self):
        nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter([nodes], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ]
        )
    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](http://example.com/image.png)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [("alt text", "http://example.com/image.png")]
        )
    def test_extract_markdown_links(self):
        text = "This is a link [example](http://example.com)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [("example", "http://example.com")]
        )
    def test_extract_markdown_links_with_nested(self):
        text = "This is a link [example](http://example.com) with [another](http://another.com)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            links,
            [("example", "http://example.com"), ("another", "http://another.com")]
        )
    def test_extract_markdown_links_and_images(self):
        text = "This is a link [example](http://example.com) and an image ![alt text](http://example.com/image.png)"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertListEqual(
            links,
            [("example", "http://example.com")]
        )
        self.assertListEqual(
            images,
            [("alt text", "http://example.com/image.png")]
        )
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_no_image(self):
        node = TextNode("This is text without an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text without an image", TextType.TEXT)],
            new_nodes,
        )
    def test_split_images_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.TEXT)], new_nodes)
    def test_split_images_and_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a link [example](http://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a link [example](http://example.com)", TextType.TEXT),
                
            ],
            new_nodes,
        )
    def test_split_images_nested_nodes(self):
        node = [TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a link [example](http://example.com)",
            TextType.TEXT,
        ),
            TextNode("This is another text node", TextType.TEXT),
            TextNode("And another ![image](https://i.imgur.com/another.png)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a link [example](http://example.com)", TextType.TEXT),
                TextNode("This is another text node", TextType.TEXT),
                TextNode("And another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/another.png"),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](http://example.com) and another [second link](http://example.com/second)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "http://example.com/second"),
            ],
            new_nodes,
        )
    def test_split_link_nested_nodes(self):
        node = [
            TextNode(
                "This is text with a [link](http://example.com) and another [second link](http://example.com/second)",
                TextType.TEXT,
            ),
            TextNode("This is another text node", TextType.TEXT),
            TextNode("And another [third link](http://example.com/third)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "http://example.com/second"),
                TextNode("This is another text node", TextType.TEXT),
                TextNode("And another ", TextType.TEXT),
                TextNode("third link", TextType.LINK, "http://example.com/third"),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is a **bold** and _italic_ text with a `code` block and an image ![alt text](http://example.com/image.png) and a link [example](http://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " text with a ")
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " block and an image ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "alt text")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "http://example.com/image.png")
        self.assertEqual(nodes[-1].text, "example")
        self.assertEqual(nodes[-1].text_type, TextType.LINK)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text with a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" block and an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "http://example.com/image.png"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("example", TextType.LINK, "http://example.com"),
            ],
            nodes,
        )




if __name__ == "__main__":
    unittest.main()