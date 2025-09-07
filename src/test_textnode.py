import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is other text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_prop(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        assert node.url is None and node2.url is not None

    def test_text_type_prop(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node = TextNode("This is a text node", TextType.CODE)
        node = TextNode("This is a text node", TextType.IMAGE)
        node = TextNode("This is a text node", TextType.ITALIC)
        node = TextNode("This is a text node", TextType.LINK)


if __name__ == "__main__":
    unittest.main()
