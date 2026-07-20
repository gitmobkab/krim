
from markdown_extractor import markdown_to_blocks
from split import text_to_textnodes
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node
from blocknode import get_block_type, BlockType


def lists_items_to_nodes(links: str, linksAreInOrder: bool = False) -> list[ParentNode]:
    nodes: list[ParentNode] = []
    for i, link in enumerate(links.split("\n"), 1):
        pattern = f"{i}. " if linksAreInOrder else "- "
        content = link.lstrip(pattern)
        node = ParentNode("li", text_to_children(content))
        nodes.append(node)
    return nodes

def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]
    

def get_block_header_tag(block: str) -> str:
    """take a string, strips all the '#' chars at the star and return the header tag based on the number of '#'
    this function assume that the heading does not contain an illegal number of #.
    
    however if the computed tag level is out of the [1, 6] it will raise a ValueError.

    Args:
        block (str): the heading

    Raises:
        ValueError: if the computed header_level is out of range [1, 6]

    Returns:
        str: the html header tag associated with it
    """
    
    header_content = block.lstrip("#")
    header_level = len(block) - len(header_content)
    if header_level not in range(1,7):
        raise ValueError(f"HTML: header is out of range [1, 6], got {header_level}")
    return f"h{header_level}"
    

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes: list[ParentNode] = [] 
    for block in blocks:
        type = get_block_type(block)
        node = block_to_parent_node(block, type)
        nodes.append(node)
    return ParentNode("div", nodes)
        
def block_to_parent_node(block: str, type: BlockType) -> ParentNode:
    match type:
        case BlockType.HEADING:
            tag = get_block_header_tag(block)
            content = block.lstrip("#")
            content = content.strip()
            return ParentNode(tag, text_to_children(content))
        case BlockType.MULTI_CODE:
            content = block.lstrip("```\n")
            content = content.rstrip("```")
            code_tag = LeafNode("code", content)
            return ParentNode("pre", [code_tag])
        case BlockType.QUOTE:
            paragraphs: list[ParentNode] = []
            for line in block.splitlines():
                raw = line.removeprefix(">").lstrip()
                paragraph = render_paragraph_node(raw)
                paragraphs.append(paragraph)
            return ParentNode("blockquote", paragraphs)
        case BlockType.UNORDERED_LIST:
            links_nodes = lists_items_to_nodes(block)
            return ParentNode("ul", links_nodes)
        case BlockType.ORDERED_LIST:
            links_nodes = lists_items_to_nodes(block, True)
            return ParentNode("ol", links_nodes)            
        case BlockType.PARAGRAPH:
            content = block.replace("\n", " ")
            return ParentNode("p", text_to_children(content))
        case _:
            raise ValueError(f"Unknown BlockType: {type!r}")

def render_paragraph_node(block: str) -> ParentNode:
    content = block.replace("\n", " ")
    return ParentNode("p", text_to_children(content))
        