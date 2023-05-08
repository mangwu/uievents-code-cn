# UI 用户界面键盘事件 code 属性值(UI Events KeyboardEvent code Values)

本仓库属于翻译参考，不具备规范一致性，下面都是对源fork仓库的README翻译，
不适用被参考及其本仓库生成的非标准提案，只能作为学习参考。

此fork仓库的源仓库用于编写 [UI Events code](https://w3c.github.io/uievents-code/) 规范。

该规范还包含一份 [实现报告](https://w3c.github.io/uievents-code/impl-report.html)。

## 构建

此规范是使用 [bikeshed](https://github.com/tabatkins/bikeshed) 创建的。
如果您想贡献编辑，请确保您的更改能正确生成。
This spec was created using [bikeshed](https://github.com/tabatkins/bikeshed).
If you would like to contribute edits, please make sure that your changes
build correctly.

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
2. 构建 (上面的构建操作)。构建成功后会创建 `impl-report.bs` 和
  `impl-report.html` 文件。

与 `index.bs` 文件一样，请确保您没有拉入 `impl-port.bs` 文件。
它也列在 `.gitignore` 文件中。

## 相关联链接

* <b>此规范:</b> [UI Events KeyboardEvent code Values](https://w3c.github.io/uievents-code/)
* UI Events KeyboardEvent key Values : [Github project](https://github.com/w3c/uievents-key/), [Link to spec](https://w3c.github.io/uievents-key/)
* UI Events : [Github project](https://github.com/w3c/uievents/), [Link to spec](https://w3c.github.io/uievents/)
