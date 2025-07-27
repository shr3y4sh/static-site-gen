import re


def extract_markdown_images(text):
    # regex = r"!\[(.*?)\]\((.*?)\)"

    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)


def extract_markdown_links(text):
    # regex = r"\[(.*?)\]\((.*?)\)"

    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)


if __name__ == "__main__":

    text = "This is text with an ![alt text](https://example.com/image.png) and another ![second alt](http://test.com/pic.jpg)"

    print(extract_markdown_images(text))
