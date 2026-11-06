# Interview: from a conversation to profile.json

Talk in the user's language. Ask 3–4 questions per round, as multiple choice where you can, and let them skip anything. Two rounds are usually enough. Never ask for passwords, card numbers or bank logins.

## Round 1: who and where
| Ask | Fills |
|---|---|
| What best describes you right now? (student / working / job hunting / freelance or own business / health is the focus / setting this up for a parent or older family member / something else) | `preset` (see the mapping below) |
| Where do you live, and which language should the dashboard use? | `lang`, `currency`, `weekStart` (Monday for most of the world; Sunday for the US, Canada, Japan, Israel and others when the user prefers it), and the timezone for the brief |
| What are the 3 things you most want to keep on top of every day? | which blocks to add, `checks`, `trackers` |
| What should the dashboard call you, and anything about your situation the AI should know? (one or two sentences: school or job, city, goals) | `name`, `title`, `about` |

Preset mapping:
- student → `student`
- working → `worker`
- job hunting → `jobseeker`
- freelance / founder → `freelancer`
- health → `health`
- parent or older user → `family`
- unclear → the closest one, or `blank`

## Round 2: money, calendar, brief
| Ask | Fills |
|---|---|
| Do you want to track spending? Monthly budget? | keep or remove the money blocks; `budget`; `cats` if they want their own categories |
| Does your bank send an email for each card transaction? Which address do they come from? | `bankQuery` such as `from:alerts@yourbank.com`; see bank-alerts.md when they are unsure |
| Do you use Google Calendar? | `calendar` block; nothing to configure |
| Do you want a morning email? At what time, and to which address? | the brief task (step 4 of SKILL.md) |

## Then show the plan before building
List each page and its blocks in plain words, using blocks.md for the names, plus the daily habits and trackers. Ask the user to tick, untick or add.

Anything they mention that no block covers goes through "Needs outside the presets" in SKILL.md.

## profile.json example
```json
{
  "preset": "student", "lang": "zh", "currency": "CNY", "weekStart": 1,
  "title": "小林的面板", "name": "小林", "about": "大二学生，在上海读计算机，明年考雅思。",
  "budget": 2500, "bankQuery": "",
  "addBlocks": { "home": ["sleep"] }, "removeBlocks": ["timeline"],
  "trackers": [{ "id": "twater", "name": "喝水", "kind": "count", "unit": "杯", "goal": 8, "period": "day", "chart": "bar" }]
}
```

Field rules:
- `checks` replaces the preset's habits, each entry `{k, n, goal}`:
  - `k` is a short ascii key that must never change;
  - `goal` is days per week, 1–7.
- `trackers` are added on top of the preset's. Each `id` is a short ascii id that must never change.

For a language other than zh or en, also add `"i18n": {...}`: translate every key of the `L` table in `templates/panel.html`. For array values (`wd`), translate each item. Also translate the preset names in the resulting `settings.json`.
