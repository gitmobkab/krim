from sys import argv

from utils import generate_pages_recursive, copy_dir

def main() -> None:
    basepath = "/" if len(argv) < 2 else argv[1]
    copy_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
    
    
    
if __name__ == "__main__":
    main()