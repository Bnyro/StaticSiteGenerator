#!/usr/bin/python

import os
import yaml
import shutil
import markdown

from obj import Page

SOURCE_DIR_NAME = "docs"
TARGET_DIR_NAME = "html"

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

def create_output_file(file_name):
    full_path = os.path.join(SOURCE_DIR_NAME, file_name)
    html_file_name = file_name.replace(".md", ".html")
    target_file = os.path.join(
        TARGET_DIR_NAME,
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

    for file_name in os.listdir(TARGET_DIR_NAME):
        path = os.path.join(TARGET_DIR_NAME, file_name)
        if os.path.isfile(path):
            with open(path, "r") as infile:
                text = infile.read().replace("{{navlinks}}", nav_html)
            with open(path, "w") as outfile:
                outfile.write(text)

with open('template.html') as infile:
    template = infile.read()

target_dir = os.path.join(TARGET_DIR_NAME)
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

for file_name in os.listdir(SOURCE_DIR_NAME):
    create_output_file(file_name)

create_nav_links(pages)

assets_dir = os.path.join(target_dir, "assets")
if (os.path.exists(assets_dir)):
    shutil.rmtree(assets_dir)
shutil.copytree('assets', assets_dir)