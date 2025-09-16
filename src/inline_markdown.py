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
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        occurences = extract_markdown_images(node.text)
        current_text = node.text
        if occurences == []:
            new_nodes.append(node)
        else:
            for occurence in occurences:
                img_alt, img_src = occurence
                sections = current_text.split(f"![{img_alt}]({img_src})", 1)
                current_text = sections[1]
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_src))
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.PLAIN))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        occurences = extract_markdown_links(node.text)
        current_text = node.text
        if occurences == []:
            new_nodes.append(node)
        else:
            for occurence in occurences:
                link_alt, link_url = occurence
                sections = current_text.split(f"[{link_alt}]({link_url})", 1)
                current_text = sections[1]
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.PLAIN))
    return new_nodes


def text_to_textnodes(text):
    new_nodes = split_nodes_delimiter(
        [TextNode(text, TextType.PLAIN)], "**", TextType.BOLD
    )
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
