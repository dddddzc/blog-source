---
title: 如何使用 GitHub Copilot CLI
date: 2026-03-25 10:00:00
tags:
 - github copilot
 - cli
categories:
 - AI
 - 编程工具
---

## 前言
2月底购买的阿里云百炼 Coding Plan 马上就到期了，现在各家的 Coding Plan 不仅变贵了，而且买不到了，需要抢购。
作为一个穷鬼，一直贯彻的是薅羊毛理念，只买便宜的。于是我想起了 github copilot。当初学生认证获得了 github copilot pro 的使用权，但一直是在 ide 内接入插件使用，没有用过 cli，今天来试试并记录一下。

## 安装
参考官方文档，由于我们是 windows 系统，所以我选择最简单的跨平台 npm 安装方式。
```bash
npm install -g @github/copilot
```
安装很简单，很快就完成了。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325002022691.png)

## 认证
认证同样很简单，跟着官方文档的步骤来即可。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325002153281.png)

输入 `copilot` 命令启动后就进入了 copilot cli，界面还挺酷炫的。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325002313866.png)

最开始会有一些询问，按照提示操作即可。注意这个：
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325002520757.png)

这是因为 cli 一般来说不支持多行输入，copilot cli 在询问你要不要添加一个快捷键 `Shift + Enter` 来支持多行输入，个人推荐添加。
如果选择 Yes，就会给 Windows Terminal 加一个配置：
Enter → 提交
Shift + Enter → 换行（不会提交）

然后我们开始登录，输入 `/login` 命令启动登录流程。此处不得不再提一句这个命令的高亮提示还蛮好看的。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325002917331.png)

等待几秒浏览器就会弹出 github 的 authorization 界面，并且 cli 上会给出授权码。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325003021687.png)

在 authorization 界面输入此时 cli 上给出的8位授权码即可。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325003150354.png)

![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325003324075.png)

然后就可以愉快的使用 github copilot cli 了！

## 使用方法
使用方法和各大主流的 code cli 类似，不多赘述，只不过好像多了 esc 打断当前正在执行任务的功能，个人还挺喜欢的。

来试试 `/model` 命令切换使用的模型。这里就是学生 copilot pro 的所有可用模型了，一般就 Gemini 3 Pro/GPT-5.3-Codex/GPT-5.4 mini 三选一了，根据场景选择使用。编程的话应该是 GPT-5.3-Codex 最好。然后 GPT-5.4 mini 上下文好像是最大的，有 400k。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325003616671.png)


甚至还可以选择模型的模式：包括 Low/Medium/High/Extra High，其实就是在速度和推理能力上做权衡。个人对速度不是很敏感（copilot 无论如何应该都没有 Coding Plan 高峰期的时候卡吧），所以会选择 Extra High。
![](https://raw.githubusercontent.com/dddddzc/ImageBed/main/img/20260325004004609.png)

## 参考资料
主要参考官方文档，链接：https://docs.github.com/zh/copilot/how-tos/copilot-cli/cli-getting-started