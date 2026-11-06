#!/usr/bin/env python3
"""Builds the page-editor artifact file from the repo's current pages.
Usage: python3 tools/build_editor.py OUTPUT.html"""
import re, base64, sys
R = '/home/claude/luzaardo.github.io/'
out = sys.argv[1]
def region(text, a, b):
    m = re.search(re.escape(a) + r'.*?\n(.*?)' + re.escape(b), text, re.S)
    return m.group(1) if m else ''
css = open(R + 'styles.css').read() + '\n' + open(R + 'case.css').read()
css = re.sub(r'url\("?(fonts/[^")]+)"?\)', lambda m: 'url("data:font/woff2;base64,%s")' % base64.b64encode(open(R + m.group(1), 'rb').read()).decode(), css)
css = re.sub(r'url\("?(images/[^")]+)"?\)', lambda m: m.group(0), css)
tpl = open(R + 'tools/editor_template.html').read().replace('/*SITE_CSS*/', css)
def inline_imgs(html):
    def f(m):
        path = R + m.group(1)
        try: return 'src="data:image/webp;base64,%s"' % base64.b64encode(open(path, 'rb').read()).decode()
        except Exception: return m.group(0)
    html = re.sub(r'srcset="[^"]*"', '', html)
    return re.sub(r'src="(images/[^"]+)"', f, html)
for i, name in ((1, 'project-1'), (2, 'project-2')):
    page = open(R + name + '.html').read()
    body = region(page, '<!-- EDITABLE:START', '<!-- EDITABLE:END -->')
    inner = re.search(r'<article class="case-body">\s*(.*?)\s*</article>', body, re.S).group(1)
    also = region(page, '<!-- ALSO:START', '<!-- ALSO:END -->')
    tpl = tpl.replace('<!--P%d-->' % i, inline_imgs(inner) + '</article><p class="home-link"><a href="#" onclick="return false">Back to home</a></p><article hidden>').replace('<!--A%d-->' % i, inline_imgs(also))
open(out, 'w').write(tpl)
print('editor built', len(tpl) // 1024, 'KB')
