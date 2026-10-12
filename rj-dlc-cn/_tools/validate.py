#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metalearner-cn 译文校验脚本
检查：主题切换、MathJax、占位符、标签平衡、引用锚点可解析、中文内容。
用法：python validate.py [path/to/index.html]
"""
import sys, re, os

PLACEHOLDERS = ["TODO", "FIXME", "[翻译]", "[待译]", "Lorem", "placeholder",
                "PLACEHOLDER", "xxxx", "XXXXX", "@@"]

def check(path):
    html = open(path, encoding="utf-8").read()
    warns, errors = [], []
    # 1. theme toggle
    if 'id="theme-toggle"' not in html:
        errors.append("缺少主题切换按钮 #theme-toggle")
    if "share-theme" not in html:
        errors.append("缺少主题 localStorage 逻辑")
    # 2. MathJax
    if "tex-mml-chtml.js" not in html:
        errors.append("缺少 MathJax 脚本")
    # 3. 占位符
    for ph in PLACEHOLDERS:
        if ph in html:
            warns.append(f"发现疑似占位符: {ph}")
    # 4. 空链接 / 未翻译英文段落(粗略)
    # 5. 引用锚点解析
    hrefs = set(re.findall(r'href="#(ref-[^"]+)"', html))
    ids = set(re.findall(r'id="(ref-[^"]+)"', html))
    missing = hrefs - ids
    if missing:
        errors.append(f"引用锚点缺失 id: {sorted(missing)}")
    # 交叉引用 eq / section
    xrefs = set(re.findall(r'href="#(eq:[^"]+|[a-z][a-z0-9-]+)"', html))
    xids = set(re.findall(r'id="(eq:[^"]+|[a-z][a-z0-9-]+)"', html))
    xmiss = xrefs - xids
    # 过滤掉明显外部/目录项
    xmiss = {x for x in xmiss if not x.startswith("ref-")}
    if xmiss:
        warns.append(f"交叉引用锚点缺失 id(可忽略若不存在): {sorted(xmiss)}")
    # 6. 标签平衡（粗略 div）
    nd_open = len(re.findall(r'<div(\s|>)', html))
    nd_close = len(re.findall(r'</div>', html))
    if nd_open != nd_close:
        warns.append(f"div 标签不平衡: open={nd_open} close={nd_close}")
    # 7. 中文内容
    cjk = len(re.findall(r'[一-鿿]', html))
    if cjk < 500:
        errors.append(f"中文内容过少: {cjk} 字")
    # 8. 数学公式保留
    if html.count('class="math inline"') + html.count('class="math display"') < 50:
        warns.append("数学公式数量偏少，请核对")
    # 9. 图片
    if 'jzhou.org/images/ReviewCausal_1.png' not in html:
        warns.append("主图未绝对化或缺失")
    # 结果
    print(f"== 校验 {os.path.basename(path)} ==")
    print(f"  中文汉字数 : {cjk}")
    print(f"  行内公式   : {html.count('class=\"math inline\"')}")
    print(f"  显示公式   : {html.count('class=\"math display\"')}")
    print(f"  引用锚点   : {len(hrefs)} 处, 缺失 {len(missing)}")
    print(f"  主题按钮   : {'OK' if 'id=\"theme-toggle\"' in html else 'MISSING'}")
    print(f"  MathJax    : {'OK' if 'tex-mml-chtml.js' in html else 'MISSING'}")
    for w in warns: print("  [WARN]", w)
    for e in errors: print("  [ERROR]", e)
    if errors:
        print("结果: 不通过")
        return 1
    print("结果: 通过")
    return 0

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "index.html")
    sys.exit(check(os.path.abspath(p)))
