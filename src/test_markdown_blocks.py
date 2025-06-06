import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_paragraph(self):
        self.assertEqual(markdown_to_blocks("Hello, world!"), ["Hello, world!"])

    def test_multiple_paragraphs(self):
        markdown = "First paragraph.\n\nSecond paragraph."
        expected = ["First paragraph.", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_newlines(self):
        markdown = "\n\nParagraph with leading and trailing newlines.\n\n"
        expected = ["Paragraph with leading and trailing newlines."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_newlines_between_paragraphs(self):
        markdown = "First paragraph.\n\n\nSecond paragraph."
        expected = ["First paragraph.", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote."), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.U_LIST)
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.O_LIST)
    def test_block_to_block_type_invalid(self):
        self.assertEqual(block_to_block_type("Invalid block type"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a\nblockquote block</p></blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )




if __name__ == "__main__":
    unittest.main()