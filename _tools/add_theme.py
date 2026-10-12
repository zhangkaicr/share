# -*- coding: utf-8 -*-
"""
给 share 站点任意页面注入「明暗主题切换」组件（幂等：已有则跳过）。

用法:
    python add_theme.py <file.html> [light|dark]

机制（与已上线页面完全一致，不引外部资源，保证单文件离线可用）:
  1. <html> 上标记 data-theme-default="light|dark"（页面自身默认）
  2. <head> 内首行插入一段立即执行的 JS：localStorage["share-theme"] > 页面默认 > light
     放在样式之前执行，避免刷新时闪一下白底
  3. 在 </style> 前追加：暗/亮两套 CSS 变量覆盖 + .tt 按钮样式 + 图标切换规则
  4. <body> 后插入圆形按钮（内嵌太阳/月亮 SVG）
偏好存 localStorage，全站四个页面共享；支持 Alt+T 快捷键。
"""
import re
import sys

# ---------- 固定代码块 ----------
THEME_JS = """<script>
(function(){
  var KEY="share-theme", d=document.documentElement;
  try{var saved=localStorage.getItem(KEY);}catch(e){var saved=null;}
  d.setAttribute("data-theme", saved || d.getAttribute("data-theme-default") || "light");
  document.addEventListener("DOMContentLoaded",function(){
    var b=document.getElementById("theme-toggle"); if(!b) return;
    function sync(){
      var dark=d.getAttribute("data-theme")==="dark";
      b.setAttribute("aria-pressed", dark?"true":"false");
      b.setAttribute("title", dark?"切换到亮色主题 (Alt+T)":"切换到暗色主题 (Alt+T)");
    }
    b.addEventListener("click",function(){
      var nxt=d.getAttribute("data-theme")==="dark"?"light":"dark";
      d.setAttribute("data-theme",nxt);
      try{localStorage.setItem(KEY,nxt);}catch(e){}
      sync();
    });
    document.addEventListener("keydown",function(e){
      if(e.altKey&&(e.key==="t"||e.key==="T")) b.click();
    });
    sync();
  });
})();
</script>
"""

BTN_CSS = """
.tt{
  position:fixed; top:16px; right:16px; z-index:9999; width:40px; height:40px;
  display:flex; align-items:center; justify-content:center; border-radius:50%;
  cursor:pointer; color:var(--text); background:var(--card,var(--surface));
  border:1px solid var(--line);
  box-shadow:0 2px 10px rgba(0,0,0,.24); transition:transform .15s, border-color .15s, background .15s;
}
.tt:hover{transform:translateY(-1px); border-color:var(--accent)}
.tt:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
.tt svg{display:none}
[data-theme="dark"] .ico-sun{display:block}
[data-theme="dark"] .ico-moon{display:none}
[data-theme="light"] .ico-sun{display:none}
[data-theme="light"] .ico-moon{display:block}
@media(max-width:640px){.tt{top:10px; right:10px; width:36px; height:36px}}
@media print{.tt{display:none}}
"""

BTN_HTML = """<button id="theme-toggle" class="tt" type="button" aria-label="\u5207\u6362\u660e\u6697\u4e3b\u9898" title="\u5207\u6362\u660e\u6697\u4e3b\u9898 (Alt+T)">
  <svg class="ico-sun" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.4M12 19v2.4M2.6 12H5M19 12h2.4M5.3 5.3l1.7 1.7M17 17l1.7 1.7M18.7 5.3L17 7M7 17l-1.7 1.7"/></svg>
  <svg class="ico-moon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M20 14.5A8.2 8.2 0 0 1 9.5 4a8.2 8.2 0 1 0 10.5 10.5z"/></svg>
</button>
"""

# 亮色为主时追加的暗色覆盖（变量名与首页一致；--surface/--card 两块都给，兼容两种命名）
DARK_VARS = """
:root[data-theme="dark"]{
  --bg:#0f1116; --surface:#181b22; --surface-2:#1e222b; --card:#181b22;
  --text:#e4e6ea; --muted:#98a0ac; --faint:#6f7783;
  --line:#2a2f3a; --line-soft:#232833;
  --accent:#7aa2f7; --accent-dim:#2e6c55; --accent-soft:#16203a;
  --blue:#7aa2f7; --blue-soft:#16203a;
  --amber:#e0af68; --amber-soft:#2b2317;
  --code-bg:#0b0d12; --code-line:#1d2129;
  --tag:#1e222b;
}
"""


def inject(path, default="light"):
    src = open(path, encoding="utf-8").read()
    if 'id="theme-toggle"' in src:
        print("skip (already has toggle):", path)
        return False

    # 1) 标记页面默认主题
    if 'data-theme-default' not in src:
        src = re.sub(r'<html lang="zh-CN"', '<html lang="zh-CN" data-theme-default="%s"' % default,
                     src, count=1)
    if 'data-theme-default' not in src:          # 兜底：任意 <html ...>
        src = re.sub(r'<html\b', '<html data-theme-default="%s"' % default, src, count=1)

    # 2) <head> 后插入主题 JS（必须在 <style> 之前，避免闪烁）
    src = re.sub(r'(<head\b[^>]*>)', r'\1\n' + THEME_JS, src, count=1)

    # 3) </style> 前追加变量覆盖 + 按钮样式
    css = BTN_CSS if default == "dark" else DARK_VARS + BTN_CSS
    if "</style>" in src:
        idx = src.rfind("</style>")
        src = src[:idx] + css + "\n" + src[idx:]
    else:  # 没有 <style> 就新建一个
        src = re.sub(r'(</head>)', '<style>' + css + '</style>\n\\1', src, count=1)

    # 4) <body> 后插入按钮
    src = re.sub(r'(<body\b[^>]*>)', r'\1\n' + BTN_HTML, src, count=1)

    open(path, "w", encoding="utf-8").write(src)
    print("injected:", path, "| default =", default)
    return True


if __name__ == "__main__":
    p = sys.argv[1]
    d = sys.argv[2] if len(sys.argv) > 2 else "light"
    inject(p, d)
