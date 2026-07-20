import unittest

from utils import extract_title

EXTRACT_TITLE_TESTS = [
    (
        "# Hello",
        "Hello"
    ),
    (
        "\n\n\n# **Not every, day**",
        "**Not every, day**"
    ),
    (
        "\t#Granted, desire",
        "Granted, desire"
    ),
]


class TestUtils(unittest.TestCase):
    
    def test_extract_title(self):
        for md, expected in EXTRACT_TITLE_TESTS:
            with self.subTest(md):
                self.assertEqual(extract_title(md), expected)