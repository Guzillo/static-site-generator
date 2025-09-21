from os.path import dirname
from typing import List
import block_markdown, inline_markdown, textnode, htmlnode
from block_markdown import BlockType
import re
import shutil
import os


def markdown_to_html_node(markdown):
    blocks = block_markdown.markdown_to_blocks(markdown)
    final_children = []
    for block in blocks:
        block_type = block_markdown.block_to_block_type(block)
        node = None
        if block_type == BlockType.HEADING:
            raw_tag, content = re.findall(r"(^#{1,6}) ([\S\s]*)", block)[0]
            tag = f"h{len(raw_tag)}"
            node = htmlnode.ParentNode(tag, text_to_children(content))
        elif block_type == BlockType.PARAGRAPH:
            joined = " ".join(block.split("\n"))
            node = htmlnode.ParentNode("p", text_to_children(joined))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            reduced_lines = list(map(lambda x: x[2:], lines))
            reduced_of_empty_lines = list(filter(lambda x: x != "", reduced_lines))
            joined = " ".join(reduced_of_empty_lines)
            children = text_to_children(joined)
            node = htmlnode.ParentNode("blockquote", children)
        elif block_type == BlockType.CODE:
            node = htmlnode.ParentNode(
                "pre",
                [
                    htmlnode.ParentNode(
                        "code",
                        [
                            textnode.text_node_to_html_node(
                                textnode.TextNode(block[4:-3], textnode.TextType.PLAIN)
                            ),
                        ],
                    )
                ],
            )
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            reduced_lines = list(map(lambda x: x[2:], lines))
            children = []
            for line in reduced_lines:
                if line != "":
                    children.append(
                        htmlnode.ParentNode("li", text_to_children(line.strip()))
                    )
            node = htmlnode.ParentNode("ul", children)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            reduced_lines = list(map(lambda x: x[2:], lines))
            children = []
            for line in reduced_lines:
                if line != "":
                    children.append(
                        htmlnode.ParentNode("li", text_to_children(line.strip()))
                    )
            node = htmlnode.ParentNode("ol", children)
        final_children.append(node)
    return htmlnode.ParentNode("html", [htmlnode.ParentNode("div", final_children)])


def text_to_children(text):
    text_nodes = inline_markdown.text_to_textnodes(text)
    new_nodes = []
    for node in text_nodes:
        new_nodes.append(textnode.text_node_to_html_node(node))
    return new_nodes


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("There is no title")
