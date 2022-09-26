#!/usr/bin/python

import os
import yaml
import shutil
import markdown

from obj import Page

SOURCE_DIR_PATH = "docs"
TARGET_DIR_PATH = "html"
TEMPLATE_FILE_PATH = "template.html"
SOURCE_ASSETS_PATH = "static"

pages = []

def get_file_content(file_path):
    with open(file_path) as infile:

        for s in infile:
            if s.startswith('---'):
                break;
        
        yaml_lines = []
        for s in infile:
            if s.startswith('---'):
                break;
            else:
                yaml_lines.append(s)
        
        ym = ''.join(yaml_lines)
        md = ''.join(infile)

    info = yaml.safe_load(ym)
    content = markdown.markdown(md)
    info['content'] = content

    return info

def render_html(info, template) -> str:
    for key in info:
        template = template.replace("{{" + key + "}}", str(info[key]))
    return template

def create_output_file(file_name, template):
    full_path = os.path.join(SOURCE_DIR_PATH, file_name)
    html_file_name = file_name.replace(".md", ".html")
    target_file = os.path.join(
        TARGET_DIR_PATH,
        html_file_name
    )

    content = get_file_content(full_path)
    pages.append(
        Page(
            content["title"],
            html_file_name
        )
    )

    html = render_html(content, template)
    with open(target_file, 'w') as outfile:
        outfile.write(html)

def create_nav_links(pages):
    nav_html = ""
    for page in pages:
        nav_html += f"<li><a href={page.location}>{page.title}</a></li>\n"

    for file_name in os.listdir(TARGET_DIR_PATH):
        path = os.path.join(TARGET_DIR_PATH, file_name)
        if os.path.isfile(path):
            with open(path, "r") as infile:
                text = infile.read().replace("{{navlinks}}", nav_html)
            with open(path, "w") as outfile:
                outfile.write(text)

def generate():
    if (os.path.exists(TARGET_DIR_PATH)):
        shutil.rmtree(TARGET_DIR_PATH)
    os.mkdir(TARGET_DIR_PATH)
    
    with open(TEMPLATE_FILE_PATH) as infile:
        template = infile.read()        

    for file_name in os.listdir(SOURCE_DIR_PATH):
        create_output_file(file_name, template)

    create_nav_links(pages)
    
    shutil.copytree(
        SOURCE_ASSETS_PATH,
        os.path.join(
            TARGET_DIR_PATH,
            SOURCE_ASSETS_PATH
        )
    )

generate()