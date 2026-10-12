# -*- coding: utf-8 -*-
"""
把 course_template.html 中的 {{IMG:xxx}} 占位符替换为 base64 内嵌图片，
生成单文件、可离线打开的公开课 HTML。

用法：  python build.py
输出：  HTE公开课_平均值的谎言.html
"""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
TEMPLATE = os.path.join(HERE, 'course_template.html')
OUTPUT = os.path.join(HERE, 'HTE公开课_平均值的谎言.html')

MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext, 'image/png')
    with open(path, 'rb') as fh:
        raw = fh.read()
    return 'data:%s;base64,%s' % (mime, base64.b64encode(raw).decode('ascii'))


def main():
    html = open(TEMPLATE, encoding='utf-8').read()

    placeholders = re.findall(r'\{\{IMG:([^}]+)\}\}', html)
    if not placeholders:
        print('[warn] 模板中未发现任何 {{IMG:...}} 占位符')

    missing = []
    used = {}
    for name in placeholders:
        path = os.path.join(ASSETS, name)
        if not os.path.exists(path):
            missing.append(name)
            continue
        if name not in used:
            used[name] = data_uri(path)
        html = html.replace('{{IMG:%s}}' % name, used[name])

    if missing:
        print('[error] 以下图片缺失：', missing)
        return 1

    with open(OUTPUT, 'w', encoding='utf-8') as fh:
        fh.write(html)

    size_kb = os.path.getsize(OUTPUT) / 1024.0
    print('[ok] 已生成: %s' % OUTPUT)
    print('[ok] 体积: %.0f KB' % size_kb)
    print('[ok] 内嵌图片: %d 张（去重后）' % len(used))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
