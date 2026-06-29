import unittest
from textnode import TextNode, TextType
import inline_markdown
 
 
class TestInlineMarkdown(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )
 
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )
 
    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )
 
    def test_split_multiple(self):
        node = TextNode("`one` and `two`", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("one", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.CODE),
            ],
        )
 
    def test_non_text_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])
 
    def test_no_closing_delimiter_raises(self):
        node = TextNode("This is `broken markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
 
    def test_extract_markdown_images(self):
        matches = inline_markdown.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
 
    def test_extract_multiple_images(self):
        matches = inline_markdown.extract_markdown_images(
            "![rick](https://i.imgur.com/aKaOqIh.gif) and ![obi](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )
 
    def test_extract_markdown_links(self):
        matches = inline_markdown.extract_markdown_links(
            "This is a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
 
    def test_extract_links_not_images(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        self.assertListEqual(
            [("link", "https://example.com")],
            inline_markdown.extract_markdown_links(text),
        )
 
    def test_extract_images_not_links(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        self.assertListEqual(
            [("image", "https://example.com/img.png")],
            inline_markdown.extract_markdown_images(text),
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![first](https://example.com/1.png) then text",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" then text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode("Just plain text with no images", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Just plain text with no images", TextType.TEXT)],
            new_nodes,
        )

    def test_split_image_non_text_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = inline_markdown.split_nodes_image([node])
        self.assertListEqual([TextNode("already bold", TextType.BOLD)], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_ignores_images(self):
        node = TextNode(
            "An ![image](https://example.com/img.png) and a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("An ![image](https://example.com/img.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = inline_markdown.text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain(self):
        nodes = inline_markdown.text_to_textnodes("Just plain text")
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            nodes,
        )
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = inline_markdown.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
 
    def test_markdown_to_blocks_excessive_newlines(self):
        md = "First block\n\n\n\nSecond block"
        blocks = inline_markdown.markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])
 
    def test_markdown_to_blocks_empty(self):
        self.assertEqual(inline_markdown.markdown_to_blocks(""), [])
 
    def test_markdown_to_blocks_single(self):
        md = "Just one block of text"
        blocks = inline_markdown.markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block of text"])
    
    def test_block_type_paragraph(self):
        block = "This is a normal paragraph with some text."
        self.assertEqual(inline_markdown.block_to_block_type(block), inline_markdown.BlockType.PARAGRAPH)

    def test_block_type_heading(self):
        self.assertEqual(inline_markdown.block_to_block_type("# Heading 1"), inline_markdown.BlockType.HEADING)
        self.assertEqual(inline_markdown.block_to_block_type("###### Heading 6"), inline_markdown.BlockType.HEADING)

    def test_block_type_heading_too_many(self):
        self.assertEqual(inline_markdown.block_to_block_type("####### Not a heading"), inline_markdown.BlockType.PARAGRAPH)

    def test_block_type_code(self):
        block = "```\ncode goes here\n```"
        self.assertEqual(inline_markdown.block_to_block_type(block), inline_markdown.BlockType.CODE)

    def test_block_type_quote(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(inline_markdown.block_to_block_type(block), inline_markdown.BlockType.QUOTE)

    def test_block_type_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(inline_markdown.block_to_block_type(block), inline_markdown.BlockType.UNORDERED_LIST)

    def test_block_type_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(inline_markdown.block_to_block_type(block), inline_markdown.BlockType.ORDERED_LIST)

    def test_block_type_ordered_list_bad_numbering(self):
        block = "1. first\n3. third\n2. second"
        self.assertEqual(inline_markdown.block_to_block_type(block), inline_markdown.BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = "This is **bolded** paragraph text in a p tag here"
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**
"""
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with multiple lines
"""
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first item
- second **bold** item
- third item
"""
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second <b>bold</b> item</li><li>third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second _italic_ item
3. third item
"""
        node = inline_markdown.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second <i>italic</i> item</li><li>third item</li></ol></div>",
        )

    def test_extract_title(self):
        self.assertEqual(inline_markdown.extract_title("# Hello"), "Hello")

    def test_extract_title_with_whitespace(self):
        self.assertEqual(inline_markdown.extract_title("#    Padded Title    "), "Padded Title")

    def test_extract_title_among_lines(self):
        md = "Some intro\n# The Title\nmore text"
        self.assertEqual(inline_markdown.extract_title(md), "The Title")

    def test_extract_title_no_h1_raises(self):
        with self.assertRaises(ValueError):
            inline_markdown.extract_title("## Only an h2\nno h1 here")
    
    def test_extract_title_ignores_h2(self):
        md = "## Subheading\n# Real Title"
        self.assertEqual(inline_markdown.extract_title(md), "Real Title")



if __name__ == "__main__":
    unittest.main()
 
 