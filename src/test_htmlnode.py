import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        node = LeafNode(tag="p",value=None , props={"class": "text"})
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_to_html_tag2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_parent_to_html_no_tag_and_no_children(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_parent_to_html_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("span", "child2")
        child3 = LeafNode("span", "child3") 
        child4 = ParentNode("div", [LeafNode("span", "child4")])
        parent_node = ParentNode("div", [child1, child2, child3, child4])
        expected_html = "<div><span>child1</span><span>child2</span><span>child3</span><div><span>child4</span></div></div>"
        self.assertEqual(parent_node.to_html(), expected_html)
    
if __name__ == "__main__":
    unittest.main()