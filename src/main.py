from textnode import TextNode, LeafNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import inline_markdown


def main():
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(inline_markdown.extract_markdown_links(text))


if __name__ == "__main__":
    main()
