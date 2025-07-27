import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init_with_tag_and_value(self):
        node = LeafNode("p", "Hello World")

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag_value_and_props(self):
        props = {"class": "highlight", "id": "main"}
        node = LeafNode("div", "Content", props)

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, props)

    def test_init_without_tag(self):
        node = LeafNode(None, "Plain text")

        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Plain text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_empty_props(self):
        node = LeafNode("span", "Text", {})

        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Text")
        self.assertEqual(node.props, {})

    def test_to_html_with_tag_and_value(self):
        node = LeafNode("p", "This is a paragraph")

        result = node.to_html()
        self.assertEqual(result, "<p>This is a paragraph</p>")

    def test_to_html_with_tag_value_and_props(self):
        props = {"class": "bold", "id": "text1"}
        node = LeafNode("b", "Bold text", props)

        result = node.to_html()
        expected = '<b class="bold" id="text1">Bold text</b>'
        self.assertEqual(result, expected)

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Raw text content")

        result = node.to_html()
        self.assertEqual(result, "Raw text content")

    # def test_to_html_self_closing_tag(self):
    #     props = {"src": "image.jpg", "alt": "Description"}
    #     node = LeafNode("img", "", props)

    #     # Note: This tests current implementation behavior
    #     # You might want to handle self-closing tags differently
    #     result = node.to_html()
    #     expected = '<img src="image.jpg" alt="Description"></img>'
    #     self.assertEqual(result, expected)

    def test_to_html_with_special_characters_in_value(self):
        node = LeafNode("p", "Text with <special> & 'characters'")

        result = node.to_html()
        self.assertEqual(result, "<p>Text with <special> & 'characters'</p>")

    def test_to_html_raises_error_with_no_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(str(context.exception), "Leaf Node must have a value")

    def test_to_html_raises_error_with_empty_string_value(self):
        node = LeafNode("p", "")

        with self.assertRaises(ValueError) as context:
            node.to_html()

        self.assertEqual(str(context.exception), "Leaf Node must have a value")

    def test_to_html_raises_error_with_whitespace_only_value(self):
        node = LeafNode("p", "   ")

        # Whitespace should be considered a valid value
        result = node.to_html()
        self.assertEqual(result, "<p>   </p>")

    def test_to_html_with_single_prop(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})

        result = node.to_html()
        self.assertEqual(result, '<a href="https://example.com">Click here</a>')

    def test_to_html_with_multiple_props(self):
        props = {"class": "btn", "type": "submit", "disabled": "true"}
        node = LeafNode("button", "Submit", props)

        result = node.to_html()
        # Should contain all props
        self.assertIn('class="btn"', result)
        self.assertIn('type="submit"', result)
        self.assertIn('disabled="true"', result)
        self.assertTrue(result.startswith("<button"))
        self.assertTrue(result.endswith("Submit</button>"))

    def test_common_html_elements(self):
        # Test various common HTML elements
        test_cases = [
            ("h1", "Main Title"),
            ("span", "Inline text"),
            ("strong", "Bold text"),
            ("em", "Emphasized text"),
            ("code", "print('hello')"),
            ("li", "List item"),
        ]

        for tag, value in test_cases:
            with self.subTest(tag=tag, value=value):
                node = LeafNode(tag, value)
                result = node.to_html()
                expected = f"<{tag}>{value}</{tag}>"
                self.assertEqual(result, expected)

    def test_numeric_and_boolean_prop_values(self):
        props = {"tabindex": "1", "colspan": "2", "hidden": ""}
        node = LeafNode("td", "Cell content", props)

        result = node.to_html()
        self.assertIn('tabindex="1"', result)
        self.assertIn('colspan="2"', result)
        self.assertIn('hidden=""', result)

    def test_to_html_with_quotes_in_props(self):
        props = {"title": 'Say "Hello" to user', "data-info": "It's working"}
        node = LeafNode("div", "Content", props)

        result = node.to_html()
        # Props should be properly escaped/handled
        self.assertIn('title="Say "Hello" to user"', result)
        self.assertIn('data-info="It\'s working"', result)

    def test_inheritance_from_htmlnode(self):
        # Verify that LeafNode properly inherits from HTMLNode
        node = LeafNode("p", "Test")

        # Should have inherited props_to_html method
        self.assertTrue(hasattr(node, "props_to_html"))

        # Children should always be None for LeafNode
        self.assertIsNone(node.children)

    def test_repr_method(self):
        node = LeafNode("p", "Test content", {"class": "test"})

        repr_str = repr(node)
        # Should use inherited __repr__ from HTMLNode
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("p", repr_str)
        self.assertIn("Test content", repr_str)


if __name__ == "__main__":
    unittest.main()
