from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType
from split_links import split_nodes_link, split_nodes_image


def text_to_textnodes(text):
    if not text:
        return []

    result = split_nodes_link([TextNode(text, TextType.TEXT)])
    result = split_nodes_image(result)

    saved_result = result

    try:
        result = split_nodes_delimiter(result, "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)
        result = split_nodes_delimiter(result, "`", TextType.CODE)
    except ValueError as e:
        result = saved_result

    return result
