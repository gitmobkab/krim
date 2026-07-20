from utils import generate_pages_recursive, copy_dir

def main() -> None:
    copy_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    
    
    
    
if __name__ == "__main__":
    main()