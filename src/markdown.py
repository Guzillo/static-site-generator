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


def copy_files(from_path, to_path):
    if not os.path.isdir(from_path):
        raise Exception("Path from you want to copy from doesn't exists")
    shutil.rmtree(to_path, ignore_errors=True)

    if not os.path.exists(os.path.abspath(to_path)):
        os.mkdir(os.path.abspath(to_path))
    files = os.listdir(from_path)
    for file in files:
        if os.path.isdir(os.path.join(os.path.abspath(from_path), file)):
            copy_files(os.path.join(from_path, file), os.path.join(to_path, file))
            continue
        shutil.copy(os.path.join(from_path, file), os.path.join(to_path, file))


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = None
    template_content = None
    with open(from_path) as f:
        md_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    if template_content is None:
        raise Exception("Template is absent")
    markdown_html = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", markdown_html)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        if os.path.isdir(os.path.join(dir_path_content, file)):
            if not os.path.exists(os.path.join(dest_dir_path, file)):
                os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file),
                basepath,
            )
            continue
        one = os.path.join(os.path.abspath(dir_path_content), file)
        two = os.path.join(os.path.abspath(dest_dir_path), file)
        print(f"file:{one} --> file:{two}")
        html_file_name = file[::-1].split(".", 1)[1][::-1] + ".html"
        generate_page(
            os.path.join(os.path.abspath(dir_path_content), file),
            template_path,
            os.path.join(os.path.abspath(dest_dir_path), html_file_name),
            basepath,
        )
