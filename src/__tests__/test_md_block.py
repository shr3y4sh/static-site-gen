import unittest
from md_to_block import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_single_paragraph(self):
        md = "This is a single paragraph with some text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with some text."])

    def test_multiple_paragraphs(self):
        md = """
First paragraph.

Second paragraph.

Third paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph.",
                "Second paragraph.",
                "Third paragraph.",
            ],
        )

    def test_paragraphs_with_blank_lines(self):
        md = """
First paragraph.


Second paragraph with extra blank lines.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph.",
                "Second paragraph with extra blank lines.",
            ],
        )

    def test_list_block(self):
        md = """
- Apple
- Banana
- Cherry
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- Apple\n- Banana\n- Cherry",
            ],
        )

    def test_numbered_list_block(self):
        md = """
1. First
2. Second
3. Third
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "1. First\n2. Second\n3. Third",
            ],
        )

    def test_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_input_with_only_whitespace(self):
        md = "   \n   \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_quoted_block(self):
        md = """
> This is a quoted block.
> It has multiple lines.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> This is a quoted block.\n> It has multiple lines.",
            ],
        )

    def test_mixed_content(self):
        md = (
            "\nIntro paragraph.\n\n"
            "- Item one\n- Item two\n\n"
            "> Blockquote line\n\n"
            "Another paragraph.\n\n"
            "``````\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Intro paragraph.",
                "- Item one\n- Item two",
                "> Blockquote line",
                "Another paragraph.",
                "``````",
            ],
        )

    def test_leading_and_trailing_blank_lines(self):
        md = """

First paragraph.

Second paragraph.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph.",
                "Second paragraph.",
            ],
        )

    def test_single_line_code_block(self):
        md = "``````"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["``````"])


if __name__ == "__main__":
    unittest.main()
