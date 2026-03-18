---
title: Vscode + Github Copilot接入MATLAB
date: 2026-03-14 15:50:36
tags: 
 - vscode
 - github copilot
 - matlab
categories:
 - 编程工具
---

## 前言
matlab 的编辑器虽然功能齐全，但在代码补全和智能提示方面完全不如现代编辑器例如 vscode（可以接入 AI 插件提效）。本文将介绍如何使用 vscode + github copilot 提升 matlab 编程效率。

以前的配置很麻烦，但由于 matlab 官方对 vscode 的插件支持，现在的接入方式非常简单：

## 前置准备
1. 安装 vscode 和 MATLAB，这一步不多说，但 MATLAB 的版本越新越好（R2023a 及以上，强推R2025b）。
2. 打开 vscode，点击左侧的[扩展]，搜索 "MATLAB" 并安装 "MATLAB" 插件，最好是安装官方插件。其他的插件也可以用，甚至有更多的功能，但官方插件更简单更稳定。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314160120392.png)
3. 在[扩展]广场搜索 "GitHub Copilot Chat" 并安装对应插件。注意 GitHub Copilot 已被弃用。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314160303383.png)

## 配置 GitHub Copilot Chat 插件
安装完成后，点击 Copilot 的机器人图标，会有网页弹出，登录你的 GitHub 账号并授权即可。

这一步忘了截图。

## 配置 MATLAB 插件
安装 MATLAB 插件后，点击左下角的设置，主要配置这两项：

Install Path：选择你电脑上的 MATLAB 安装路径，例如 `C:\Program Files\MATLAB\R2025b`。我的路径是 `D:\MATLAB`，根据你的实际情况填写即可。

Matlab Connection Timing: 如果选择 "On Startup"，这样在每次打开 vscode 时都会自动连接 MATLAB。我个人建议选择 "On Demand"，这样只有在需要使用 MATLAB 功能时才连接，避免每次打开 vscode 都连接 MATLAB 导致启动变慢。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314160836124.png)

还可以配置别的，例如 formatter 等。配置好后 vscode 左下角会显示 MATLAB 的连接状况：

![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314161223729.png)

显示 Connected 就可以开始在 vscode 里写代码了，无需显式打开 MATLAB 前台。完美继承了以下功能：

1. MATLAB 终端
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162000562.png)

2. run selection 和 run section
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162204183.png)

3. 调试
在 vscode 中，代码行左侧正常打断点，按 F5 就可以调试了，和在 MATLAB 前端调试一样。断点、单步执行、查看变量等功能都支持。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162320434.png)
如果配置了这个，那么直接点击运行就可以进入调试模式。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162429535.png)

4. 批量修改变量
选中变量，按 F2，就可以批量修改变量名了。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162534816.png)
可以使用 Enter 直接重命名，或者 Ctrl + Enter 先预览再修改（下图）。个人感觉甚至比 MATLAB 原生的重命名功能更方便。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162725935.png)
其他高级功能例如例如绘图也可以正常使用。个人感觉唯一的不足是【不支持随时查看变量值】，但无伤大雅。个人喜欢在 vscode 的 MATLAB 终端中敲出 desktop 调出 MATLAB 前端以偶尔查看变量。有非官方插件实现了这一点，但我对这个需求没太大要求，于是没装。

## 配合 GitHub Copilot Chat 插件使用
这个就无须多言了，在 Copilot 的聊天窗口进行对话即可，Ask/Plan/Agent三个模式都可以使用，对于学生档免费使用 Github Copilot 更是友好。下图是用 Agent 模式，帮我免去了注释/批量修改代码的麻烦。

![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260314162937945.png)

## 总结
总而言之，vscode + github copilot 对于学生来说是一个非常强大的组合，可以大幅提升 matlab/latex 等非常规语言的编程效率。当然这也得益于各类插件的支持，感谢插件开发者团队！
