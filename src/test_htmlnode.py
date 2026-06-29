import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Just text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Just text", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, Hello, None, {'class': 'greeting'})",
        )
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i></p>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>text</span></div>',
        )

    def test_to_html_no_tag_raises(self):
        parent = ParentNode(None, [LeafNode("span", "text")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children_raises(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

if __name__ == "__main__":
    unittest.main()