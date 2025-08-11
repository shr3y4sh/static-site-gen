from markdown_extractor import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def preprocess(old_nodes, ttype, extractor):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text

        data = extractor(text)
        if not data:
            result.append(node)
            continue

        for extra, url in data:
            markdown_syntax = f"[{extra}]({url})"

            if ttype == TextType.IMAGE:
                markdown_syntax = "!" + markdown_syntax

            splits = text.split(markdown_syntax, 1)

            if splits[0]:
                result.append(TextNode(splits[0], TextType.TEXT))

            result.append(TextNode(extra, ttype, url))
            text = splits[1]

        if text:
            result.append(TextNode(text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes):
    return preprocess(old_nodes, TextType.LINK, extract_markdown_links)


def split_nodes_image(old_nodes):
    return preprocess(old_nodes, TextType.IMAGE, extract_markdown_images)
