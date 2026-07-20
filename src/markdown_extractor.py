from typing import Callable
import re


ExtractionResult = list[tuple[str, str]]
Extractor = Callable[[str], ExtractionResult]

def extract_markdown_images(text: str) -> ExtractionResult:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> ExtractionResult:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    for block in markdown.split("\n\n"):
        stripped_block = block.strip()
        if stripped_block:
            blocks.append(stripped_block)
    return blocks        
        