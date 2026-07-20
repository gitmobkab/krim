from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links, Extractor


def text_to_textnodes(text: str) -> list[TextNode]:
    text_node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    bold_and_italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    bold_italic_code_block_nodes = split_nodes_delimiter(bold_and_italic_nodes, "`", TextType.CODE)
    bold_italic_code_block_images_nodes = split_nodes_image(bold_italic_code_block_nodes)
    return split_nodes_link(bold_italic_code_block_images_nodes)
    

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes : list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            nodes = split_node_with_extractor(old_node,TextType.LINK , extract_markdown_links, "[%1](%2)")
            new_nodes.extend(nodes)
    return new_nodes
    

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes : list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            nodes = split_node_with_extractor(old_node, TextType.IMAGE, extract_markdown_images, "![%1](%2)")
            new_nodes.extend(nodes)
    return new_nodes
        

def split_node_with_extractor(old_node: TextNode, text_type: TextType, extractor: Extractor, pattern: str) -> list[TextNode]:
    """the demon of complexity.
    
    this basically abstract the extraction of images and links in old_node
    

    Args:
        old_node (TextNode): the node to extract images or links from.
        text_type (TextType): well you know what it is. i think...
        extractor (Extractor): the extractor charges of extracting the links/images
        pattern (str): the pattern for order resolution. links = \\[%1](%2). images = !\\[%1](%2)

    Returns:
        list[TextNode]: the computed new nodes (i think).
    """
    
    if old_node.text_type is not TextType.TEXT:
        return [old_node]
    nodes: list[TextNode] = []
    content = old_node.text
    extraction_result = extractor(content)
    if not extraction_result:
        return [old_node]
    remaining = content
    for result in extraction_result:
        alt_text, url = result
        delimiter = pattern.replace("%1", alt_text, 1)
        delimiter = delimiter.replace("%2", url, 1)
        parts = remaining.split(delimiter, 1)
        before = parts[0]
        after = parts[1]
        if before:
            nodes.append(
                TextNode(before, TextType.TEXT)
            )
        nodes.append(
            TextNode(alt_text, text_type, url)
            )
        remaining = after
    if remaining:
        nodes.append(
            TextNode(remaining, TextType.TEXT)
        )
    return nodes
    


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            nodes = split_node_delimiter(old_node, delimiter, text_type)
            new_nodes.extend(nodes)
    return new_nodes
    
def split_node_delimiter(old_node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    if old_node.text_type is not TextType.TEXT:
        return [old_node]
    delimited_parts = old_node.text.split(delimiter)
    
    if len(delimited_parts) % 2 == 0:
        raise Exception(f"MARKDOWN: missing closing delimiter {delimiter!r}")
    
    new_nodes: list[TextNode] = []
    
    for i, part in enumerate(delimited_parts):
        if not part:
            continue
        if i % 2 == 0:
            new_nodes.append(TextNode(part, TextType.TEXT))
        else:
            new_nodes.append(TextNode(part, text_type))
    return new_nodes