import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_init_with_tag_and_children(self):
        children = [LeafNode("p", "Child 1"), LeafNode("p", "Child 2")]
        node = ParentNode("div", children)

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)
        self.assertIsNone(node.value)

    def test_init_with_tag_children_and_props(self):
        children = [LeafNode("span", "Text")]
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", children, props)

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)
        self.assertIsNone(node.value)

    def test_init_with_empty_props(self):
        children = [LeafNode("p", "Content")]
        node = ParentNode("section", children, {})

        self.assertEqual(node.tag, "section")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {})

    def test_init_raises_error_with_no_tag(self):
        children = [LeafNode("p", "Content")]

        with self.assertRaises(ValueError) as context:
            ParentNode(None, children).to_html()

        self.assertEqual(str(context.exception), "Parent node must have a tag")

    def test_init_raises_error_with_empty_tag(self):
        children = [LeafNode("p", "Content")]

        with self.assertRaises(ValueError) as context:
            ParentNode("", children).to_html()

        self.assertEqual(str(context.exception), "Parent node must have a tag")

    def test_init_raises_error_with_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()

        self.assertEqual(str(context.exception), "Parent node must have children nodes")

    def test_init_raises_error_with_empty_children_list(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", []).to_html()

        self.assertEqual(str(context.exception), "Parent node must have children nodes")

    def test_to_html_with_single_child(self):
        child = LeafNode("p", "Hello World")
        node = ParentNode("div", [child])

        result = node.to_html()
        expected = "<div><p>Hello World</p></div>"
        self.assertEqual(result, expected)

    def test_to_html_with_multiple_children(self):
        children = [
            LeafNode("h1", "Title"),
            LeafNode("p", "Paragraph 1"),
            LeafNode("p", "Paragraph 2"),
        ]
        node = ParentNode("article", children)

        result = node.to_html()
        expected = (
            "<article><h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p></article>"
        )
        self.assertEqual(result, expected)

    def test_to_html_with_props(self):
        child = LeafNode("p", "Content")
        props = {"class": "wrapper", "id": "main"}
        node = ParentNode("div", [child], props)

        result = node.to_html()
        expected = '<div class="wrapper" id="main"><p>Content</p></div>'
        self.assertEqual(result, expected)

    def test_to_html_with_nested_parent_nodes(self):
        # Grandchild
        grandchild = LeafNode("span", "Deep text")

        # Child ParentNode
        child_parent = ParentNode("p", [grandchild])

        # Root ParentNode
        root = ParentNode("div", [child_parent])

        result = root.to_html()
        expected = "<div><p><span>Deep text</span></p></div>"
        self.assertEqual(result, expected)

    def test_to_html_with_complex_nested_structure(self):
        # Create a complex nested structure
        list_items = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3"),
        ]
        unordered_list = ParentNode("ul", list_items)

        header = LeafNode("h2", "My List")

        container = ParentNode(
            "div", [header, unordered_list], {"class": "list-container"}
        )

        result = container.to_html()
        expected = '<div class="list-container"><h2>My List</h2><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>'
        self.assertEqual(result, expected)

    def test_to_html_with_mixed_child_types(self):
        # Mix of LeafNodes and ParentNodes as children
        leaf_child = LeafNode("p", "Simple paragraph")

        nested_children = [
            LeafNode("strong", "Bold"),
            LeafNode(None, " and "),
            LeafNode("em", "italic"),
        ]
        parent_child = ParentNode("p", nested_children)

        root = ParentNode("section", [leaf_child, parent_child])

        result = root.to_html()
        expected = "<section><p>Simple paragraph</p><p><strong>Bold</strong> and <em>italic</em></p></section>"
        self.assertEqual(result, expected)

    def test_to_html_with_raw_text_children(self):
        # Children including LeafNode with no tag (raw text)
        children = [
            LeafNode("strong", "Bold text"),
            LeafNode(None, " followed by raw text "),
            LeafNode("em", "and italic"),
        ]
        node = ParentNode("p", children)

        result = node.to_html()
        expected = (
            "<p><strong>Bold text</strong> followed by raw text <em>and italic</em></p>"
        )
        self.assertEqual(result, expected)

    def test_to_html_with_single_prop(self):
        child = LeafNode("span", "Text")
        node = ParentNode("div", [child], {"id": "container"})

        result = node.to_html()
        expected = '<div id="container"><span>Text</span></div>'
        self.assertEqual(result, expected)

    def test_to_html_with_multiple_props(self):
        child = LeafNode("p", "Content")
        props = {"class": "highlight", "data-id": "123", "role": "main"}
        node = ParentNode("section", [child], props)

        result = node.to_html()
        # Should contain all props
        self.assertIn('class="highlight"', result)
        self.assertIn('data-id="123"', result)
        self.assertIn('role="main"', result)
        self.assertTrue(result.startswith("<section"))
        self.assertTrue(result.endswith("</section>"))

    def test_common_html_structures(self):
        # Test common HTML parent elements
        test_cases = [
            ("div", [LeafNode("p", "Content")]),
            ("ul", [LeafNode("li", "Item")]),
            ("ol", [LeafNode("li", "First")]),
            ("table", [LeafNode("tr", "Row")]),
            # ("form", [LeafNode("input", "", {"type": "text"})]),
        ]

        for tag, children in test_cases:
            with self.subTest(tag=tag):
                node = ParentNode(tag, children)
                result = node.to_html()
                self.assertTrue(result.startswith(f"<{tag}>"))
                self.assertTrue(result.endswith(f"</{tag}>"))

    def test_deeply_nested_structure(self):
        # Create a deeply nested structure to test recursion
        deepest = LeafNode("span", "Deep")
        level3 = ParentNode("em", [deepest])
        level2 = ParentNode("strong", [level3])
        level1 = ParentNode("p", [level2])
        root = ParentNode("div", [level1])

        result = root.to_html()
        expected = "<div><p><strong><em><span>Deep</span></em></strong></p></div>"
        self.assertEqual(result, expected)

    def test_to_html_with_children_having_props(self):
        children = [
            LeafNode("a", "Link 1", {"href": "https://example1.com"}),
            LeafNode(
                "a", "Link 2", {"href": "https://example2.com", "target": "_blank"}
            ),
        ]
        node = ParentNode("nav", children, {"class": "navigation"})

        result = node.to_html()
        expected = '<nav class="navigation"><a href="https://example1.com">Link 1</a><a href="https://example2.com" target="_blank">Link 2</a></nav>'
        self.assertEqual(result, expected)

    def test_inheritance_from_htmlnode(self):
        child = LeafNode("p", "Test")
        node = ParentNode("div", [child])

        # Should have inherited props_to_html method
        self.assertTrue(hasattr(node, "props_to_html"))

        # Value should always be None for ParentNode
        self.assertIsNone(node.value)

    def test_repr_method(self):
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child], {"class": "test"})

        repr_str = repr(node)
        # Should use inherited __repr__ from HTMLNode
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("div", repr_str)


if __name__ == "__main__":
    unittest.main()
