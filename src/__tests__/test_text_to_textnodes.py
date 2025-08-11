import unittest

# Assuming the function will be in a file named `markdown_to_textnode.py`
# along with your TextNode/TextType definitions.
from textnode import TextNode, TextType
from markdown_to_textnode import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_only(self):
        text = "This is a simple sentence with no markdown."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a simple sentence with no markdown.", TextType.TEXT)
        ]
        self.assertListEqual(result, expected)

    def test_bold_text(self):
        text = "This is text with **bolded content** inside."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bolded content", TextType.BOLD),
            TextNode(" inside.", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_italic_text(self):
        text = "This is text with *italic content* inside."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic content", TextType.ITALIC),
            TextNode(" inside.", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_code_block(self):
        text = "This is text with a `code block` inside."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside.", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_single_link(self):
        text = "Here is a link to [a website](https://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is a link to ", TextType.TEXT),
            TextNode("a website", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_single_image(self):
        text = "Look at this image: ![alt text](https://example.com/image.png)!"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Look at this image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("!", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_multiple_delimiters(self):
        text = "Some **bold text** and some *italic text*."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and some ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_image_link_and_bold(self):
        text = "An image ![img](img.png), a link [link](link.com), and **bold** text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("An image ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(", a link ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_all_markdown_types(self):
        text = "This is **bold** and *italic* with `code`, an ![image](img.png), and a [link](link.com)!"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "link.com"),
            TextNode("!", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_markdown_at_start(self):
        text = "**Bold** at the beginning."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the beginning.", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_markdown_at_end(self):
        text = "Text ending with an ![image](img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text ending with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
        ]
        self.assertListEqual(result, expected)

    def test_adjacent_markdown(self):
        text = "Adjacent markdown: ![image](img.png)[link](link.com)**bold**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Adjacent markdown: ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode("link", TextType.LINK, "link.com"),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(result, expected)

    def test_malformed_markdown_is_plain_text(self):
        text = "This has a [malformed link and **unclosed bold."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This has a [malformed link and **unclosed bold.", TextType.TEXT)
        ]
        # This tests that your splitting logic doesn't crash or create partial nodes
        # from invalid markdown, but instead treats it as plain text.
        self.assertListEqual(result, expected)

    def test_empty_input_string(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertListEqual(result, [])

    def test_complex_nesting_like_case(self):
        # The prompt doesn't require true nesting, but tests how sequential splitting works.
        # Assuming an order of: image, link, bold, italic
        text = "A link with **bold content** inside: [a **bold** link](link.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("A link with ", TextType.TEXT),
            TextNode("bold content", TextType.BOLD),
            TextNode(" inside: ", TextType.TEXT),
            TextNode("a **bold** link", TextType.LINK, "link.com"),
        ]
        # This is a key test. The text inside the link ("a **bold** link") is NOT
        # further processed because link extraction happens before delimiter splitting.
        # This is a common and reasonable implementation choice.
        self.assertListEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
