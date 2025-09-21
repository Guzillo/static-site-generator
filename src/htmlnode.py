class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        html_props = ""
        props = self.props
        for prop in props:
            html_props += f'{prop}="{self.props[prop]}" '
        return html_props.rstrip()

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf has no value")
        if self.tag is None or self.tag == "":
            return self.value
        if self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, value=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("node has no value")
        if self.children is None:
            raise ValueError("node has no children")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        return f"<{self.tag}>{children_string}</{self.tag}>"
