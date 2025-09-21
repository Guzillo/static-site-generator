import os
import shutil
import markdown


def main():
    markdown.copy_files("static", "public")
    markdown.generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
