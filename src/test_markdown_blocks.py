import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

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



if __name__ == "__main__":
    unittest.main()