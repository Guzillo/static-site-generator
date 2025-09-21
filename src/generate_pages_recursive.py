import os
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        if os.path.isdir(os.path.join(dir_path_content, file)):
            if not os.path.exists(os.path.join(dest_dir_path, file)):
                os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file),
                basepath,
            )
            continue
        one = os.path.join(os.path.abspath(dir_path_content), file)
        two = os.path.join(os.path.abspath(dest_dir_path), file)
        print(f"file:{one} --> file:{two}")
        html_file_name = file[::-1].split(".", 1)[1][::-1] + ".html"
        generate_page(
            os.path.join(os.path.abspath(dir_path_content), file),
            template_path,
            os.path.join(os.path.abspath(dest_dir_path), html_file_name),
            basepath,
        )
