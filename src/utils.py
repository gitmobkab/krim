import os
import shutil
import rich

from markdown_to_html import get_block_header_tag, markdown_to_html_node


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if not os.path.isfile(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)
        else:
            filename, ext = os.path.splitext(entry)
            if ext != ".md":
                rich.print(f"[yellow]Warning: {from_path!r} is not an .md file, skipped.")
                continue
            target_file = filename + ".html" 
            dest_path = os.path.join(dest_dir_path, target_file)
            generate_page(from_path, template_path, dest_path)
            

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    rich.print(f"Generating page from {from_path!r} to {dest_path!r} using template {template_path!r}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    html_content = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    page_with_title = template.replace("{{ Title }}", page_title)
    full_html = page_with_title.replace("{{ Content }}", html_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(full_html)


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            continue # ignore the empty lines at the start of the doc
        if not stripped.startswith("#"):
            raise Exception("Markdown: Expected first line to start with '#'")
        header_tag = get_block_header_tag(stripped)
        if header_tag != "h1":
            level = int(header_tag[1:])
            header_repr = "#" * level
            header_repr = f"({header_repr} Header)"
            raise Exception(f"Expected title to use <h1> (# Header), got header of type <{header_tag}> {header_repr}")
        return stripped.lstrip("#").strip()
    raise ValueError("No title found")

def copy_dir(src: str, dest: str) -> None:
    if os.path.exists(dest):
        rich.print(f"Wiping destination folder: {dest!r}")
        shutil.rmtree(dest)
    else:
        rich.print(f"[yellow]Warning: {dest!r} doesn't exist. Creating barebone folder.")
    os.mkdir(dest)
        
    for file in os.listdir(src):
        path_src = os.path.join(src, file)
        path_dest = os.path.join(dest, file)
        if os.path.isfile(path_src):
            rich.print(f"Copying file {path_src!r} to {path_dest!r}")
            shutil.copy(path_src, path_dest)
        else:
            copy_dir(path_src, path_dest)
