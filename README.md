# 青春期家长知识树（原文阅读版）

本项目直接展示现有 chapters 文章，不重新解读或改写正文。事件标题只是入口，同一文章也可通过年龄入口找到。

## 本地使用
双击 `本地打开.html`。不需要编译、安装软件或联网。

可选本地服务器：`python -m http.server 8767 --bind 127.0.0.1 --directory docs`

## 内容在哪里
- `docs/texts/chapters/`：15 篇原始 Markdown，逐字复制保留。
- `docs/texts/`：原有速查、模式、术语和 SKILL 索引。
- `docs/articles/`：相同原文的网页阅读形式，不是另一套文章。
- `docs/downloads/`：两份独立可下载打印的 HTML 练习表，打开后可打印为 PDF。
- `scripts/build.py`：仅将 Markdown 显示成网页。文章更改后运行 `python scripts/build.py`，不涉及 AI 重新生成内容。
- `source-checksums.json`：正文原文件校验记录。

搜索覆盖 19 篇资料全文。表格按 HTML 展示，Mermaid 图保留原始代码。阅读页可以下载原始 Markdown。两张练习表沿用之前整理版，非原书表格逐字复制。

## 自己推送 GitHub
请将本文件夹作为独立项目，不要从包含原著的父文件夹提交全部文件。
在 GitHub 的 wumingdanwu-wq 账号创建空仓库 `teen-parent-guide` 后，在本项目文件夹运行：

```powershell
git init -b main
git add -- docs scripts README.md .gitignore 本地打开.html source-checksums.json
git diff --cached --stat
git commit -m "Add original-text parenting knowledge tree"
git remote add origin https://github.com/wumingdanwu-wq/teen-parent-guide.git
git push -u origin main
```

已有仓库先检查 `git status` 与 `git remote -v`，不要覆盖远端或强制推送。
推送后 Settings → Pages → Deploy from a branch → main → /docs → Save。
本次没有执行推送，未设置域名。

## 原文说明
Markdown 来自已有 AI 学习材料，未逐条校核，其中可能存在过度概括或不适用的建议；保留原文不代表验证其准确性。风险章节不能当成危机处置流程。未包含原著 EPUB。公开前仍需核查第三方内容的分享权利。

原著信息、第三方权利与授权范围见 `docs/copyright.html`。不将第三方材料标为开放许可。

## 工具来源与致谢

资料生成工作流来自 [apple-ouyang/book-to-skill](https://github.com/apple-ouyang/book-to-skill)，用户在 Antigravity 中使用后生成学习材料。本项目提供独立的阅读与检索界面，不代表上游官方产品。上游工具使用 MIT License；该许可不覆盖原著及译文，也不自动授予生成笔记第三方内容的再分发权。

网站新增“与 AI 一起练习”：文章底部可复制提问模板，完整 Skill 资料包在 `docs/downloads/shipp-decoding-teens.zip`。本网站不调用任何 AI API。
