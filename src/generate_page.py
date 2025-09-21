from markdown import markdown_to_html_node, extract_title
import os


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = None
    template_content = None
    with open(from_path) as f:
        md_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    if template_content is None:
        raise Exception("Template is absent")
    markdown_html = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", markdown_html)
    template_content = template_content.replace('href="/', f'href="{basepath}/')
    template_content = template_content.replace('src="/', f'src="{basepath}/')

    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with open(dest_path, "w") as f:
        f.write(template_content)
