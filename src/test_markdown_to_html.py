import unittest
from markdown_to_html import markdown_to_html_node

tests = [
    (
        "# Heading",
        "<div><h1>Heading</h1></div>",
    ),
    (
        "## Heading 2",
        "<div><h2>Heading 2</h2></div>",
    ),
    (
        "### Heading 3",
        "<div><h3>Heading 3</h3></div>",
    ),
    (
        "> Quote",
        "<div><blockquote><p>Quote</p></blockquote></div>",
    ),
    (
        "> First line\n> Second line",
        "<div><blockquote><p>First line</p><p>Second line</p></blockquote></div>",
    ),
    (
        "- Apple\n- Banana\n- Orange",
        "<div><ul><li>Apple</li><li>Banana</li><li>Orange</li></ul></div>",
    ),
    (
        "**bold**",
        "<div><p><b>bold</b></p></div>",
    ),
    (
        "_italic_",
        "<div><p><i>italic</i></p></div>",
    ),
    (
        "`code`",
        "<div><p><code>code</code></p></div>",
    ),
    (
        "![alt](img.png)",
        '<div><p><img src="img.png" alt="alt"></img></p></div>',
    ),
    (
        "[Boot.dev](https://boot.dev)",
        '<div><p><a href="https://boot.dev">Boot.dev</a></p></div>',
    ),
    (
        "**bold** _italic_ `code`",
        "<div><p><b>bold</b> <i>italic</i> <code>code</code></p></div>",
    ),
    (
        "# **Bold Heading**",
        "<div><h1><b>Bold Heading</b></h1></div>",
    ),
    (
        "> Quote with **bold** and _italic_",
        "<div><blockquote><p>Quote with <b>bold</b> and <i>italic</i></p></blockquote></div>",
    ),
    (
        "- **Apple**\n- _Banana_\n- `Orange`",
        "<div><ul><li><b>Apple</b></li><li><i>Banana</i></li><li><code>Orange</code></li></ul></div>",
    ),
    (
        "1. **One**\n2. _Two_\n3. `Three`",
        "<div><ol><li><b>One</b></li><li><i>Two</i></li><li><code>Three</code></li></ol></div>",
    ),
    (
        "# Heading\n\nParagraph",
        "<div><h1>Heading</h1><p>Paragraph</p></div>",
    ),
    (
        "Paragraph\n\n- One\n- Two",
        "<div><p>Paragraph</p><ul><li>One</li><li>Two</li></ul></div>",
    ),
    (
        "> Quote\n\n```\ncode\n```",
        "<div><blockquote><p>Quote</p></blockquote><pre><code>code\n</code></pre></div>",
    ),
    (
        "# Heading\n\n> Quote\n\n- Item\n\n1. Number",
        "<div><h1>Heading</h1><blockquote><p>Quote</p></blockquote><ul><li>Item</li></ul><ol><li>Number</li></ol></div>",
    ),
]

class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_markdown_to_html_node(self):
        for md, expected in tests:
            with self.subTest(markdown=md):
                node = markdown_to_html_node(md)
                self.assertEqual(node.to_html(), expected)
