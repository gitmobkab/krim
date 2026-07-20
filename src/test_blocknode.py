import unittest

from blocknode import BlockType, get_block_type

TESTS = [
    # Paragraphs
    (
        "Hello world",
        BlockType.PARAGRAPH,
    ),
    (
        "This is a paragraph with multiple words.",
        BlockType.PARAGRAPH,
    ),
    (
        "This is a paragraph\nthat spans multiple lines.",
        BlockType.PARAGRAPH,
    ),

    # Headings
    (
        "# Heading",
        BlockType.HEADING,
    ),
    (
        "## Heading",
        BlockType.HEADING,
    ),
    (
        "### Heading",
        BlockType.HEADING,
    ),
    (
        "#### Heading",
        BlockType.HEADING,
    ),
    (
        "##### Heading",
        BlockType.HEADING,
    ),
    (
        "###### Heading",
        BlockType.HEADING,
    ),

    # Code blocks
    (
        "```\nprint('Hello')\n```",
        BlockType.MULTI_CODE,
    ),
    (
        "```\nline 1\nline 2\nline 3\n```",
        BlockType.MULTI_CODE,
    ),

    # Quotes
    (
        "> Quote",
        BlockType.QUOTE,
    ),
    (
        "> Quote\n> Second line",
        BlockType.QUOTE,
    ),
    (
        "> First\n> Second\n> Third",
        BlockType.QUOTE,
    ),

    # Unordered lists
    (
        "- Item",
        BlockType.UNORDERED_LIST,
    ),
    (
        "- Item 1\n- Item 2",
        BlockType.UNORDERED_LIST,
    ),
    (
        "- Apples\n- Bananas\n- Oranges",
        BlockType.UNORDERED_LIST,
    ),

    # Ordered lists
    (
        "1. First",
        BlockType.ORDERED_LIST,
    ),
    (
        "1. First\n2. Second",
        BlockType.ORDERED_LIST,
    ),
    (
        "1. First\n2. Second\n3. Third",
        BlockType.ORDERED_LIST,
    ),
    
    # invalid ordered lists
    (
        "1. One\n3. Two\n2. Three",
        BlockType.PARAGRAPH,
    ),
    (
        "2. Two\n3. Three",
        BlockType.PARAGRAPH,
    ),
    # Edge cases that should still be paragraphs
    (
        "#Not a heading",
        BlockType.PARAGRAPH,
    ),
    (
        "-Not a list",
        BlockType.PARAGRAPH,
    ),
    (
        "1.Not a list",
        BlockType.PARAGRAPH,
    ),
    (
        "```not closed",
        BlockType.PARAGRAPH,
    ),
    (
        "####### Too many hashes",
        BlockType.PARAGRAPH,
    ),
]

class TestBlockNode(unittest.TestCase):
    
    def test_block_to_block_type(self):
        for block, expected in TESTS:
            with self.subTest(block):
                self.assertEqual(get_block_type(block), expected)