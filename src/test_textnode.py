import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        expected_repr = "TextNode('This is a text node', 'bold', 'https://example.com')"
        self.assertEqual(repr(node), expected_repr)
    def test_text_type(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertEqual(node.text, "This is a text node")
        self.assertIsNone(node.url)
        


if __name__ == "__main__":
    unittest.main()