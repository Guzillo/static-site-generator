from textnode import TextNode
from textnode import TextType


def main():
    text_node = TextNode("dummy", TextType.BOLD, "https://www.boot.dev")
    print(text_node)


if __name__ == "__main__":
    main()
