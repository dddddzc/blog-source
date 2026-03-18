---
title: vscode中打汉字拼音只出现下划线不出现文字
date: 2026-03-13 23:19:33
tags: 
 - vscode
 - 打字 
categories: bug
---

早在 2025 下半年的时候，笔者使用 vscode 输入汉字拼音时，就会经常触发只出现下划线而不显示文字的问题。

正常情况下在 vscode 中打字：

![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260313232127652.png)

但有时候会出现这种情况：

![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260313232222010.png)

我以为是插件过多，或者搜狗输入法的问题，甚至尝试重装了 Vscode 也无法解决。当时的 AI 也不懂这个问题，毕竟也没有解决这个问题的文章来源。

如果是写代码也就算了，写注释什么的还可以用英文代替。

但我的毕业论文撰写深受其害，我放弃了曾经 Vscode + LaTex + Github Copilot 的组合，而是选择使用 TexStudio 进行手工古法撰写。

但就在论文快交初稿的今天，我心血来潮在网上搜索了一下，发现这个问题是 Vscode 自身的 BUG，并且已经有了解决方法：
原因是新版的 Vscode 使用了 EditContext API，这个 API 导致了输入汉字的 bug，我们在 Vscode 设置中搜索 "editContext"，取消勾选即可。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260313233050572.png)

感谢网友!
<!-- 给出引用的网址 -->
参考来源：<https://www.cnblogs.com/hardestnut/articles/19043595>
