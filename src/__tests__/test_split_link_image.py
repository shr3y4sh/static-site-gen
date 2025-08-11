import unittest

from textnode import TextNode, TextType
from split_links import split_nodes_link, split_nodes_image


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("Text with a [link](https://example.com) here", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [
            TextNode("Text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertListEqual(result, expected)

    def test_no_links(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [TextNode("This is plain text with no links", TextType.TEXT)]

        self.assertListEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode(
            "[start link](https://start.com) followed by text", TextType.TEXT
        )

        result = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "https://start.com"),
            TextNode(" followed by text", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode("Text ending with [end link](https://end.com)", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://end.com"),
        ]

        self.assertListEqual(result, expected)

    def test_only_link(self):
        node = TextNode("[only link](https://only.com)", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://only.com"),
        ]

        self.assertListEqual(result, expected)

    def test_adjacent_links(self):
        node = TextNode(
            "[first](https://first.com)[second](https://second.com)", TextType.TEXT
        )

        result = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "https://first.com"),
            TextNode("second", TextType.LINK, "https://second.com"),
        ]

        self.assertListEqual(result, expected)

    def test_empty_link_text(self):
        node = TextNode("Link with empty text [](https://empty.com)", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [
            TextNode("Link with empty text ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://empty.com"),
        ]

        self.assertListEqual(result, expected)

    def test_empty_url(self):
        node = TextNode("Link with empty URL [empty url]()", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [
            TextNode("Link with empty URL ", TextType.TEXT),
            TextNode("empty url", TextType.LINK, ""),
        ]

        self.assertListEqual(result, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First [link1](url1)", TextType.TEXT),
            TextNode("Second [link2](url2)", TextType.TEXT),
        ]

        result = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]

        self.assertListEqual(result, expected)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text with [link](url)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]

        result = split_nodes_link(nodes)

        # First node should be split
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)

        # Other nodes should remain unchanged
        self.assertEqual(result[2].text, "Already bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "Already italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

    def test_ignores_image_syntax(self):
        node = TextNode("This has ![image](img.png) and [link](url)", TextType.TEXT)

        result = split_nodes_link([node])
        expected = [
            TextNode("This has ![image](img.png) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]

        self.assertListEqual(result, expected)

    def test_empty_input_list(self):
        result = split_nodes_link([])
        self.assertListEqual(result, [])

    def test_special_characters_in_url(self):
        node = TextNode(
            "Link [search](https://example.com/search?q=hello&type=web)", TextType.TEXT
        )

        result = split_nodes_link([node])
        expected = [
            TextNode("Link ", TextType.TEXT),
            TextNode(
                "search", TextType.LINK, "https://example.com/search?q=hello&type=web"
            ),
        ]

        self.assertListEqual(result, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertListEqual(result, expected)

    def test_single_image(self):
        node = TextNode(
            "Text with an ![alt text](https://example.com/image.png) here",
            TextType.TEXT,
        )

        result = split_nodes_image([node])
        expected = [
            TextNode("Text with an ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_no_images(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [TextNode("This is plain text with no images", TextType.TEXT)]

        self.assertListEqual(result, expected)

    def test_image_at_start(self):
        node = TextNode(
            "![start image](https://start.png) followed by text", TextType.TEXT
        )

        result = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "https://start.png"),
            TextNode(" followed by text", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode("Text ending with ![end image](https://end.png)", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://end.png"),
        ]

        self.assertListEqual(result, expected)

    def test_only_image(self):
        node = TextNode("![only image](https://only.png)", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "https://only.png"),
        ]

        self.assertListEqual(result, expected)

    def test_adjacent_images(self):
        node = TextNode(
            "![first](https://first.png)![second](https://second.png)", TextType.TEXT
        )

        result = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "https://first.png"),
            TextNode("second", TextType.IMAGE, "https://second.png"),
        ]

        self.assertListEqual(result, expected)

    def test_empty_alt_text(self):
        node = TextNode("Image with empty alt ![](https://empty.png)", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [
            TextNode("Image with empty alt ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://empty.png"),
        ]

        self.assertListEqual(result, expected)

    def test_empty_url(self):
        node = TextNode("Image with empty URL ![empty url]()", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [
            TextNode("Image with empty URL ", TextType.TEXT),
            TextNode("empty url", TextType.IMAGE, ""),
        ]

        self.assertListEqual(result, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First ![img1](url1)", TextType.TEXT),
            TextNode("Second ![img2](url2)", TextType.TEXT),
        ]

        result = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]

        self.assertListEqual(result, expected)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text with ![image](url)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]

        result = split_nodes_image(nodes)

        # First node should be split
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)

        # Other nodes should remain unchanged
        self.assertEqual(result[2].text, "Already bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "Already italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

    def test_ignores_link_syntax(self):
        node = TextNode("This has [link](url) and ![image](img.png)", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [
            TextNode("This has [link](url) and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
        ]

        self.assertListEqual(result, expected)

    def test_empty_input_list(self):
        result = split_nodes_image([])
        self.assertListEqual(result, [])

    def test_special_characters_in_url(self):
        node = TextNode(
            "Image ![photo](https://example.com/photos/my%20photo.jpg)", TextType.TEXT
        )

        result = split_nodes_image([node])
        expected = [
            TextNode("Image ", TextType.TEXT),
            TextNode(
                "photo", TextType.IMAGE, "https://example.com/photos/my%20photo.jpg"
            ),
        ]

        self.assertListEqual(result, expected)

    def test_mixed_with_regular_brackets(self):
        node = TextNode("Regular [brackets] and ![image](url)", TextType.TEXT)

        result = split_nodes_image([node])
        expected = [
            TextNode("Regular [brackets] and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
        ]

        self.assertListEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
