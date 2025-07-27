from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf Node must have a value")

        if not self.tag:
            return self.value

        return f"<{self.tag}{f" {self.props_to_html()}" if self.props else ""}>{self.value}</{self.tag}>"
