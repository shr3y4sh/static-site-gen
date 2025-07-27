from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")

        if not self.children:
            raise ValueError("Parent node must have children nodes")

        buffer = f"<{self.tag}{f" {self.props_to_html()}" if self.props else ""}>"

        for child in self.children:
            buffer += child.to_html()

        buffer += f"</{self.tag}>"

        return buffer
