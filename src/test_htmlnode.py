import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):


    def test_repr(self):
        node = HTMLNode("div", "This is a div", props= {"class": "test"})
        expected_repr = "HTMLNode(tag='div', value='This is a div', children=None, props={'class': 'test'})"
        self.assertEqual(repr(node), expected_repr)
    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div",props= {"class": "test", "id": "unique"})
        expected_props = ' class="test" id="unique"'
        self.assertEqual(node.props_to_html(), expected_props)
    def test_props_to_html_empty(self):
        node = HTMLNode("div", "This is a div")
        expected_props = ""
        self.assertEqual(node.props_to_html(), expected_props)
    def test_to_html_not_implemented(self):
        node = HTMLNode("div", "This is a div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html(self):
        node = LeafNode("p", "This is a paragraph", props={"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">This is a paragraph</p>')
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", props={"class": "text"})
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_to_html_tag2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    
if __name__ == "__main__":
    unittest.main()