from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:

        text = node.text
        new_node = text.split(delimiter)

        if node.text_type != TextType.TEXT or len(new_node) == 1:
            # no splitting
            result.append(node)
            continue

        if len(new_node) % 2 == 0:
            raise ValueError("delimiters unmatched")

        for i in range(len(new_node)):
            if new_node[i] == "":
                continue

            if i % 2 == 0:
                maketype = TextType.TEXT
            else:
                maketype = text_type

            result.append(TextNode(new_node[i], maketype))

    return result
