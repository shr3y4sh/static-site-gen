import unittest

# Assuming your functions will be in a file named markdown_extractor.py
# You would replace this with the actual import
from markdown_extractor import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_multiple_images(self):
        text = "This is text with an ![alt text](https://example.com/image.png) and another ![second alt](http://test.com/pic.jpg)"
        result = extract_markdown_images(text)
        expected = [
            ("alt text", "https://example.com/image.png"),
            ("second alt", "http://test.com/pic.jpg"),
        ]
        self.assertListEqual(result, expected)

    def test_extract_single_image(self):
        text = "A single image: ![an image](path/to/image.gif)"
        result = extract_markdown_images(text)
        expected = [("an image", "path/to/image.gif")]
        self.assertListEqual(result, expected)

    def test_no_images(self):
        text = "This is plain text with no images."
        result = extract_markdown_images(text)
        self.assertListEqual(result, [])

    def test_image_at_start_of_text(self):
        text = "![start](start.png) This is the rest of the text."
        result = extract_markdown_images(text)
        expected = [("start", "start.png")]
        self.assertListEqual(result, expected)

    def test_image_at_end_of_text(self):
        text = "Text ends with an image ![end](end.png)"
        result = extract_markdown_images(text)
        expected = [("end", "end.png")]
        self.assertListEqual(result, expected)

    def test_only_image_in_text(self):
        text = "![solo](solo.jpg)"
        result = extract_markdown_images(text)
        expected = [("solo", "solo.jpg")]
        self.assertListEqual(result, expected)

    def test_empty_alt_text(self):
        text = "Image with no alt text: ![](no-alt.gif)"
        result = extract_markdown_images(text)
        expected = [("", "no-alt.gif")]
        self.assertListEqual(result, expected)

    def test_empty_url(self):
        text = "Image with no URL: ![no url]()"
        result = extract_markdown_images(text)
        expected = [("no url", "")]
        self.assertListEqual(result, expected)

    def test_empty_alt_and_url(self):
        text = "Image with nothing: ![]()"
        result = extract_markdown_images(text)
        expected = [("", "")]
        self.assertListEqual(result, expected)

    def test_mixed_with_links(self):
        text = "An image ![img](img.png) and a [link](link.html)."
        result = extract_markdown_images(text)
        expected = [("img", "img.png")]
        self.assertListEqual(result, expected)

    def test_malformed_markdown_images(self):
        # These should not be matched
        malformed_texts = [
            "[not an image](link.com)",  # Missing !
            "![no closing bracket(link.com)",  # Missing ]
            "![no opening parenthesis]link.com)",  # Missing (
            "![no closing parenthesis](link.com",  # Missing )
            "![extra space] (link.com)",  # Space between brackets and parens
            "text ! [image](url) text",  # Space between ! and [
        ]
        for text in malformed_texts:
            with self.subTest(text=text):
                self.assertListEqual(extract_markdown_images(text), [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(result, expected)

    def test_extract_single_link(self):
        text = "A single link: [my website](https://mysite.com)"
        result = extract_markdown_links(text)
        expected = [("my website", "https://mysite.com")]
        self.assertListEqual(result, expected)

    def test_no_links(self):
        text = "This is plain text with no links."
        result = extract_markdown_links(text)
        self.assertListEqual(result, [])

    def test_link_at_start_of_text(self):
        text = "[start link](start.html) This is the rest of the text."
        result = extract_markdown_links(text)
        expected = [("start link", "start.html")]
        self.assertListEqual(result, expected)

    def test_link_at_end_of_text(self):
        text = "Text ends with a link [end link](end.html)"
        result = extract_markdown_links(text)
        expected = [("end link", "end.html")]
        self.assertListEqual(result, expected)

    def test_only_link_in_text(self):
        text = "[solo link](solo.html)"
        result = extract_markdown_links(text)
        expected = [("solo link", "solo.html")]
        self.assertListEqual(result, expected)

    def test_empty_link_text(self):
        text = "Link with no text: [](no-text.html)"
        result = extract_markdown_links(text)
        expected = [("", "no-text.html")]
        self.assertListEqual(result, expected)

    def test_empty_url(self):
        text = "Link with no URL: [no url]()"
        result = extract_markdown_links(text)
        expected = [("no url", "")]
        self.assertListEqual(result, expected)

    def test_empty_link_text_and_url(self):
        text = "Link with nothing: []()"
        result = extract_markdown_links(text)
        expected = [("", "")]
        self.assertListEqual(result, expected)

    def test_mixed_with_images(self):
        text = "A link [link](link.html) and an image ![img](img.png)."
        result = extract_markdown_links(text)
        expected = [("link", "link.html")]
        self.assertListEqual(result, expected)

    def test_malformed_markdown_links(self):
        # These should not be matched
        malformed_texts = [
            "![this is an image](image.png)",  # This is an image, not a link
            "[no closing bracket(link.com)",  # Missing ]
            "[no opening parenthesis]link.com)",  # Missing (
            "[no closing parenthesis](link.com",  # Missing )
            "[extra space] (link.com)",  # Space between brackets and parens
        ]
        for text in malformed_texts:
            with self.subTest(text=text):
                self.assertListEqual(extract_markdown_links(text), [])


if __name__ == "__main__":
    unittest.main()
