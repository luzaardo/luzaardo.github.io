#!/usr/bin/env python3
"""Puts the page editor's saved content into the real site files.

Usage:
  apply_editor_export.py PAGE CONTENT.html ASSETS_DIR   # PAGE = project-1 or project-2
  apply_editor_export.py --refresh-also                 # re-copy the "Also check out" cards from index.html

CONTENT.html is the saved page body from the editor. ASSETS_DIR holds the uploaded images, named <asset-id>.<ext>.
Images are resized and converted to WebP (480, 960 and 1600 px wide) so pages stay fast but sharp."""
import re, sys, os, glob
from html import escape
R = '/home/claude/luzaardo.github.io/'
WIDTHS = [480, 960, 1600]

def optimize(asset_id, src):
    from PIL import Image
    im = Image.open(src)
    if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGB')
    made = []
    for w in WIDTHS:
        if w > im.width and made: break
        k = min(1.0, w / im.width)
        out = im if k == 1 else im.resize((w, round(im.height * k)), Image.LANCZOS)
        name = f'images/case-{asset_id[:8]}-{w}.webp'
        out.save(R + name, 'WEBP', quality=80, method=6)
        made.append((name, out.width))
    return made

def rebuild_img(tag, page, assets_dir, first):
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
    aid = attrs.get('data-asset')
    if not aid: return tag
    files = glob.glob(os.path.join(assets_dir, aid + '*'))
    if not files:
        print('WARNING: asset file missing for', aid); return tag
    made = optimize(aid, files[0])
    best = made[min(1, len(made) - 1)][0]
    srcset = ', '.join(f'{n} {w}w' for n, w in made)
    alt = escape(attrs.get('alt', ''), quote=True)
    extra = '' if first else ' loading="lazy"'
    return f'<img src="{best}" srcset="{srcset}" sizes="(max-width: 760px) 100vw, 1000px" alt="{alt}"{extra} decoding="async">'

def check(html):
    if re.search(r'<\s*script|\son\w+\s*=|javascript:|<\s*iframe', html, re.I):
        sys.exit('Refusing to publish: the saved content contains scripts or unsafe markup.')

def refresh_also(page_names=('project-1', 'project-2')):
    index = open(R + 'index.html').read()
    cards = {m.group(1): m.group(0) for m in re.finditer(r'<a class="project" href="(project-\d\.html)">.*?</a>', index, re.S)}
    for name in page_names:
        other = 'project-2.html' if name == 'project-1' else 'project-1.html'
        card = cards.get(other)
        if not card: print('WARNING: no Home card found for', other); continue
        block = ('<section class="also" aria-labelledby="also-h">\n      <h2 class="eyebrow" id="also-h">Also check out</h2>\n      '
                 + card + '\n    </section>')
        path = R + name + '.html'; text = open(path).read()
        text = re.sub(r'(<!-- ALSO:START[^\n]*-->).*?(<!-- ALSO:END -->)', lambda m: m.group(1) + '\n    ' + block + '\n    ' + m.group(2), text, flags=re.S)
        open(path, 'w').write(text)
    print('Also-check-out cards refreshed')

def apply(page, content_file, assets_dir):
    html = open(content_file).read().strip()
    check(html)
    imgs = list(re.finditer(r'<img\b[^>]*>', html))
    out, pos = [], 0
    for i, m in enumerate(imgs):
        out.append(html[pos:m.start()]); out.append(rebuild_img(m.group(0), page, assets_dir, i == 0)); pos = m.end()
    out.append(html[pos:]); html = ''.join(out)
    path = R + page + '.html'; text = open(path).read()
    new = '<!-- EDITABLE:START (managed by the page editor; do not rename these markers) -->\n    <article class="case-body">\n    ' + html + '\n    </article>\n    <!-- EDITABLE:END -->'
    text, n = re.subn(r'<!-- EDITABLE:START.*?<!-- EDITABLE:END -->', lambda m: new, text, flags=re.S)
    if n != 1: sys.exit('Could not find the editable region in ' + path)
    open(path, 'w').write(text)
    print('Updated', path)

if __name__ == '__main__':
    if sys.argv[1] == '--refresh-also': refresh_also()
    else: apply(sys.argv[1], sys.argv[2], sys.argv[3])
