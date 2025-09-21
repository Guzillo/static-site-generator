import os
import shutil
import markdown


def main():
    markdown.copy_files("static", "public")
    markdown.generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
