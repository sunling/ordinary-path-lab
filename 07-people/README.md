# 咨询对象管理

这一层用来管理来咨询或曾经交流过的人：名字、联系方式、简短介绍、关联咨询记录、是否适合后续连接。

`07-people` 默认是私密层，不进入 `scripts/build_index.py` 生成的通用记录索引。原因是这里可能包含姓名、微信、邮箱、手机号和真实身份线索。

## 文件

- `people.csv`：轻量联系人表，适合快速检索和维护。
- `people_candidates.csv`：自动扫描生成的候选表，不能直接当作正式联系人表。
- `person-template.md`：如果某个人后续咨询很多次，可以复制这个模板建立单独档案。

## 使用原则

- 只记录管理咨询关系所需的最少信息。
- 联系方式不要写进 `02-normalized`、`03-issue-units`、`04-topic-clusters` 或 `06-article-drafts`。
- 如果要把某个人放进连接池，必须先确认对方是否愿意被连接。
- 高敏感情况只保留本地私密备注，不进入群体连接。

## 自动生成候选表

运行：

```bash
python3 "对外交流/咨询资料整理/scripts/build_people_candidates.py"
```

这个脚本会从两类地方生成 `people_candidates.csv`：

- `02-normalized` 的 frontmatter 和“她/他是谁”部分。
- `00-inbox` 里的文件名和文件夹名，尤其是 `00-inbox/人生教练` 这类按人名存放的材料。

注意：

- 候选表只是线索，所有行都有 `needs_review=yes`。
- 同一个人多次咨询时，脚本会尽量按 `display_name` 自动合并到同一行，并把多个 `related_records` 和 `source_path` 用分号连接。
- 自动合并仍需人工复查：同名不一定同人，同人也可能使用过不同昵称。
- 从文件名推断出的微信号、昵称或姓名必须人工确认。
- 只有确认过的人，才进入正式 `people.csv`。

## people.csv 字段

- `person_id`：内部 ID，建议 `person-YYYYMMDD-slug`。
- `display_name`：常用称呼，可以是真名、昵称或匿名代号。
- `real_name`：真实姓名；不确定或不想记录可留空。
- `contact_channel`：微信、邮箱、电话、LinkedIn、知乎等。
- `contact_value`：具体联系方式。
- `short_intro`：一句话介绍，例如“26岁，上海，QA，英文环境工作，未来想出国”。
- `primary_theme`：主主题。
- `tags`：关键词。
- `related_records`：关联的 normalized/issue/topic ID。
- `connection_fit`：`yes` / `maybe` / `no`。
- `consent_to_connect`：`yes` / `no` / `unknown`。
- `privacy_level`：通常为 `private`。
- `last_contacted`：最后联系日期。
- `notes`：只写必要备注，避免写过度敏感细节。
- `created` / `updated`：维护日期。

## 连接池判断

适合：

- 处境相似，且信息/经验可以互补。
- 对方表达过希望认识同类人或愿意参与小圆桌。
- 话题风险低，不涉及债务、家暴、抑郁、签证身份、商业机密。

不适合：

- 对方只是一次性咨询。
- 资料高度敏感。
- 对方没有明确连接意愿。
- 连接可能增加对方压力或暴露隐私。
