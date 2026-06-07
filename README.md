# Ordinary Path Lab 普通人路径实验室

这是一个围绕真实问题建立的个人知识与连接系统。

它把散落的读者提问、咨询记录、邮件、聊天、会议转写和会后笔记，整理成本地优先、可搜索、可分类、可复用的 Markdown 知识库。这个系统不是 Web app，也不是数据库；它的核心是先保留真实处境和回答细节，再拆出可复用问题，聚合成主题，最后流向内容、服务和人与人的连接。

核心循环是：

```text
真实问题 -> 结构化沉淀 -> 内容输出 -> 服务改进 -> 人与人连接 -> 新的问题和经验
```

## 当前状态

截至 2026-06-07，已有：

- `00-inbox`：46 份原始材料索引。
- `02-normalized`：42 条标准化咨询记录。
- `03-issue-units`：37 条问题单元。
- `04-topic-clusters`：7 个主题聚合。
- `05-outputs`：3 份可用化输出。
- `06-article-drafts`：1 篇文章草稿。
- `07-people`：咨询对象和联系方式管理，默认私密。

索引文件在：

- `01-source-index/source_inventory.md`
- `01-source-index/records.md`
- `01-source-index/records.csv`
- `01-source-index/records.json`
- `01-source-index/stats.md`

更新索引：

```bash
python3 scripts/build_index.py
```

扫描原始来源：

```bash
python3 scripts/scan_sources.py
```

## 核心原则

内容层是结果，不是第一步。

整理顺序是：

```text
原始资料
  -> 标准化咨询记录
  -> 问题单元
  -> 主题聚合
  -> 内容选题 / 服务雏形 / 连接池候选
```

不要一上来就把材料写成文章。先把真实问题、人物背景、回答逻辑和可复用洞察保存下来。

系统有三层输出：

- 内容层：文章、FAQ、案例、选题。
- 服务层：咨询服务、问卷、模板、资源包。
- 连接层：连接池、小圆桌、互助网络。

## 目录结构

```text
ordinary-path-lab/
  00-inbox/           # 新进来的原始材料
  01-source-index/    # 原始资料清单、索引和统计
  02-normalized/      # 标准化后的咨询记录
  03-issue-units/     # 从咨询记录里拆出的单个问题
  04-topic-clusters/  # 按主题聚合出的内容/服务/连接线索
  05-outputs/         # 内容选题、服务雏形、连接池候选
  06-article-drafts/  # 从 issue/topic 发展出的文章草稿
  07-people/          # 咨询对象、联系方式和连接意愿管理
  templates/          # 模板
  scripts/            # 本地脚本
  taxonomy.md         # 分类字段、主题、标签和隐私规则
```

旧咨询材料现在集中放在 `00-inbox/` 下：

- `00-inbox/问答咨询`
- `00-inbox/一对一咨询`
- `00-inbox/人生教练`

## 每一层做什么

### 00-inbox

放还没有进入知识库的新材料：

- Gmail 咨询邮件。
- 微信聊天记录。
- 公众号后台留言。
- 临时复制的评论、私信、问答。
- 一对一咨询或线上会议转写。

原则：只做暂存，不在这里深度整理。

### 01-source-index

登记和统计材料：

- `source_inventory.md`：原始来源清单。
- `records.md`：整理后记录索引。
- `records.csv`：表格索引。
- `records.json`：结构化索引。
- `stats.md`：按目录、主题、标签、层级统计。

### 02-normalized

这是最重要的基础层。每份原始材料先整理成一份标准化咨询记录，固定包含：

- 她/他是谁。
- 原始问题。
- 背景处境。
- 真正卡住的地方。
- 我的回答。
- 后续追问。
- 可复用洞察。
- 可能沉淀成的内容。
- 适合的服务形态。
- 连接池可能性。

“她/他是谁”要尽量保留事实背景：年龄、性别、所在地、身份、学历、工作、关键经历、当前资源和当前约束。没有提到的信息写“未提及”，不要为了完整而猜测。

“我的回答”要保留判断过程：回答立场、具体建议、不确定部分、判断逻辑和可复用原话。

模板：

```text
templates/normalized-consult.md
```

### 03-issue-units

把一份咨询记录拆成单个可复用问题。

例如：

- 文科或非典型学历背景，现在转编程还合适吗？
- 非全日制本科能不能申请美国计算机相关硕士？
- 小城市女生该先考研还是先去大城市工作？
- 长期倦怠时，该休息还是重新出发？

一个 issue unit 应该只回答一个问题，包含问题本质、常见背景、回答方向、可复用素材和可进入的主题聚合。

模板：

```text
templates/issue-unit.md
```

### 04-topic-clusters

把重复出现的问题聚成主题。

当前主题：

- `topic-liberal-arts-nontraditional-cs-transition`：文科/非典型学历转码。
- `topic-overseas-study-work-path`：出国读书和海外求职。
- `topic-career-start-rebuild`：职业起步和路径重建。
- `topic-degree-upgrade-stage-priority`：学历提升和阶段排序。
- `topic-family-boundary-self-choice`：家庭影响和自我选择。
- `topic-small-city-women-career`：小城市女性职业起步。
- `topic-consulting-boundaries-collaboration`：咨询流程和边界。

主题页回答：这个主题是什么、重复出现的问题有哪些、典型处境是什么、可复用观点是什么、已有关联记录和问题单元，以及可以长出哪些内容、服务和连接池。

模板：

```text
templates/topic-cluster.md
```

### 05-outputs

把主题转成可直接使用的工作台。

当前输出：

- `content-backlog.md`：内容选题清单，按优先级整理 FAQ、文章、案例。
- `service-offers.md`：服务产品雏形，包括一对一、小圆桌、路径诊断。
- `connection-pool.md`：连接池候选分组，只记录相似处境和连接原则，不公开个人隐私。

这一层不是原始事实层，而是复用层。写公开内容、设计服务或做连接前，都要回到 `02-normalized` 和 `03-issue-units` 检查原始语境。

### 06-article-drafts

放从 `03-issue-units` 和 `04-topic-clusters` 发展出的文章草稿。

这一层仍然是内部草稿，不等于可以直接发布。文章发布前要重新检查：

- 是否暴露个人隐私。
- 是否把个案写成普遍承诺。
- 是否把过来人经验写成官方政策。
- 是否需要查证学校、签证、费用、就业市场等会变化的信息。

### 07-people

放咨询对象和联系方式管理。

这一层默认私密，不进入通用 records 索引。它只服务于关系维护、后续咨询和连接池判断。

当前文件：

- `people.csv`：轻量联系人表。
- `people_candidates.csv`：从已有记录中提取出的联系人候选。
- `person-template.md`：多人次咨询或重要关系可单独建人物档案。

联系方式不要写进文章草稿、问题单元或主题聚合里。

## 推荐工作流

### 新增一份咨询材料

1. 把原始材料放入 `00-inbox/`，或确认它已经在 `00-inbox` 的子目录中。
2. 运行来源扫描：

```bash
python3 scripts/scan_sources.py
```

3. 复制 `templates/normalized-consult.md` 到 `02-normalized/`。
4. 按事实整理成 normalized record。
5. 如果里面有多个可复用问题，再拆到 `03-issue-units/`。
6. 如果同类问题已经反复出现，更新或新增 `04-topic-clusters/`。
7. 如果已经能复用，更新 `05-outputs/`。
8. 如果要写文章，把草稿放到 `06-article-drafts/`。
9. 如果需要保留咨询对象信息，把最少必要信息写入 `07-people/people.csv`。
10. 运行索引：

```bash
python3 scripts/build_index.py
```

### 想写一篇内容

1. 先看 `05-outputs/content-backlog.md`。
2. 选一个具体 FAQ 或文章题目。
3. 回到对应 `03-issue-units/`，只回答一个问题。
4. 再回到相关 `02-normalized/`，确认真实语境和隐私边界。
5. 在 `06-article-drafts/` 写内部草稿。
6. 发布前删除或模糊化姓名、城市、公司、学校、收入、债务、签证、家庭事件等细节。
7. 如果涉及学校政策、签证、学费、就业市场等会变化的信息，发布前必须重新查官方来源。

### 想设计一个服务

1. 先看 `05-outputs/service-offers.md`。
2. 选一个服务方向。
3. 回到对应 topic，检查重复问题和典型处境。
4. 写清楚适合谁、不适合谁、交付什么、不承诺什么。
5. 高敏感议题只做一对一，不做小圆桌。

### 想做连接池

1. 先看 `05-outputs/connection-pool.md`。
2. 只按处境分组，不直接暴露个人信息。
3. 债务、借钱、家暴、抑郁、亲人离世、签证身份、商业机密不进入群体连接。
4. 真实连接前必须获得双方明确同意。
5. 具体联系人和同意状态只记录在 `07-people/`。

## 分类字段

分类规范详见 `taxonomy.md`。常用字段包括：

- `record_type`：资料类型，如 `qa_thread`、`consult_call`、`coaching_session`、`collaboration`、`boundary`、`output`、`article_draft`。
- `primary_theme`：主主题，如 `文科转码`、`出国读书和海外求职`、`早期职业迷茫`、`学历提升和考研`、`家庭影响和自我边界`。
- `layers`：未来可能进入的层级，如 `content`、`service`、`connection`。
- `privacy_level`：隐私级别，如 `private`、`anonymized`、`public_ready`。

## 隐私和边界

默认所有咨询材料都是私密资料。

公开使用前必须检查：

- 姓名、微信号、邮箱、手机号。
- 具体城市、学校、公司、项目、收入。
- 债务、借钱、签证身份、家庭冲突、家暴、抑郁、亲人离世。
- 合作邀约、商业计划、报价、未公开项目。

过来人经验不能替代官方信息。涉及申请、学费、签证、政策、就业市场的内容，只能作为经验和判断逻辑，不能写成确定承诺。
