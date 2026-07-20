from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    MULTI_CODE = "multi_code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def get_block_type(block: str) -> BlockType:
    lines = block.splitlines()
    if re.match(r"^(#{1,6}) (.*)$", block):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.MULTI_CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^(\d+?\.) ", line) for line in lines):
        orderIsValid = True
        for i, line in enumerate(lines, start=1):
            if int(line[0]) != i:
                orderIsValid = False
        if orderIsValid:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH