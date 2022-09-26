#!/usr/bin/python

import os
import yaml
import json
import shutil
import markdown

from obj import Page

SOURCE_DIR_PATH = "docs"
TARGET_DIR_PATH = "html"
TEMPLATE_FILE_PATH = "template.html"
SOURCE_ASSETS_PATH = "static"
CONFIG_PATH = "config.json"

def get_file_content(file_path) -> dict:
    """
    Get the content of a properly formatted markdown file
    :param file_path: Path of the markdown file
    :return A dict object containing all the extracted information
    """
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

def replace_by_key(text: str, dict: dict) -> str:
    """
    Replace the keys of a dict with their values inside a text
    :param text: The base text to modify
    :param dict: The dict object containing the fields to replace
    :return The modified text as string
    """
    for key in dict:
        text = text.replace("{{" + key + "}}", str(dict[key]))
    return text


def render_html(template, content, config) -> str:
    """
    Replace all the keys in the dict object with their values inside the template
    :param info: Dict object containing the source configuration
    :param template: The HTML template whose content should be rendered
    :return The rendered HTML as string
    """
    template = replace_by_key(template, content)
    template = replace_by_key(template, config)

    return template

def create_output_file(file_name, template, config) -> Page:
    """
    Generate an output file by reading the markdown file and rendering it into the template
    :param file_name: The name or relative path of the source file
    :param template: The HTML template to use as base
    :param config: The projects config
    :return The generated [Page] object
    """
    full_path = os.path.join(SOURCE_DIR_PATH, file_name)
    target_file_name = file_name.replace(".md", ".html")
    target_file = os.path.join(
        TARGET_DIR_PATH,
        target_file_name
    )

    content = get_file_content(full_path)
    html = render_html(template, content, config)

    with open(target_file, 'w') as outfile:
        outfile.write(html)

    return Page(
            content["title"],
            target_file_name
        )

def create_nav_links(pages):
    """
    Insert the navigation links inside the file
    :param pages: A list of the [Page] class
    """
    nav_html = ""
    for page in pages:
        nav_html += f"<li><a href={page.location}>{page.title}</a></li>\n"

    for file_name in os.listdir(TARGET_DIR_PATH):
        path = os.path.join(TARGET_DIR_PATH, file_name)
        if os.path.isfile(path):
            with open(path, "r") as f:
                text = f.read().replace("{{navlinks}}", nav_html)
                
            with open(path, "w") as f:
                f.write(text)

def generate_index() -> list:
    """
    Indexes all pages for use as navigation list
    :returns A list of the indexed pages
    """
    for file_name in os.listdir(SOURCE_DIR_PATH):
        print(file_name)

def generate():
    if (os.path.exists(TARGET_DIR_PATH)):
        shutil.rmtree(TARGET_DIR_PATH)
    os.mkdir(TARGET_DIR_PATH)
    
    with open(TEMPLATE_FILE_PATH) as infile:
        template = infile.read()    

    with open(CONFIG_PATH, "r") as infile:
        config = json.load(infile)   

    pages = []

    for file_name in os.listdir(SOURCE_DIR_PATH):
        page = create_output_file(file_name, template, config)
        pages.append(page)

    create_nav_links(pages)
    
    shutil.copytree(
        SOURCE_ASSETS_PATH,
        os.path.join(
            TARGET_DIR_PATH,
            SOURCE_ASSETS_PATH
        )
    )

def run_fast_scandir(dir):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        elif f.is_file():
            files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

generate()