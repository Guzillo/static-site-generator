from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    blocks = list(filter(lambda x: x != "", blocks))
    return blocks


def block_to_block_type(markdown_text_block):
    lines = markdown_text_block.split("\n")
    if re.search(r"^#{1,6} .+", markdown_text_block):
        return BlockType.HEADING
    if re.search(r"^```[A-Za-z0-9\n]*```$", markdown_text_block):
        return BlockType.CODE
    status = True
    for line in lines:
        if not re.search(r">.*", line):
            status = False
    if status:
        return BlockType.QUOTE

    status = True
    for line in lines:
        if not re.search(r"- .*", line):
            status = False
    if status:
        return BlockType.UNORDERED_LIST

    status = True
    index = 1
    for line in lines:
        if not re.search(rf"{index}. .*", line):
            status = False
        index += 1
    if status:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
