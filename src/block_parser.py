from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if is_code(block):
        return BlockType.CODE

    first_line = block.split("\n", 1)[0]

    if is_unordered_list(first_line):
        for line in block.split("\n"):
            if not is_unordered_list(line):
                return BlockType.PARAGRAPH

        return BlockType.UNORDERED_LIST

    if is_ordered_list(first_line, 1):
        i = 0
        for line in block.split("\n"):
            i += 1
            if not is_ordered_list(line, i):
                return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST

    if is_heading(first_line):
        return BlockType.HEADING

    if is_quote(first_line):
        for line in block.split("\n"):
            if not is_quote(line):
                return BlockType.PARAGRAPH

        return BlockType.QUOTE

    return BlockType.PARAGRAPH


def is_unordered_list(line):
    return line.startswith("- ")


def is_ordered_list(line, number):
    return line.startswith(f"{number}. ")


def is_code(text):
    return text.startswith("```") and text.endswith("```")


def is_quote(line):
    return line.startswith("> ")


def is_heading(line):
    valid_starts = ["# ", "## ", "### ", "#### ", "##### ", "###### "]

    for item in valid_starts:
        if line.startswith(item):
            return True

    return False


if __name__ == "__main__":
    block = "1. First item\n2. Second item\n3. Third item"

    print(block_to_block_type(block))
