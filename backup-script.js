/*
 * @Author: mangwu                                                             *
 * @File: backup.js                                                            *
 * @Date: 2023-05-12 16:36:22                                                  *
 * @LastModifiedDate: 2023-05-12 16:53:48                                      *
 * @ModifiedBy: mangwu                                                         *
 * -----------------------                                                     *
 * Copyright (c) 2023 mangwu                                                   *
 * -----------------------                                                     *
 * @HISTORY:                                                                   *
 * Date   	            By 	    Comments                                       *
 * ---------------------	--------	----------------------------------------------- *
 */

/**
 * @description 备份样式
 */
function backupLink() {
  const link = document.querySelector("link");
  link &&
    link.addEventListener("error", () => {
      // 样式文件加载失败使用备份样式
      console.log("加载w3c样式失败，使用备份样式");
      const newLink = document.createElement("link");
      link.setAttribute("rel", "stylesheet");
      link.setAttribute("href", "./backup.css");
      document.head.appendChild(newLink);
    });
}

/**
 * @description 备份样式
 */
function backupLogo() {
  const logo = document.querySelector(".logo > img");
  logo &&
    logo.addEventListener("error", () => {
      // logo文件加载失败使用备用logo
      console.log("加载w3c logo失败，使用备份logo");
      logo.setAttribute("src", "./logos/W3C.svg");
    });
}

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

tryCatch(backupLink, "备份样式加载失败:")
tryCatch(backupLogo, "备份logo加载失败:")

