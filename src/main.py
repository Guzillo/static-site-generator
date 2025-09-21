import os
import shutil
import markdown
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1 and sys.argv[1] != "":
        basepath = sys.argv[1]

    markdown.copy_files("static", "docs")
    markdown.generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
