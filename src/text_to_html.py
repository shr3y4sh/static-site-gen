from leafnode import LeafNode
from textnode import TextType, TextNode


def text_to_html(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        if not text_node.url or text_node.url.isspace():
            raise ValueError("Link node must have a URL")

        return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})

    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url or text_node.url.isspace():
            raise ValueError("Image node must have a URL")

        return LeafNode(
            "img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"}
        )

    else:
        raise ValueError("Unknown text type")
