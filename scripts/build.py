"""Only format source Markdown for reading; never rewrite its content."""
from pathlib import Path
import re, html, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
def esc(s):return html.escape(s,quote=True)
def inline(s):
    s=esc(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
    def link(m):
        label,url=m[1],html.unescape(m[2])
        if url.endswith('.md'):url=Path(url).stem+'.html'
        if url.startswith(('https://','http://','#')) or re.match(r'^[\w-]+\.html$',url):return '<a href="'+esc(url)+'">'+label+'</a>'
        return m[0]
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    return s
def render(md):
    lines=md.splitlines(); out=[]; i=0
    if lines and lines[0]=='---':
        end=next((j for j in range(1,len(lines)) if lines[j]=='---'),0)
        if end:
            out.append('<details><summary>原文件元数据</summary><pre>'+esc('\n'.join(lines[:end+1]))+'</pre></details>');i=end+1
    while i<len(lines):
        line=lines[i]; t=line.strip()
        if not t:i+=1;continue
        if t.startswith('```'):
            block=[]; i+=1
            while i<len(lines) and not lines[i].strip().startswith('```'):block.append(lines[i]);i+=1
            out.append('<pre><code>'+esc('\n'.join(block))+'</code></pre>');i+=1;continue
        if re.match(r'^#{1,6} ',t):
            m=re.match(r'^(#{1,6}) (.*)',t);level=len(m[1]);out.append(f'<h{level}>{inline(m[2])}</h{level}>')
        elif t=='---':out.append('<hr>')
        elif t.startswith('|') and i+1<len(lines) and re.match(r'^\s*\|[ :|\-]+\|\s*$',lines[i+1]):
            rows=[t];i+=2
            while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
            out.append('<div class="table-scroll"><table>')
            for j,row in enumerate(rows):
                tag='th' if j==0 else 'td';out.append('<tr>'+''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in row.strip('|').split('|'))+'</tr>')
            out.append('</table></div>');continue
        elif t.startswith('>'):out.append('<blockquote>'+inline(t.lstrip('> ').strip())+'</blockquote>')
        elif re.match(r'^(?:[-*]|\d+\.) ',t):
            indent=len(line)-len(line.lstrip());out.append(f'<p class="list-line" style="margin-left:{min(indent,12)*8}px">'+inline(t)+'</p>')
        else:out.append('<p>'+inline(t)+'</p>')
        i+=1
    return '\n'.join(out)
def page(title,body,prefix=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · 青春期知识树</title><link rel="icon" href="{prefix}assets/icon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/tree.css"><script src="{prefix}assets/tree.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><header class="header"><div class="shell header-inner"><a class="brand" href="{prefix}index.html"><img class="personal-logo" src="{prefix}assets/gudaobei-logo.png" alt="古道北 Logo" width="48" height="48"><span class="brand-text"><strong>青春期 · 家长知识树</strong><small>古道北的技术分享</small></span></a><nav><a href="{prefix}index.html">事件目录</a><a href="{prefix}index.html#ages">按年龄读</a><a href="{prefix}tools.html">下载练习表</a><a href="{prefix}practice.html">与 AI 一起练习</a></nav></div></header>{body}<footer class="shell footer"><p class="personal-credit">网站整理与技术分享 · 古道北</p><p>阅读现有笔记，从具体问题出发。</p><a href="{prefix}copyright.html">原著信息与版权声明</a><p class="small">原文来自《解码青春期》AI 学习材料，正文保留，未经逐条核验；不是诊疗指南。练习表为整理版。</p></footer></body></html>'''
events=[
('孩子说“别管我”，我还要靠近吗？','陪伴与关系','ch01'),
('什么都要我盯，怎样慢慢放手？','学习与自主','ch02'),
('养孩子太累，我也需要帮助','陪伴与关系','ch03'),
('孩子总担心别人不喜欢自己','年龄与成长','ch04'),
('孩子变得敏感，不愿和我说话','年龄与成长','ch05'),
('朋友比父母重要，怎么走进他的世界？','年龄与成长','ch06'),
('孩子总问“为什么我不能”？','年龄与成长','ch07'),
('孩子想证明自己，我怎样支持？','年龄与成长','ch08'),
('快毕业了，孩子不知道将来做什么','年龄与成长','ch09'),
('撒了谎、伤了心，怎样重新建立信任？','陪伴与关系','ch10'),
('性、死亡、心理求助，难开口的话怎么谈？','陪伴与关系','ch11'),
('发现危险行为，我该重视哪些信号？','风险与求助','ch12'),
('手机放不下，还遇到了网络困扰','手机与学校','ch13'),
('学习没动力，或在学校受了委屈','手机与学校','ch14'),
('想和孩子聊聊，却不知道怎么开口','陪伴与关系','ch15')]
items=[]
for title,cat,code in events:
    p=next((DOCS/'texts/chapters').glob(code+'-*.md'));items.append((title,cat,p))
for name,title in [('cheatsheet','遇到冲突时，先翻一翻速查手册'),('patterns','同样的问题反复发生，有哪些沟通方法？'),('glossary','读到陌生概念，来这里查一查'),('SKILL','想先看全貌？从核心框架与总索引开始')]:items.append((title,'工具与速查',DOCS/'texts'/f'{name}.md'))
cards=[];manifest={}
for n,(title,cat,p) in enumerate(items):
    md=p.read_text(encoding='utf-8');slug=p.stem;raw=p.relative_to(DOCS).as_posix();original=next((line[2:] for line in md.splitlines() if line.startswith('# ')),p.stem)
    manifest[raw]=hashlib.sha256(p.read_bytes()).hexdigest()
    toc=''.join(f'<a href="#s{i}">{inline(m.group(2))}</a>' for i,m in enumerate(re.finditer(r'^(#{2}) (.+)$',md,re.M)))
    rendered=render(md);counter=iter(range(1000));rendered=re.sub(r'<h2>',lambda m:f'<h2 id="s{next(counter)}">',rendered)
    body=f'''<main id="main" class="shell reading-layout"><aside class="reading-aside"><a href="../index.html">← 返回知识树</a><p class="eyebrow">原文章节</p><nav>{toc}</nav></aside><article class="article original"><p class="eyebrow">原文阅读 / {esc(cat)}</p><div class="source-note">以下正文保留现有学习材料，不是新写的文章。标题与措辞按原文展示；内容尚未逐条核验。<a href="../{raw}" download>下载原始 Markdown ↓</a></div>{rendered}<details class="practice-box"><summary>读完之后，带着这个问题和 AI 聊聊</summary><p>先下载本页的原始 Markdown，附到你常用的 AI 对话中，再复制下方提问。若已在 Antigravity 中安装对应 Skill，也可以直接调用它。</p><textarea class="ai-prompt" readonly aria-label="可复制的 AI 提问模板">请参考我附上的《解码青春期》学习材料（{esc(p.name)}），协助我理解一个具体的家庭事件。
孩子的大致年龄：[填写]
发生的事情：[填写]
我已经尝试过：[填写]
我希望改善的是：[填写]
请先问我一个最需要澄清的问题，再结合材料一步步讨论。区分材料中的观点和你的补充，不要编造出处，不要把一次行为直接解释为孩子的动机或诊断。最后帮我整理一个可尝试的小行动和之后的复盘问题。</textarea><button type="button" data-copy-prompt>复制提问模板</button><span class="copy-status" role="status"></span><p class="small"><a href="../practice.html">了解如何使用完整 Skill →</a></p></details><div class="article-actions"><button data-print>打印文章</button><a href="../tools.html">下载家庭练习表</a><a href="../index.html">返回目录</a></div></article></main>'''
    (DOCS/'articles').mkdir(exist_ok=True)
    (DOCS/'articles'/f'{slug}.html').write_text(page(title,body,'../'),encoding='utf-8')
    cards.append(f'<a class="event-card" data-category="{esc(cat)}" data-search="{esc(title+" "+md)}" href="articles/{slug}.html"><span class="eyebrow">{esc(cat)} · {n+1:02d}</span><h3>{esc(title)}</h3><p>{esc(original)}</p><span class="card-end">阅读现有文章 ↗</span></a>')
ages=[]
for age,num in zip(['11—12 岁','12—14 岁','14—15 岁','15—16 岁','16—17 岁','17—18 岁'],range(4,10)):
    p=next((DOCS/'texts/chapters').glob(f'ch{num:02}-*.md'));ages.append(f'<a href="articles/{p.stem}.html">{age} ↗</a>')
cats=['全部事件']+list(dict.fromkeys(x[1] for x in items))
filters=''.join(f'<button data-filter="{c}" aria-pressed="{str(i==0).lower()}">{c}</button>' for i,c in enumerate(cats))
body=f'''<main id="main" class="shell"><section class="tree-hero"><p class="eyebrow">《解码青春期》学习笔记 · 知识树</p><h1>遇到一件事，<br>找到一篇值得读的文章。</h1><p class="intro">从眼前的困扰出发，也可以按年龄慢慢读。<br>按事件查阅，按年龄学习，把书里的方法带回日常。</p></section><section id="ages" class="age-section"><h2>孩子正处在哪个阶段？</h2><div class="age-links">{''.join(ages)}</div><p class="small muted">年龄是阅读线索，不是每个孩子必须遵循的成长时间表。</p></section><section id="events"><div class="section-heading"><h2>你正在遇到什么事？</h2><span class="muted">15 篇章节 · 4 份索引资料</span></div><form id="search-form" class="search-wrap" role="search"><label for="search">搜索文章全文</label><div class="search-row"><input id="search" type="search" placeholder="输入：手机、作业、朋友、道歉…" aria-describedby="search-hint"><button type="submit" class="search-submit">搜索</button></div><p id="search-hint" class="small muted">输入即筛选，也可以点击搜索或按回车确认。</p></form><div class="filters">{filters}</div><p id="result-count" tabindex="-1" class="small muted" aria-live="polite">共 19 篇资料</p><div class="cards">{''.join(cards)}</div><div id="empty" class="empty" hidden><p>没有找到匹配资料，换个词试试。</p><button id="reset">清除搜索和筛选</button></div></section><section class="tool-banner"><div><h2>一起商量，一起写下来。</h2><p>家庭小约定与亲子复盘表，保留为可下载、可打印的练习工具。</p></div><a class="primary" href="tools.html">打开两张练习表 ↗</a></section><details class="sources"><summary>关于原文与使用范围</summary><p>正文来自用户已有的 book-to-skill 学习材料，逐字保留，网页只做 Markdown 显示转换。事件入口标题是导航标签，不是对原文内容的重新改写。原文可能含未经核实或过度概括的表述，尤其风险与求助章节不能直接作为危机处置指令。网站不包含原著 EPUB。</p><p>文章内的 Markdown 流程图代码按原文保留；文末章节编号可配合首页目录查阅。两张练习表沿用上一版整理版，非书中原表的逐字复制。</p></details></main>'''
(DOCS/'index.html').write_text(page('事件目录',body),encoding='utf-8')
(ROOT/'source-checksums.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(DOCS/'.nojekyll').write_text('')
print('Built 19 original-text pages. Source Markdown left unchanged.')
import zipfile
(DOCS/'downloads').mkdir(exist_ok=True)
with zipfile.ZipFile(DOCS/'downloads/shipp-decoding-teens.zip','w',zipfile.ZIP_DEFLATED) as bundle:
    for source in (DOCS/'texts').rglob('*.md'):
        bundle.write(source,Path('shipp-decoding-teens')/source.relative_to(DOCS/'texts'))
