import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is dummy text", TextType.LINK, "http://www.google.com")
        self.assertTrue(repr(node).startswith("TextNode("))

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_one_with_url_one_without(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_repr_without_url(self):
        node = TextNode("Plain text", TextType.TEXT)
        expected = "TextNode(Plain text, plain_text, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        node = TextNode("Google", TextType.LINK, "http://www.google.com")
        expected = "TextNode(Google, link, http://www.google.com)"
        self.assertEqual(repr(node), expected)

    def test_all_text_types(self):
        # Test that all TextType enum values work
        text_types = [
            TextType.TEXT,
            TextType.BOLD,
            TextType.ITALIC,
            TextType.CODE,
            TextType.LINK,
            TextType.IMAGE,
        ]

        for text_type in text_types:
            node = TextNode("Test text", text_type)
            self.assertEqual(node.text_type, text_type)

    def test_properties_assignment(self):
        node = TextNode("Test text", TextType.BOLD, "http://example.com")
        self.assertEqual(node.text, "Test text")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, "http://example.com")

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_image_node(self):
        node = TextNode("Alt text", TextType.IMAGE, "http://example.com/image.png")
        node2 = TextNode("Alt text", TextType.IMAGE, "http://example.com/image.png")
        self.assertEqual(node, node2)

    def test_code_node(self):
        node = TextNode("print('hello')", TextType.CODE)
        self.assertEqual(node.text, "print('hello')")
        self.assertEqual(node.text_type, TextType.CODE)


if __name__ == "__main__":
    unittest.main()
