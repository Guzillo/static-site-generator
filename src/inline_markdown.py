from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue
        occurences = node.text.count(delimiter)
        if occurences % 2 != 0:
            raise Exception("Invalid markdown exception")
        tmp_nodes = node.text.split(delimiter)
        for i in range(len(tmp_nodes)):
            if i % 2 != 0:
                new_nodes.append(TextNode(tmp_nodes[i], text_type))
            else:
                new_nodes.append(TextNode(tmp_nodes[i], TextType.PLAIN))
        new_nodes = [x for x in new_nodes if x.text != ""]
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[([^\]\[\)\(]*?)\]\(([^\(\)\[\]]*?)\)", text)
