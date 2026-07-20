import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

HTML_NODE_TESTS = [
    (
        {
            "href": "https://boot.dev",
            "target": "_blank"
        },
        ' href="https://boot.dev" target="_blank"'
    ),
    (
        {
            "href": "https://boot.dev",
            "target": "_blank",
            "wait": " "
        },
        ' href="https://boot.dev" target="_blank" wait=" "'
    ),
    (
        None,
        ''
    )
]


LEAF_NODE_TESTS = [
    (
        ("p", "Hello, world!"),
        "<p>Hello, world!</p>"
    ),
    (

        ("br <p>", "Hello, world!"),
        "<br <p>>Hello, world!</br <p>>"
    ),
    (
        ("", "Hello, world!"),
        "Hello, world!"
    ),    
]


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        for props, expected in HTML_NODE_TESTS:
            with self.subTest(props):
                node = HTMLNode(props=props)
                self.assertEqual(node.props_to_html(), expected)
            
    def test_leaf_to_html_p(self):
        for args, expected in LEAF_NODE_TESTS:
            with self.subTest(args):
                node = LeafNode(*args)
                self.assertEqual(node.to_html(), expected)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("", "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("", "Normal text"),
            ], 
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode("", "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("", "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
if __name__ == "__main__":
    unittest.main()