# UI 用户界面键盘事件 code 属性值(UI Events KeyboardEvent code Values)

本仓库属于翻译参考，不具备规范一致性，下面都是对被fork的 [源仓库](https://github.com/w3c/uievents-code) 的 `README.md` 的翻译，本仓库生成的非标准提案包含译者对原规范的理解，不属于规范文档，只能作为学习参考。翻译链接如下

1. [UI 用户界面键盘事件 code 属性值](https://mangwu.github.io/uievents-code-cn/)
2. [实现报告](https://mangwu.github.io/uievents-code-cn/impl-report.html)

此fork仓库的源仓库用于编写 [UI Events code](https://w3c.github.io/uievents-code/) 规范。

该规范还包含一份 [实现报告](https://w3c.github.io/uievents-code/impl-report.html)。

## 构建

此规范是使用 [bikeshed](https://github.com/tabatkins/bikeshed) 创建的。
如果您想贡献编辑，请确保您的更改能正确生成。

要**构建**此规范，请执行以下操作:

1. 将此仓库克隆到本地目录中。
1. 安装 [bikeshed](https://github.com/tabatkins/bikeshed)
1. 在本地目录中运行`python build.py`。

要编辑本规范，请执行以下操作:

1. 编辑 `index-source.txt` 文件。
2. 构建 (上面的构建操作)。构建成功后会创建 `index.bs` 和 `index.html` 文件.

提交 pull 请求时，请确保您的变更列表中没有包含 `index.bs` 文件——它是
`.gitignore` 的一部分，这样您就不会意外包含它。所有更改都应在
`index-source.txt`文件中进行。

要**更新实现报告**，请执行以下操作:

1. 编辑 `impl-report.txt` 文件。
2. 构建 (上面的构建操作)。构建成功后会创建 `impl-report.bs` 和 `impl-report.html` 文件。

与 `index.bs` 文件一样，请确保您没有拉入 `impl-port.bs` 文件。
它也列在 `.gitignore` 文件中。

## 相关联链接

* <b>此规范:</b> [UI Events KeyboardEvent code Values](https://w3c.github.io/uievents-code/)
* UI Events KeyboardEvent key Values : [Github 项目](https://github.com/w3c/uievents-key/), [规范链接](https://w3c.github.io/uievents-key/)
* UI Events : [Github project](https://github.com/w3c/uievents/), [规范链接](https://w3c.github.io/uievents/)

# 合并记录

本节内容不属于fork仓库的内容，属于翻译项目基于源fork仓库更新后的异步合并记录。

需要注意的是，本翻译项目是从源仓库的 [Fix](https://github.com/w3c/uievents-code/commit/c89e2a1482efb8960964f75633117b2a79962740) [#33](https://github.com/w3c/uievents-code/issues/33)[: Remove "Page Down" as keycap for "End"](https://github.com/w3c/uievents-code/commit/c89e2a1482efb8960964f75633117b2a79962740)  (c89e2a1482efb8960964f75633117b2a79962740)开始进行的，所以不会有之前(包括这次)的合并记录

| 源项目更新                                                   | 源项目更新的SHA码                         | 本项目更新的SHA码                                            | 更新内容                                                     |
| :----------------------------------------------------------- | :---------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [Fix](https://github.com/w3c/uievents-code/commit/b201684d1de0af90bc403814bbdee6aa96647130) [#41](https://github.com/w3c/uievents-code/issues/41) [Fix titles in control pad figure.](https://github.com/w3c/uievents-code/commit/b201684d1de0af90bc403814bbdee6aa96647130) | b201684d1de0af90bc40 3814bbdee6aa96647130 | [6f6e9dcfdb79a7235a49 81033bcb2f75c86f21cd](https://github.com/mangwu/uievents-code-cn/commit/6f6e9dcfdb79a7235a4981033bcb2f75c86f21cd) | 键盘区域控制板(control pad)布局图示的 `images/control-pad.svg` 文件显示的描述有错误，修正之 |

