---
id: visual-system
title: "视觉系统：我常被问到的 100 个问题"
record_type: output
status: reusable
created: 2026-06-07
updated: 2026-06-07
---

# 视觉系统：我常被问到的 100 个问题

这份文件用于固定 Ordinary Path Lab 系列文章的封面图和插图方向。

目标不是做成营销海报，而是让读者一眼知道：这是一篇从真实问题里整理出来的文章。

## 系列名称

主系列名：

```text
我常被问到的 100 个问题
```

封面上可以使用：

```text
我常被问到的 100 个问题
#001
AI 时代，文科或非技术背景的人还需要学编程吗？
```

编号从 `#001` 开始，后续文章递增。

## 封面气质

关键词：

- 日常
- 真实
- 安静
- 克制
- 有问题感
- 有笔记感
- 不像课程广告
- 不像成功学海报

避免：

- 科技蓝光和赛博风。
- 夸张 AI 机器人。
- 大字报式焦虑标题。
- “逆袭”“上岸”“财富自由”式视觉语言。
- 过度精英化的办公室和成功人士形象。

## 封面构图

推荐固定模板：

```text
左上：我常被问到的 100 个问题
左中：#001
主标题：AI 时代，文科或非技术背景的人还需要学编程吗？
右下或底部：Ordinary Path Lab / 孙玲
```

画面建议：

- 桌面、电脑、笔记本、便签、手写问题。
- 便签上可以出现短词：`AI?`、`转码?`、`Python?`、`下一步?`。
- 人可以出现，但不要像职业宣传照；更像一个人在整理问题。
- 保留留白，让标题能清楚放上去。

## 第一篇封面 Prompt

中文 prompt：

```text
一张温暖、安静、真实感的公众号文章封面图。桌面上有一台打开的笔记本电脑、一本摊开的纸质笔记本、几张手写便签，便签上写着“AI?”、“转码?”、“Python?”、“下一步?”。画面像一个普通人在整理自己收到的问题，而不是商业课程广告。自然光，柔和但不梦幻，颜色克制，有留白，适合叠加中文标题。不要机器人，不要赛博风，不要夸张科技感，不要成功学海报。
```

English prompt:

```text
A warm, quiet, realistic editorial cover image for a Chinese essay series. A desk with an open laptop, an open paper notebook, and several handwritten sticky notes saying "AI?", "转码?", "Python?", and "下一步?". The scene should feel like an ordinary person organizing real questions, not a commercial course advertisement. Natural light, restrained colors, gentle but not dreamy, with enough empty space for Chinese title text. No robots, no cyberpunk, no exaggerated tech glow, no motivational poster style.
```

## 封面文字模板

```text
我常被问到的 100 个问题
#001
AI 时代，文科或非技术背景的人还需要学编程吗？
```

可选短版：

```text
#001
AI 时代，还需要学编程吗？
```

## 文中插图类型

不是每篇都需要插图。需要时，插图应该帮助读者理解问题，而不是装饰。

### 结构图

用于拆概念。

本篇可用：

```text
学编程
  -> 工具
  -> 协作能力
  -> 职业转型
```

### 小实验卡片

用于给读者一个低成本起点。

本篇可用：

```text
30 天小实验
- 处理一份真实表格
- 做一个简单网页
- 自动化一个重复流程
```

### 判断清单

用于提示现实条件。

本篇可用：

```text
转行前先看
- 为什么想转
- 是否写过代码
- 经济缓冲
- 真实岗位信息
- 其他调整方式
```

## 文中插图风格

推荐：

- 黑白或低饱和。
- 像笔记、卡片、流程图。
- 简单线条，少装饰。
- 可以手写感，但要清楚。

避免：

- 信息过满。
- 卡通化过强。
- 强科技感。
- 用插图替代文章本身的判断。

## 每篇文章记录模板

```md
## #001 AI 时代，文科或非技术背景的人还需要学编程吗？

- article_path: `06-article-drafts/article-20260606-liberal-arts-cs-fit.md`
- cover_title: `AI 时代，文科或非技术背景的人还需要学编程吗？`
- cover_short_title: `AI 时代，还需要学编程吗？`
- cover_prompt_status: drafted
- cover_image_status: not_generated
- inline_visuals:
  - `学编程三层结构图`
  - `30 天小实验卡片`
  - `转行前现实条件清单`
- privacy_check: pending
- publish_status: draft
```

## 已生成素材

### #001 AI 时代，文科或非技术背景的人还需要学编程吗？

- article_path: `06-article-drafts/article-20260606-liberal-arts-cs-fit.md`
- cover_publish: `05-outputs/article-visuals/001-ai-programming-cover-publish.jpg`
- cover_text:

```text
我常被问到的 100 个问题
#001
AI 时代，还需要学编程吗？
```

- image_status: publish_cover_ready
- note: 发布版 JPG 当前约 310KB，低于 2MB；后续如需要二次排版，再重新生成无字背景和 PNG 母版。

## 文章产出时的视觉流程

以后每篇系列文章完成草稿后，顺手做三件事：

1. 在本文档里新增一条视觉记录。
2. 生成一张无中文标题的封面底图，保存到 `05-outputs/article-visuals/`。
3. 判断是否需要文中插图；只有当插图能帮助理解结构、实验或判断清单时才生成。

默认不让 AI 直接生成中文标题。中文标题后期叠加，避免乱码。
