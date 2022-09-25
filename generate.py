#!/usr/bin/python

import yaml
import markdown

def getFileContent():
    with open('docs/index.md') as infile:

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

    info = yaml.load(ym, yaml.SafeLoader)
    content = markdown.markdown(md)
    info['content'] = content

    return info

def renderHTML(yaml, template) -> str:
    for item in yaml:
        template = template.replace("{{" + item + "}}", str(yaml[item]))
    return template

with open('template.html') as infile:
    template = infile.read()

html = renderHTML(getFileContent(), template)
print(html)

# with open('output.html', 'w') as outfile:
    # outfile.write(html)