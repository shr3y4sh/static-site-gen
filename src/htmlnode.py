class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        buffer = []
        for k, v in self.props.items():
            buffer.append(f'{k}="{v}"')

        return " ".join(buffer)

    def __repr__(self):
        buffer = f'HTMLNode (tag=<{self.tag}>\n \t value="{self.value}"'

        if self.children:
            children_tags = list(map(lambda x: x.tag, self.children))
            buffer += f"\n\t children={children_tags}"

        if self.props:
            buffer += f"\n\t props={{{self.props_to_html()}}}"

        return buffer + ")"
