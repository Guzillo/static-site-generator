import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
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

    def test_markdown_to_blocks_with_images_and_links(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

This is a link [linkhere](https://example.com) and a goddamn picture ![somepic](https://pinterest.com)
This is a link [another](https://example.com) and a goddamn picture ![anotherpic](https://pinterest.com)
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "This is a link [linkhere](https://example.com) and a goddamn picture ![somepic](https://pinterest.com)\nThis is a link [another](https://example.com) and a goddamn picture ![anotherpic](https://pinterest.com)",
            ],
        )

    def test_block_to_block_type_heading_one_symbol(self):
        self.assertEqual(block_to_block_type("# test"), BlockType.HEADING)

    def test_block_to_block_type_heading_no_space(self):
        self.assertEqual(block_to_block_type("#test"), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_space_at_start(self):
        self.assertEqual(block_to_block_type(" # test"), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_6_symbols(self):
        self.assertEqual(block_to_block_type("###### test"), BlockType.HEADING)

    def test_block_to_block_type_heading_7_symbols(self):
        self.assertEqual(block_to_block_type("####### test"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        self.assertEqual(block_to_block_type("```\nhey\n```"), BlockType.CODE)

    def test_block_to_block_type_code_block_doesnt_end_with_backticks(self):
        self.assertEqual(block_to_block_type("```hey``` "), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type(">one\n>two"), BlockType.QUOTE)

    def test_block_to_block_type_quote_one_line_doesnt_start_with_symbol(self):
        self.assertEqual(block_to_block_type(">one\ntwo\n>three"), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- one\n- two"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_one_line_wrong(self):
        self.assertEqual(
            block_to_block_type("- one\n two\n- three"), BlockType.PARAGRAPH
        )

    def test_block_to_block_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. hey\n2. hey\n3. hey"), BlockType.ORDERED_LIST
        )

    def test_block_to_block_ordered_list_wrong_number(self):
        self.assertEqual(
            block_to_block_type("1. hey\n3. hey\n4. hey"), BlockType.PARAGRAPH
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
