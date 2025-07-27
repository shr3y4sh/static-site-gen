import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from text_to_html import text_to_html


class TestTextToHtml(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("Plain text", TextType.TEXT)

        result = text_to_html(node)
        expected = LeafNode(None, "Plain text")

        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

    def test_text_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)

        result = text_to_html(node)
        expected = LeafNode("b", "Bold text")

        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

    def test_text_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)

        result = text_to_html(node)
        expected = LeafNode("i", "Italic text")

        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

    def test_text_type_code(self):
        node = TextNode("print('hello')", TextType.CODE)

        result = text_to_html(node)
        expected = LeafNode("code", "print('hello')")

        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

    def test_text_type_link_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")

        result = text_to_html(node)
        expected = LeafNode("a", "Click here", {"href": "https://example.com"})

        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

    def test_text_type_link_without_url(self):
        node = TextNode("Link text", TextType.LINK, None)

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Link node must have a URL")

    def test_text_type_link_with_empty_url(self):
        node = TextNode("Link text", TextType.LINK, "")

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Link node must have a URL")

    def test_text_type_image_with_url(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")

        result = text_to_html(node)
        expected = LeafNode(
            "img", "", {"src": "https://example.com/image.png", "alt": "Alt text"}
        )

        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.props, expected.props)

    def test_text_type_image_without_url(self):
        node = TextNode("Alt text", TextType.IMAGE, None)

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Image node must have a URL")

    def test_text_type_image_with_empty_url(self):
        node = TextNode("Alt text", TextType.IMAGE, "")

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Image node must have a URL")

    def test_invalid_text_type(self):
        # Create a TextNode with an invalid type (this would require modifying the enum or mocking)
        # Since we can't easily create an invalid enum value, we'll test with None
        node = TextNode("Test text", None)

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Unknown text type")

    def test_empty_text_content(self):
        # Test with empty text for different types
        test_cases = [
            (TextType.TEXT, None, ""),
            (TextType.BOLD, "b", ""),
            (TextType.ITALIC, "i", ""),
            (TextType.CODE, "code", ""),
        ]

        for text_type, expected_tag, expected_value in test_cases:
            with self.subTest(text_type=text_type):
                node = TextNode("", text_type)
                result = text_to_html(node)

                self.assertEqual(result.tag, expected_tag)
                self.assertEqual(result.value, expected_value)

    def test_text_with_special_characters(self):
        special_text = "Text with <special> & 'characters' \"quotes\""
        test_cases = [
            (TextType.TEXT, None),
            (TextType.BOLD, "b"),
            (TextType.ITALIC, "i"),
            (TextType.CODE, "code"),
        ]

        for text_type, expected_tag in test_cases:
            with self.subTest(text_type=text_type):
                node = TextNode(special_text, text_type)
                result = text_to_html(node)

                self.assertEqual(result.tag, expected_tag)
                self.assertEqual(result.value, special_text)

    def test_link_with_special_characters_in_url(self):
        node = TextNode(
            "Search", TextType.LINK, "https://example.com/search?q=hello+world&type=web"
        )

        result = text_to_html(node)
        expected_props = {"href": "https://example.com/search?q=hello+world&type=web"}

        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "Search")
        self.assertEqual(result.props, expected_props)

    def test_image_with_special_characters_in_url(self):
        node = TextNode(
            "My Image", TextType.IMAGE, "https://example.com/images/my%20image.png"
        )

        result = text_to_html(node)
        expected_props = {
            "src": "https://example.com/images/my%20image.png",
            "alt": "My Image",
        }

        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, expected_props)

    def test_all_valid_text_types_exhaustive(self):
        # Comprehensive test for all valid TextType enum values
        test_cases = [
            (TextNode("Plain", TextType.TEXT), None, "Plain", None),
            (TextNode("Bold", TextType.BOLD), "b", "Bold", None),
            (TextNode("Italic", TextType.ITALIC), "i", "Italic", None),
            (TextNode("Code", TextType.CODE), "code", "Code", None),
            (
                TextNode("Link", TextType.LINK, "http://test.com"),
                "a",
                "Link",
                {"href": "http://test.com"},
            ),
            (
                TextNode("Alt", TextType.IMAGE, "http://img.com"),
                "img",
                "",
                {"src": "http://img.com", "alt": "Alt"},
            ),
        ]

        for text_node, expected_tag, expected_value, expected_props in test_cases:
            with self.subTest(text_type=text_node.text_type):
                result = text_to_html(text_node)

                self.assertEqual(result.tag, expected_tag)
                self.assertEqual(result.value, expected_value)
                self.assertEqual(result.props, expected_props)

    def test_function_returns_leafnode_instance(self):
        node = TextNode("Test", TextType.TEXT)

        result = text_to_html(node)

        self.assertIsInstance(result, LeafNode)

    def test_link_with_whitespace_url(self):
        node = TextNode("Link", TextType.LINK, "   ")

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Link node must have a URL")

    def test_image_with_whitespace_url(self):
        node = TextNode("Alt", TextType.IMAGE, "   ")

        with self.assertRaises(ValueError) as context:
            text_to_html(node)

        self.assertEqual(str(context.exception), "Image node must have a URL")

    def test_case_sensitivity_of_text_types(self):
        # Test that the function works with all enum values as defined
        for text_type in TextType:
            if text_type in [TextType.LINK, TextType.IMAGE]:
                node = TextNode("Test", text_type, "http://example.com")
            else:
                node = TextNode("Test", text_type)

            # Should not raise an exception for any valid TextType
            result = text_to_html(node)
            self.assertIsInstance(result, LeafNode)


if __name__ == "__main__":
    unittest.main()
