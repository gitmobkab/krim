import unittest

from textnode import TextNode,TextType
from split import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)

INPUT_TYPE = tuple[
    list[TextNode], str, TextType
]

TEST_CASE = tuple[INPUT_TYPE, list[TextNode]]

TEST_NODE_SPLIT_DEMILIMITER_CASES: list[TEST_CASE] = [
    (
        (
            [TextNode("This is text with a `code block` word", TextType.TEXT)],
            "`",
            TextType.CODE
        ),
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
    ),
    (
        (
            [TextNode("This is quite a bold tone, sir!", TextType.BOLD)],
            "`",
            TextType.ITALIC
        ),
        [TextNode("This is quite a bold tone, sir!", TextType.BOLD)]
    ),
    (
        (
            [
                TextNode("This is text with a **bold** word", TextType.TEXT),
                TextNode("China town and oopsie!?", TextType.ITALIC),
                TextNode("**My bad**, i `think jared` is **DownStairs™**", TextType.TEXT),
                TextNode("**some`advanced`gibberish**", TextType.TEXT),
            ],
            "**",
            TextType.BOLD
        ),
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("China town and oopsie!?", TextType.ITALIC),
            TextNode("My bad", TextType.BOLD),
            TextNode(", i `think jared` is ", TextType.TEXT),
            TextNode("DownStairs™", TextType.BOLD),
            TextNode("some`advanced`gibberish", TextType.BOLD),
        ]
    ),
]

LINK_TESTS = [
    (
        [TextNode("Hello world", TextType.TEXT)],
        [TextNode("Hello world", TextType.TEXT)],
    ),
    (
        [TextNode("Visit [Google](https://google.com)", TextType.TEXT)],
        [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        [TextNode("[Google](https://google.com) is great", TextType.TEXT)],
        [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" is great", TextType.TEXT),
        ],
    ),
    (
        [TextNode("[Google](https://google.com)", TextType.TEXT)],
        [
            TextNode("Google", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        [TextNode("A [Google](https://google.com) B [GitHub](https://github.com)", TextType.TEXT)],
        [
            TextNode("A ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" B ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ],
    ),
    (
        [TextNode("[A](a)[B](b)", TextType.TEXT)],
        [
            TextNode("A", TextType.LINK, "a"),
            TextNode("B", TextType.LINK, "b"),
        ],
    ),
    (
        [TextNode("foo[A](a)bar", TextType.TEXT)],
        [
            TextNode("foo", TextType.TEXT),
            TextNode("A", TextType.LINK, "a"),
            TextNode("bar", TextType.TEXT),
        ],
    ),
    (
        [TextNode("", TextType.TEXT)],
        [
            TextNode("", TextType.TEXT),
        ],
    ),
    (
        [TextNode("Already link", TextType.LINK, "https://google.com")],
        [
            TextNode("Already link", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        [
            TextNode("Hello ", TextType.TEXT),
            TextNode("[Google](https://google.com)", TextType.TEXT),
        ],
        [
            TextNode("Hello ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        [TextNode("[Search](https://google.com?q=test&lang=en)", TextType.TEXT)],
        [
            TextNode("Search", TextType.LINK, "https://google.com?q=test&lang=en"),
        ],
    ),
    (
        [TextNode("Start [A](a), middle [B](b), end [C](c).", TextType.TEXT)],
        [
            TextNode("Start ", TextType.TEXT),
            TextNode("A", TextType.LINK, "a"),
            TextNode(", middle ", TextType.TEXT),
            TextNode("B", TextType.LINK, "b"),
            TextNode(", end ", TextType.TEXT),
            TextNode("C", TextType.LINK, "c"),
            TextNode(".", TextType.TEXT),
        ],
    ),
    (
        [TextNode("  [Google](url)  ", TextType.TEXT)],
        [
            TextNode("  ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "url"),
            TextNode("  ", TextType.TEXT),
        ],
    ),
]

IMAGE_TESTS = [
    (
        [TextNode("Hello world", TextType.TEXT)],
        [TextNode("Hello world", TextType.TEXT)],
    ),
    (
        [TextNode("Look at ![cat](https://example.com/cat.png)", TextType.TEXT)],
        [
            TextNode("Look at ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ],
    ),
    (
        [TextNode("![cat](https://example.com/cat.png) is cute", TextType.TEXT)],
        [
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode(" is cute", TextType.TEXT),
        ],
    ),
    (
        [TextNode("Look at ![cat](https://example.com/cat.png)", TextType.TEXT)],
        [
            TextNode("Look at ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ],
    ),
    (
        [TextNode("![cat](https://example.com/cat.png)", TextType.TEXT)],
        [
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ],
    ),
    (
        [
            TextNode(
                "A ![cat](https://example.com/cat.png) B ![dog](https://example.com/dog.jpg)",
                TextType.TEXT,
            )
        ],
        [
            TextNode("A ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode(" B ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "https://example.com/dog.jpg"),
        ],
    ),
    (
        [TextNode("![A](a.png)![B](b.png)", TextType.TEXT)],
        [
            TextNode("A", TextType.IMAGE, "a.png"),
            TextNode("B", TextType.IMAGE, "b.png"),
        ],
    ),
    (
        [TextNode("foo![A](a.png)bar", TextType.TEXT)],
        [
            TextNode("foo", TextType.TEXT),
            TextNode("A", TextType.IMAGE, "a.png"),
            TextNode("bar", TextType.TEXT),
        ],
    ),
    (
        [TextNode("", TextType.TEXT)],
        [
            TextNode("", TextType.TEXT),
        ],
    ),
    (
        [TextNode("Already image", TextType.IMAGE, "https://example.com/image.png")],
        [
            TextNode("Already image", TextType.IMAGE, "https://example.com/image.png"),
        ],
    ),
    (
        [
            TextNode("Hello ", TextType.TEXT),
            TextNode("![cat](https://example.com/cat.png)", TextType.TEXT),
        ],
        [
            TextNode("Hello ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ],
    ),
    (
        [
            TextNode(
                "Start ![A](a.png), middle ![B](b.png), end ![C](c.png).",
                TextType.TEXT,
            )
        ],
        [
            TextNode("Start ", TextType.TEXT),
            TextNode("A", TextType.IMAGE, "a.png"),
            TextNode(", middle ", TextType.TEXT),
            TextNode("B", TextType.IMAGE, "b.png"),
            TextNode(", end ", TextType.TEXT),
            TextNode("C", TextType.IMAGE, "c.png"),
            TextNode(".", TextType.TEXT),
        ],
    ),
    (
        [TextNode("  ![cat](cat.png)  ", TextType.TEXT)],
        [
            TextNode("  ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode("  ", TextType.TEXT),
        ],
    ),
]

TEXT_TO_TEXTNODES_TESTS = [
    (
        "Hello world",
        [
            TextNode("Hello world", TextType.TEXT),
        ],
    ),
    (
        "**bold**",
        [
            TextNode("bold", TextType.BOLD),
        ],
    ),
    (
        "_italic_",
        [
            TextNode("italic", TextType.ITALIC),
        ],
    ),
    (
        "`code`",
        [
            TextNode("code", TextType.CODE),
        ],
    ),
    (
        "![cat](cat.png)",
        [
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ],
    ),
    (
        "[Google](https://google.com)",
        [
            TextNode("Google", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        "This is **bold** text",
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ],
    ),
    (
        "This is _italic_ text",
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ],
    ),
    (
        "This is `code` text",
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ],
    ),
    (
        "This is ![cat](cat.png)",
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ],
    ),
    (
        "This is [Google](https://google.com)",
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        "**bold** _italic_ `code`",
        [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ],
    ),
    (
        "**bold** ![cat](cat.png) [Google](https://google.com)",
        [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ],
    ),
    (
        "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
    ),
]

class TestSplit(unittest.TestCase):
    
    def test_nodes_split_delimiter(self):
        for test in TEST_NODE_SPLIT_DEMILIMITER_CASES:
            args, expected = test
            self.assertListEqual(split_nodes_delimiter(*args), expected)
            
    def test_split_links(self):
        for test in LINK_TESTS:
            args, expected = test
            self.assertListEqual(split_nodes_link(args), expected)
            
    def test_split_images(self):
        for test in IMAGE_TESTS:
            args, expected = test
            self.assertListEqual(split_nodes_image(args), expected)
            
    def test_text_to_textnodes(self):
        for test in TEXT_TO_TEXTNODES_TESTS:
            args, expected = test
            self.assertListEqual(text_to_textnodes(args), expected)
            