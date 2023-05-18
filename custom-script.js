/*
 * @Author: mangwu                                                             *
 * @File: custom-script.js                                                     *
 * @Date: 2023-05-01 02:02:19                                                  *
 * @LastModifiedDate: 2023-05-19 01:27:40                                      *
 * @ModifiedBy: mangwu                                                         *
 * -----------------------                                                     *
 * Copyright (c) 2023 mangwu                                                   *
 * -----------------------                                                     *
 * @HISTORY:                                                                   *
 * Date   	            By 	    Comments                                       *
 * ---------------------	--------	----------------------------------------------- *
 */

/**
 * @description 尝试执行代码
 * @param {Function} callback 试运行的回调函数
 * @param {string} message 运行错误的打印消息
 * @param  {...any} args callback的参数
 */
function tryCatch(callback, message, ...args) {
  try {
    callback(...args);
  } catch (error) {
    console.log(message, error.message);
  }
}

/**
 * @description 查询元素
 * @param {string} selector 查询器
 * @param {HTMLElement}
 * @returns {NodeList}
 */
function getElements(selector, parent = document) {
  return parent.querySelectorAll(selector);
}
/**
 * @description 查询元素
 * @param {string} selector 查询器
 * @param {HTMLElement}
 * @returns {HTMLElement}
 */
function getElement(selector, parent = document) {
  return parent.querySelector(selector);
}
// 切换图像功能
function figureAllChange() {
  const figureChangeBoxes = getElements(".figure-change");
  for (const item of figureChangeBoxes) {
    figureChange(item);
  }
}

/**
 * @description 队单个图像添加图像切换功能
 * @param {HTMLElement} figureChangeBox 图像包裹层
 */
function figureChange(figureChangeBox) {
  const tabs = getElements(".custom-tabs-tab", figureChangeBox);
  const figures = getElements("figure", figureChangeBox);
  tabsChange(tabs, figures);
}

/**
 * @description 添加监听器
 * @param {NodeList} tabs
 */
function tabsChange(tabs, figures) {
  const tab1 = tabs[0];
  const tab2 = tabs[1];
  const figure1 = figures[0];
  const figure2 = figures[1];

  tab1.addEventListener("click", () => {
    const classList = tab1.classList;
    if (classList.length === 1) {
      classList.add("custom-tabs-tab-active");
      tab2.classList.remove("custom-tabs-tab-active");
      figure1.classList.remove("figure-hidden");
      figure2.classList.add("figure-hidden");
    }
  });
  tab2.addEventListener("click", () => {
    const classList = tab2.classList;
    if (classList.length === 1) {
      classList.add("custom-tabs-tab-active");
      tab1.classList.remove("custom-tabs-tab-active");
      figure2.classList.remove("figure-hidden");
      figure1.classList.add("figure-hidden");
    }
  });
}

/**
 * @description 翻译所有引用面板中的Reference in:
 */
function translatePanels() {
  const dfns = getElements(".dfn-paneled + span");
  for (const dfn of dfns) {
    translatePanel(dfn);
  }
}

/**
 * @description 翻译一个引用面板中的Reference in:
 * @param {HTMLElement} dfn
 */
function translatePanel(dfn) {
  const b2 = dfn.querySelector("aside.dfn-panel > span + b + b");
  if (b2) {
    b2.textContent = "引用列表: ";
  } else {
    const b1 = dfn.querySelector("aside.dfn-panel > b");
    if (b1) {
      b1.textContent = "引用列表: ";
    } else {
      console.log(dfn);
    }
  }
}

/**
 * @description 翻译目录英文部分
 */
function tranlateToc() {
  const tocTitle = getElement("#contents");
  tocTitle.textContent = "目录";
  const tocJump = getElement("#toc-jump > span + span");
  tocJump.textContent = "跳转到目录";
  const tocNav = getElement("#toc-nav");
  const tocToggle = getElement("#toc-toggle > span + span");
  setToggleContentTranlation(tocToggle);
  const mutationObserver = new MutationObserver((mutations) => {
    outer: for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (setToggleContentTranlation(node)) {
          break outer;
        }
      }
    }
  });
  mutationObserver.observe(tocNav, { childList: true, subtree: true });
}

/**
 * @description 翻译触发器内部文本
 * @param {Node} node
 * @returns {boolean}
 */
function setToggleContentTranlation(node) {
  if (node.textContent === "Pop Out Sidebar") {
    node.textContent = "弹出侧边栏";
    return true;
  } else if (node.textContent === "Collapse Sidebar") {
    node.textContent = "折叠侧边栏";
    return true;
  }
  return false;
}
/**
 * @description 翻译所有Dfn中的类型英文文本
 */
function translateDfnTypes() {
  const originDfns = getElements(".origin-dfn");
  for (const od of originDfns) {
    translateDfnType(od);
  }
}
/**
 * @description 翻译一个Dfn中的类型英文文本
 * @param {HTMLElement} originDfn
 */
function translateDfnType(originDfn) {
  const customDfn = originDfn.nextElementSibling;
  if (customDfn && customDfn.className == "custom-dfn") {
    const replacement = getElement(".replacement", customDfn);
    const span = getElement("span + span", originDfn);
    const idlNameLink = getElement("a", span);
    const copy1 = idlNameLink.cloneNode(true);
    const copy2 = replacement.cloneNode(true);
    span.replaceChildren(copy1, copy2);
    span.previousSibling.nodeValue = "，"; // 可修改英文逗号为中文逗号
  }
}

function tranlateIndex() {
  // 目录
  tranlateIndexBySeletor("a[href='#index'] .content", "索引");
  tranlateIndexBySeletor(
    "a[href='#index-defined-here'] .content",
    "本规范定义的术语"
  );
  tranlateIndexBySeletor(
    "a[href='#index-defined-elsewhere'] .content",
    "引用其他规范定义的术语"
  );
  // 标题
  tranlateIndexBySeletor("#index .content", "索引");
  tranlateIndexBySeletor("#index-defined-here .content", "本规范定义的术语");
  tranlateIndexBySeletor(
    "#index-defined-elsewhere .content",
    "引用其他规范定义的术语"
  );

  // 内容
  const eles = getElements(".index li a[data-link-type='biblio']");
  for (const ele of eles) {
    ele.nextSibling.nodeValue = "定义了以下术语: \n";
  }
}

function tranlateIndexBySeletor(seletor, translateZh = "", parent = document) {
  const element = getElement(seletor, parent);
  element.textContent = translateZh;
}
function tranlateReferences() {
  // 目录
  tranlateIndexBySeletor("a[href='#references'] .content", "引用");
  tranlateIndexBySeletor("a[href='#normative'] .content", "规范性引用");
  tranlateIndexBySeletor("a[href='#informative'] .content", "资料性引用");

  // 标题
  tranlateIndexBySeletor("#references .content", "引用");
  tranlateIndexBySeletor("#normative .content", "规范性引用");
  tranlateIndexBySeletor("#informative .content", "资料性引用");
}

window.addEventListener("DOMContentLoaded", () => {
  tryCatch(figureAllChange, "figureAllChange方法执行错误:");
  tryCatch(translatePanels, "translatePanels方法执行错误:");
  tryCatch(tranlateToc, "tranlateToc方法执行错误:");
  tryCatch(translateDfnTypes, "translateDfnTypes方法执行错误:");
  tryCatch(tranlateIndex, "tranlateIndex方法执行错误:");
  tryCatch(tranlateReferences, "tranlateReferences方法执行错误:");
});
