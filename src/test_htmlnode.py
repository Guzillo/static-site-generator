import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
