
class HTMLNode:
    
    def __init__(
        self, 
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        
        str_out = ""
        for key, value in self.props.items():
            str_out += f' {key}="{value}"'
        return str_out
    
    def __repr__(self) -> str:
        out = f"HTMLNode<{self.tag=}, {self.value=}, {self.children=}, {self.props=}>"
        return out
    
class LeafNode(HTMLNode):
    
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict | None = None) -> None:
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("HTML: can't represente html leaf node without a value.")

        if not self.tag:
            return self.value    
        html_props = self.props_to_html()
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        out = f"LeafNode<{self.tag=}, {self.value=}, {self.props=}>"
        return out

class ParentNode(HTMLNode):
    
    def __init__(self, tag: str | None = None, children: list | None = None, props: dict | None = None) -> None:
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML: cannot represent parent node without a tag.")
        
        if self.children is None:
            raise ValueError("HTML: parent node must have childrens nodes.")
        
        childrens_html = ""
        for child in self.children:
            childrens_html += child.to_html()
        
        html_props = self.props_to_html()
        return f"<{self.tag}{html_props}>{childrens_html}</{self.tag}>"
    
    def __repr__(self) -> str:
        out = f"ParentNode<{self.tag=}, {self.children=}, {self.props=}>"
        return out
