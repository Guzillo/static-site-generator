import unittest
from textnode import TextNode, TextType, text_node_to_html_node




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

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        content = "This is bold node"
        node = TextNode(content, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, content)

    def test_italic(self):
        content = "This is italic node"
        node = TextNode(content, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, content)

    def test_code(self):
        content = "This is code node"
        node = TextNode(content, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, content)

    def test_link(self):
        content = "This is a link"
        url = "https://example.com"
        node = TextNode(content, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, content)
        self.assertEqual(html_node.props.get("href"), url)

    def test_image(self):
        url = "https://example.com/image.png"
        node = TextNode("", TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props.get("src"), url)


if __name__ == "__main__":
    unittest.main()
