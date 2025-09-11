import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_default_values(self):
        no_children = HTMLNode(tag="p", value="text here", props={"some": "value"})
        no_tag = HTMLNode(value="some text", props={"some": "value"})
        no_value = HTMLNode(
            tag="p", children=[no_children, no_tag], props={"some": "value"}
        )
        no_props = HTMLNode(tag="p", children=[no_children, no_tag, no_value])
        self.assertTrue(
            no_children.children is None
            and no_tag.tag is None
            and no_value.value is None
            and no_props.props is None
        )

    def test_props_to_html(self):
        no_children = HTMLNode(tag="p", value="text here", props={"some": "value"})
        hnode = HTMLNode("p", "text here", no_children, {"some": "value"})
        self.assertTrue(hnode.props_to_html() == 'some="value"')

    def test_repr(self):
        no_children = HTMLNode(tag="p", value="text here", props={"some": "value"})
        hnode = HTMLNode("p", "text here", no_children, {"some": "value"})
        self.assertTrue(
            hnode.__repr__()
            == f"tag: {hnode.tag}\nvalue: {hnode.value}\nchildren: {hnode.children}\nprops: {hnode.props}"
        )

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
        child_node = LeafNode("span", "some text")
        child_node2 = LeafNode("span", "some text")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>some text</span><span>some text</span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h3(self):
        node = LeafNode("h3", "Hello, world!")
        self.assertEqual(node.to_html(), "<h3>Hello, world!</h3>")

    def test_leaf_to_html_h3(self):
        node = LeafNode("h3", "Hello, world!")
        self.assertEqual(node.to_html(), "<h3>Hello, world!</h3>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
