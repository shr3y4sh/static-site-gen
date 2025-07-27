import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_node_with_single_delimiter_pair(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_single_node_with_multiple_delimiter_pairs(self):
        node = TextNode("Text with `code1` and `code2` here", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertEqual(len(result), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_single_node_no_delimiters(self):
        node = TextNode("This is plain text with no special formatting", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is plain text with no special formatting", TextType.TEXT)
        ]

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First `code` block", TextType.TEXT),
            TextNode("Second `another` block", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("another", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]

        self.assertEqual(len(result), 6)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Normal text with `code`", TextType.TEXT),
            TextNode("Already bold text", TextType.BOLD),
            TextNode("Already italic text", TextType.ITALIC),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        # First node should be split
        self.assertEqual(result[0].text, "Normal text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)

        # Other nodes should remain unchanged
        self.assertEqual(result[2].text, "Already bold text")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "Already italic text")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

    def test_delimiter_at_start_of_text(self):
        node = TextNode("`code` at start", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            # TextNode("", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]

        self.assertEqual(len(result), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_delimiter_at_end_of_text(self):
        node = TextNode("Text ends with `code`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            # TextNode("", TextType.TEXT),
        ]

        self.assertEqual(len(result), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_entire_text_is_delimited(self):
        node = TextNode("`entire text`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            # TextNode("", TextType.TEXT),
            TextNode("entire text", TextType.CODE),
            # TextNode("", TextType.TEXT),
        ]

        self.assertEqual(len(result), 1)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode("Text with unmatched `delimiter", TextType.TEXT)

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertIn("unmatched", str(context.exception).lower())

    def test_empty_delimiter_content(self):
        node = TextNode("Text with `` empty delimiters", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            # TextNode("", TextType.CODE),
            TextNode(" empty delimiters", TextType.TEXT),
        ]

        self.assertEqual(len(result), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_different_delimiters(self):
        # Test with asterisk delimiter for bold
        node = TextNode("This is *bold* text", TextType.TEXT)

        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_double_asterisk_delimiter(self):
        # Test with double asterisk for bold
        node = TextNode("This is **bold** text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_empty_input_list(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_delimiter_only_text(self):
        node = TextNode("`", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_adjacent_delimited_sections(self):
        node = TextNode("Text `code1``code2` more text", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            # TextNode("", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" more text", TextType.TEXT),
        ]

        self.assertEqual(len(result), 4)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    def test_special_characters_in_delimited_content(self):
        node = TextNode("Code: `print('hello & world')` here", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Code: ", TextType.TEXT),
            TextNode("print('hello & world')", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)

    # def test_nested_same_delimiters_invalid(self):
    #     node = TextNode("Text with `nested `code` block` here", TextType.TEXT)

    #     # This should raise an error as nested same delimiters are invalid
    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node], "`", TextType.CODE)

    def test_whitespace_only_delimited_content(self):
        node = TextNode("Text with `   ` whitespace", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("   ", TextType.CODE),
            TextNode(" whitespace", TextType.TEXT),
        ]

        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)


if __name__ == "__main__":
    unittest.main()
