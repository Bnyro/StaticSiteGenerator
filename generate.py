#!/usr/bin/python

import os
import yaml
import markdown

sourceDirName = "docs"
targetDirName = "html"

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

def createOutputFile(file):
    fullpath = os.path.join(sourceDirName, file)
    content = getFileContent(fullpath)
    html = renderHTML(content, template)
    targetFile = os.path.join(
        targetDirName,
        file.replace(".md", ".html")
    )
    with open(targetFile, 'w') as outfile:
        outfile.write(html)

with open('template.html') as infile:
    template = infile.read()

targetDir = os.path.join(targetDirName)
if not os.path.exists(targetDir):
    os.mkdir(targetDir)

for file in os.listdir(sourceDirName):
    createOutputFile(file)