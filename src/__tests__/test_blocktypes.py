import unittest

from block_parser import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    # PARAGRAPH TESTS
    def test_paragraph_simple(self):
        block = "This is a simple paragraph."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nof text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_inline_formatting(self):
        block = "This paragraph has **bold** and *italic* text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # HEADING TESTS
    def test_heading_h1(self):
        block = "# This is a heading 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h2(self):
        block = "## This is a heading 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a heading 6"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_with_space_required(self):
        block = "# Proper heading with space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_not_heading_no_space(self):
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_not_heading_hash_in_middle(self):
        block = "This # is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # CODE BLOCK TESTS
    def test_code_block_simple(self):
        block = "```print('Hello World')```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_with_language(self):
        block = """```
def hello():
    print('Hello')
    ```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_multiline(self):
        block = """```
for i in range(10):
    print(i)
    if i == 5:
        break
    ```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_empty(self):
        block = """```
```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_not_code_block_incomplete(self):
        block = """```print('incomplete code block'"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_code_block_with_content_and_language(self):
        block = """```
function test() {
    console.log('test');
}
    ```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_single_line(self):
        block = """```
echo 'hello'
    ```"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    # QUOTE TESTS
    def test_quote_single_line(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_multiline(self):
        block = "> This is a quote\n> with multiple lines\n> of text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    # def test_quote_nested(self):
    #     block = "> This is a quote\n>> This is nested\n> Back to first level"
    #     result = block_to_block_type(block)
    #     self.assertEqual(result, BlockType.QUOTE)

    def test_quote_with_space_required(self):
        block = "> Proper quote with space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_not_quote_no_space(self):
        block = ">This is not a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_not_quote_bracket_in_middle(self):
        block = "This > is not a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # UNORDERED LIST TESTS
    def test_unordered_list_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "- Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_with_space_required(self):
        block = "- Proper list item with space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_not_unordered_list_no_space(self):
        block = "-This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_not_unordered_list_dash_in_middle(self):
        block = "This - is not a list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # ORDERED LIST TESTS
    def test_ordered_list_simple(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        block = "1. Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    # def test_ordered_list_double_digits(self):
    #     block = "10. Item ten\n11. Item eleven"
    #     result = block_to_block_type(block)
    #     self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_with_space_required(self):
        block = "1. Proper list item with space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_not_ordered_list_no_space(self):
        block = "1.This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_not_ordered_list_no_dot(self):
        block = "1 This is not a list"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_not_ordered_list_starts_zero(self):
        block = "0. This might not be a valid list"
        result = block_to_block_type(block)
        # This depends on your implementation - some parsers accept 0, others don't
        # Adjust expected result based on your requirements
        self.assertEqual(result, BlockType.PARAGRAPH)

    # EDGE CASES
    def test_empty_block(self):
        block = ""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_whitespace_only_block(self):
        block = "   \n   \n   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_mixed_list_types_should_be_paragraph(self):
        # Mixed list types in same block should not be recognized as list
        block = "- Unordered item\n1. Ordered item"
        result = block_to_block_type(block)
        # This depends on implementation - might be paragraph or first detected type
        # Adjust based on your requirements
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading_with_trailing_hashes(self):
        block = "## Heading with trailing hashes ##"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_code_block_indented(self):
        # Some markdown parsers support indented code blocks (4+ spaces)
        block = "    def indented_code():\n        pass"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)  # or BlockType.PARAGRAPH

    def test_quote_with_other_content(self):
        block = "> Quote line\nNormal line"
        result = block_to_block_type(block)
        # This should probably be paragraph since it's mixed content
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_list_with_other_content(self):
        block = "- List item\nNormal line"
        result = block_to_block_type(block)
        # This should probably be paragraph since it's mixed content
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
