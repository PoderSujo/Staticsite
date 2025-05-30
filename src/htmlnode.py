

class HTMLNode:

    def __init__(self, tag = None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html() method is not implemented for HTMLNode. Please implement it in a subclass.")
    
    def props_to_html(self):

        attributes = ""
        if self.props is None:
            return attributes
        for i in self.props:
            attributes += f' {i}="{self.props[i]}"'

        return attributes
    def __repr__(self):
        #return f"HTMLnode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
        

class LeafNode(HTMLNode):
    """
    Class representing a leaf node in the HTML tree.
    A leaf node is a node that does not have any children.
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        