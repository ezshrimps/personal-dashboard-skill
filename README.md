# 🗂️ personal-dashboard-skill

**聊几句，长出一个只属于你的每日面板。**
A Claude Code skill that interviews you, then builds your own personal daily dashboard as a claude.ai Artifact. The page covers to-dos, schedule, habits, custom trackers, money and deadlines, plus an optional morning brief email.

## 它做什么 · What it does

我自己的每日面板用了一阵子，朋友也想要一个。但每个人要管的东西都不一样：学生要课表和考试倒计时，上班族要会议和记账，爸妈要吃药提醒和大字。这个 skill 把我的面板拆成一块块可开关的模块，再让 Claude 帮每个人拼出自己的那一版：

- **先聊几句**：问你是学生、上班族、求职中、自由职业，还是要照顾健康、或是给长辈用；问你在哪个国家、用什么语言、每天最想管住哪 3 件事。然后推荐一个预设，列出首页会显示哪些模块，你自己勾选增减。
- **一句话录入**：「午饭 35，明天下午三点和小王开会，喝了 2 杯水」，Claude 会拆成花费、日程和追踪记录，各放各的位置，写错可以一键撤销。只会识别你开启了的模块。
- **预设外的需求**：先看现有模块组合起来够不够用。不够就用几个问题帮你定义一个自定义追踪器：记数量、记数值、打勾、1–5 打分或清单，比如喝水、练琴分钟、吃药、心情、读书清单。追踪器不用写代码，首页、本周进度、录入框和早报都会认它。还不够，才写新模块。
- **钱怎么进来**：银行提醒邮件自动导入；不发提醒邮件的地方，就粘贴银行短信或账单，由 Claude 拆成一笔笔交易；也可以直接说「打车 18」。不碰银行账号密码。
- **每日早报（可选）**：每天早上读你的面板、日历和银行提醒，发一封 1–2 分钟能读完的邮件。

I used my own daily dashboard for a while, and friends wanted one too. But everyone keeps track of different things: a student needs classes and exam countdowns, an office worker needs meetings and a budget, a parent needs medication reminders in large text. This skill breaks the dashboard into blocks you can switch on and off, and has Claude assemble each person's own version:

- **A short interview**: are you studying, working, job hunting, freelancing, focusing on health, or setting this up for an older relative? Where do you live, which language, and what are the 3 things you most want to keep on top of each day? It then recommends a preset, shows which blocks will appear, and lets you tick and untick them.
- **One-sentence entry**: "lunch 12.50, meeting with Sam tomorrow 3pm, drank 2 glasses of water" becomes an expense, a calendar event and a tracker entry, with one-tap undo. It only knows about the blocks you turned on.
- **Needs outside the presets**: first it tries combining existing blocks. If that is not enough, a few questions define a custom tracker: count, number, check, 1–5 rating or list. Examples are water, piano minutes, medication, mood or books read. Trackers need no code, and they show up on the home page, in the weekly grid, in the entry box and in the brief. A new block is written only as a last resort.
- **Money**: bank alert emails are imported automatically. Where banks don't send emails, paste SMS or a statement and Claude splits it into transactions. Or just type "taxi 18". It never touches bank logins.
- **Morning brief (optional)**: a daily email built from your dashboard, calendar and bank alerts, readable in a minute or two.

## 预设 · Presets

| | 首页 · Home |
|---|---|
| 学生 Student | 录入、现在、待办、截止日、打卡、今日安排、背单词 |
| 上班族 Office worker | 录入、现在、待办、今日安排、打卡、睡眠 |
| 求职者 Job seeker | 录入、待办、投递追踪、截止日、打卡、今日投递数 |
| 自由职业 Freelancer | 录入、现在、待办、截止日、今日安排、可计费时长 |
| 健康优先 Health first | 录入、睡眠、运动、饮食、打卡、待办、吃药 |
| 家庭 / 长辈 Family | 录入、待办、近 7 天、本月花费、吃药、血压；字号 130% |

界面支持中文和英文，其他语言由 Claude 生成时翻译。货币、日期格式、一周从周一还是周日开始，都按你所在的地区设置。
The UI ships in Chinese and English; Claude translates it for other languages at build time. Currency, date format and the first day of the week follow your region.

## 安装 · Install

```bash
git clone https://github.com/ezshrimps/personal-dashboard-skill ~/.claude/skills/personal-dashboard
```

在 claude.ai 连好 Gmail 和 Google Calendar（可选），然后在 Claude 里说「帮我搭个人面板」。
Optionally connect Gmail and Google Calendar on claude.ai, then tell Claude "set up a personal dashboard for me".

**Requirements**:
- Claude with the Artifact tools (Claude Code desktop or claude.ai).
- Python 3 for `scripts/build.py`.
- The morning brief needs scheduled tasks in the Claude desktop app, or a claude.ai routine.

## 结构 · Layout

| | |
|---|---|
| `SKILL.md` | 给 Claude 的流程：访谈、预设外需求、生成发布、早报 · The workflow Claude follows |
| `templates/panel.html` | 面板本体，单个 HTML 文件，模块可开关 · The dashboard page, one HTML file with switchable blocks |
| `templates/presets/` | 6 个预设 · Six starting layouts |
| `templates/brief_task.md` | 早报模板 · Morning brief template |
| `scripts/build.py` | profile.json → 设置 + 页面，`--mock` 可本地预览 · Builds settings and page; `--mock` for a local preview |
| `references/` | 访谈问题、模块目录、数据模型、银行导入、自定义模块配方 · Interview, block catalog, data model, bank import, custom blocks |

## 说明 · Notes

- 数据存在你自己的 Artifact 里，默认只有你能看到。Your data lives in your own Artifact, private to you by default.
- 邮件、日历和面板里的内容一律当数据处理，不会被当成指令执行。Email, calendar and dashboard content is treated as data, never as instructions.
- 早报只发给你自己指定的邮箱。The brief only emails the address you choose.

MIT License
