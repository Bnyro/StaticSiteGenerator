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
    if info is not None:
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


def render_html(template, content, config, nav_html) -> str:
    """
    Replace all the keys in the dict object with their values inside the template
    :param info: Dict object containing the source configuration
    :param template: The HTML template whose content should be rendered
    :return The rendered HTML as string
    """
    template = replace_by_key(template, content)
    template = replace_by_key(template, config)
    template = template.replace("{{navlinks}}", nav_html)

    return template

def create_output_file(page: Page, template: str, config: dict, nav_html: str):
    """
    Generate an output file by reading the markdown file and rendering it into the template
    :param file_name: The name or relative path of the source file
    :param template: The HTML template to use as base
    :param config: The projects config
    :return The generated [Page] object
    """
    target_file_name = page.location.replace(".md", ".html")
    target_file = target_file_name

    html = render_html(template, page.content, config, nav_html)

    with open(target_file, 'w') as outfile:
        outfile.write(html)

def get_nav_html(pages) -> str:
    """
    Insert the navigation links inside the file
    :param pages: A list of the [Page] class
    :return The html to be inserted for the navbar
    """
    nav_html = ""
    for page in pages:
        location = page.location.replace(f"{TARGET_DIR_PATH}/", "")
        nav_html += f"<a href={location}><li>{page.title}</li></a>\n"
        if page.children is not None:
            nav_html += "<ol>\n" + get_nav_html(page.children) + "<ol>\n"
        # nav_html += "</li>"

    return nav_html

def get_target_file_path(path: str) -> str:
    """
    Convert the source path to a target path
    """
    path = path.replace(".md", ".html")
    return path.replace(SOURCE_DIR_PATH, TARGET_DIR_PATH)

def index_pages(base_path: str) -> list:
    """
    Indexes all pages for use as navigation list
    :returns A list of the indexed pages
    """
    pages = []
    for f in os.scandir(base_path):
        if f.is_file():
            pages.append(
                Page(
                    "title",
                    get_target_file_path(f.path),
                    get_file_content(f.path)
                )
            )
        elif f.is_dir():
            pages.append(
                Page(
                    "subdir",
                    get_target_file_path(f.path),
                    None,
                    index_pages(f.path)
                )
            )
    
    return pages

def create_pages(pages, template: str, config: dict, nav_html: str):
    for page in pages:
        if page.content is not None:
            create_output_file(page, template, config, nav_html)
        else:
            if not os.path.exists(page.location):
                os.mkdir(page.location)
            create_pages(page.children, template, config, nav_html)


def generate():
    if (os.path.exists(TARGET_DIR_PATH)):
        shutil.rmtree(TARGET_DIR_PATH)
    os.mkdir(TARGET_DIR_PATH)
    
    with open(TEMPLATE_FILE_PATH) as infile:
        template = infile.read()    

    with open(CONFIG_PATH, "r") as infile:
        config = json.load(infile)   

    pages = index_pages(SOURCE_DIR_PATH)
    nav_html = get_nav_html(pages)
    
    create_pages(pages, template, config, nav_html)

    shutil.copytree(
        SOURCE_ASSETS_PATH,
        os.path.join(
            TARGET_DIR_PATH,
            SOURCE_ASSETS_PATH
        )
    )

generate()