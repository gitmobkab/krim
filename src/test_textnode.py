import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("claude's plan", TextType.BOLD)
        node2 = TextNode("claude's plan", TextType.ITALIC)
        
        self.assertNotEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("claude's plan", TextType.LINK, "https://claude.ai/u/self.png")
        node2 = TextNode("claude's plan", TextType.LINK, "https://claude.ai/u/are_u_dumb.png")
        
        self.assertNotEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()