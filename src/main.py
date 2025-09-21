import os
import shutil
import markdown


def main():
    markdown.copy_files("static", "public")


if __name__ == "__main__":
    main()
