import unittest
from markdown_extractor import (
    extract_markdown_images, 
    extract_markdown_links,
    markdown_to_blocks
)


IMAGE_TEST_CASES = [
    (
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
    ),
]

LINK_TEST_CASES = [
    (
        "This is text with a [*simple link you can trust*](https://pornhub.com)",
        [("*simple link you can trust*", "https://pornhub.com")]
    ),
    (
        "This is text with a [classic experiment][https://youtube.com](https://pornhub.com)",
        [("https://youtube.com", "https://pornhub.com")]
    ),
]

class TestMarkdownExtractors(unittest.TestCase):
    
    def test_extract_images(self):
        for args, expected in IMAGE_TEST_CASES:
            with self.subTest(args):
                self.assertListEqual(extract_markdown_images(args), expected)
            
    def test_extract_links(self):
        for args, expected in IMAGE_TEST_CASES:
            with self.subTest(args):
                self.assertListEqual(extract_markdown_links(args), expected)

    def test_markdown_to_blocks(self):
        with open("test_files/md_test.md") as file:
            content = file.read()
        self.assertListEqual(
            markdown_to_blocks(content),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
                "**Isn't the view spectacular?** [Yes, babe.](https://youtu.be/xnP7qKxwzjg?si=wc1eShHipqm0ZaZj) | [Heck no!](https://youtu.be/-ed6UeDp1ek?si=LVUmYzaQn7Lpf8_Q)"
            ]
        )