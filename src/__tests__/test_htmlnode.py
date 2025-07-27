import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_with_all_params(self):
        children = [HTMLNode("p", "child1"), HTMLNode("span", "child2")]
        props = {"class": "container", "id": "main"}
        node = HTMLNode("div", "Hello World", children, props)

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_init_with_defaults(self):
        node = HTMLNode()

        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag_only(self):
        node = HTMLNode("p")

        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag_and_value(self):
        node = HTMLNode("h1", "Title")

        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag_and_children(self):
        children = [HTMLNode("li", "item1"), HTMLNode("li", "item2")]
        node = HTMLNode("ul", None, children)

        self.assertEqual(node.tag, "ul")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)

    def test_init_with_tag_and_props(self):
        props = {"href": "https://example.com", "target": "_blank"}
        node = HTMLNode("a", None, None, props)

        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, props)

    def test_props_to_html_with_single_prop(self):
        props = {"class": "highlight"}
        node = HTMLNode("div", None, None, props)

        result = node.props_to_html()
        self.assertEqual(result, 'class="highlight"')

    def test_props_to_html_with_multiple_props(self):
        props = {"class": "btn", "id": "submit", "disabled": "true"}
        node = HTMLNode("button", None, None, props)

        result = node.props_to_html()
        # Should contain all props, order may vary
        self.assertIn('class="btn"', result)
        self.assertIn('id="submit"', result)
        self.assertIn('disabled="true"', result)

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("div")

        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode("div", None, None, {})

        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_special_characters(self):
        props = {"data-value": "test & example", "title": 'Quote "test"'}
        node = HTMLNode("div", None, None, props)

        result = node.props_to_html()
        self.assertIn('data-value="test & example"', result)
        self.assertIn('title="Quote "test""', result)

    def test_to_html_not_implemented(self):
        node = HTMLNode("div", "content")

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_with_all_attributes(self):
        children = [HTMLNode("span")]
        props = {"class": "test"}
        node = HTMLNode("div", "content", children, props)

        repr_str = repr(node)
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("div", repr_str)
        self.assertIn("content", repr_str)

    def test_repr_with_no_attributes(self):
        node = HTMLNode()

        repr_str = repr(node)
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("None", repr_str)

    def test_repr_with_tag_only(self):
        node = HTMLNode("br")

        repr_str = repr(node)
        self.assertIn("HTMLNode", repr_str)
        self.assertIn("br", repr_str)

    def test_children_as_empty_list(self):
        node = HTMLNode("div", "content", [])

        self.assertEqual(node.children, [])
        self.assertIsInstance(node.children, list)

    def test_self_closing_tags(self):
        # Test common self-closing HTML tags
        self_closing_tags = ["br", "hr", "img", "input", "meta", "link"]

        for tag in self_closing_tags:
            node = HTMLNode(tag)
            self.assertEqual(node.tag, tag)
            self.assertIsNone(node.value)

    def test_props_with_boolean_attributes(self):
        props = {"disabled": "", "checked": "", "selected": ""}
        node = HTMLNode("input", None, None, props)

        result = node.props_to_html()
        self.assertIn('disabled=""', result)
        self.assertIn('checked=""', result)
        self.assertIn('selected=""', result)

    def test_nested_children_structure(self):
        grandchild = HTMLNode("span", "text")
        child = HTMLNode("p", None, [grandchild])
        parent = HTMLNode("div", None, [child])

        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child)
        self.assertEqual(child.children[0], grandchild)

    def test_props_with_numeric_values(self):
        props = {"tabindex": "1", "colspan": "2", "data-count": "42"}
        node = HTMLNode("td", None, None, props)

        result = node.props_to_html()
        self.assertIn('tabindex="1"', result)
        self.assertIn('colspan="2"', result)
        self.assertIn('data-count="42"', result)

    def test_value_with_special_characters(self):
        node = HTMLNode("p", "This has <special> & 'quoted' \"characters\"")

        self.assertEqual(node.value, "This has <special> & 'quoted' \"characters\"")


if __name__ == "__main__":
    unittest.main()
