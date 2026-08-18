# LaTeX 与 ZIP 交付规范

## 1. 模板优先级

1. 用户上传模板与 `.cls`。
2. 当年官方模板。
3. Skill 自带的 `assets/paper_skeleton.tex` 仅作骨架。

不要在用户已经给模板时另起版式系统。

## 2. 推荐工程结构

```text
project/
├── figures/
├── code/
│   ├── q1_*.py
│   ├── q2_*.py
│   ├── q3_*.py
│   ├── q4_*.py
│   ├── plot_*.py
│   ├── requirements.txt
│   └── README.md
├── .gitignore
├── cumcmthesis.cls
├── example.tex
├── example.pdf
├── example.aux
├── example.log
├── example.out
└── example.synctex.gz
```

## 3. 编译

优先 XeLaTeX，两遍以上：

```bash
xelatex -interaction=nonstopmode -halt-on-error example.tex
xelatex -interaction=nonstopmode -halt-on-error example.tex
```

有参考文献工具时按模板要求增加 biber/bibtex。

## 4. 必查日志

搜索：

- `Overfull`
- `Undefined`
- `LaTeX Warning`
- `Citation`
- `Reference`

对正文关键公式/表格的 Overfull 必须修正。

## 5. 页面检查

编译后使用 PDF 渲染检查：

- 摘要是否独占第1页；
- 图表是否越界；
- 中文字体是否正常；
- overview 图是否重叠；
- 表格是否过小；
- 参考文献是否排版整齐；
- 主论文是否落在目标页数。

## 6. 代码

代码必须服务于正文：

- 每问主模型代码独立或清晰分模块；
- 绘图代码独立；
- 固定随机种子；
- 输出关键数值；
- 不依赖无法获得的本地绝对路径；
- README 说明运行顺序。

## 7. ZIP

最终 ZIP 只包含必要工程。删除：

- 临时渲染图片；
- Python 缓存；
- 编辑器缓存；
- 无关下载文件；
- 调试中间产物。
