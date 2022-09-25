#!/usr/bin/python

import os
import yaml
import markdown

from obj import Page

sourceDirName = "docs"
targetDirName = "html"
pages = []

def getFileContent(filePath):
    with open(filePath) as infile:

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

def renderHTML(yaml, template) -> str:
    for item in yaml:
        template = template.replace("{{" + item + "}}", str(yaml[item]))
    return template

def createOutputFile(fileName):
    fullpath = os.path.join(sourceDirName, fileName)
    htmlFileName = fileName.replace(".md", ".html")
    targetFile = os.path.join(
        targetDirName,
        htmlFileName
    )

    content = getFileContent(fullpath)
    pages.append(
        Page(
            content["title"],
            htmlFileName
        )
    )

    html = renderHTML(content, template)
    with open(targetFile, 'w') as outfile:
        outfile.write(html)

def createNavLinks(pages):
    navHtml = ""
    for page in pages:
        navHtml += f"<li><a href={page.location}>{page.title}</a></li>\n"

    for fileName in os.listdir(targetDirName):
        path = os.path.join(targetDirName, fileName)
        with open(path, "r") as infile:
            text = infile.read().replace("{{navlinks}}", navHtml)
        with open(path, "w") as outfile:
            outfile.write(text)

with open('template.html') as infile:
    template = infile.read()

targetDir = os.path.join(targetDirName)
if not os.path.exists(targetDir):
    os.mkdir(targetDir)

for file in os.listdir(sourceDirName):
    createOutputFile(file)

createNavLinks(pages)