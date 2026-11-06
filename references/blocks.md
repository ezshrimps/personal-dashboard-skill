# Block catalog

Every block has a fixed look. Users choose which blocks appear on which page and in what order: in the page under Settings → Pages and blocks, or in `settings.layout.pages[].blocks` (an array of block ids).

## Today
| id | Shows | Good for |
|---|---|---|
| `entry` | One-sentence AI entry box plus photo (food or receipt). Turns text into records with one-tap undo. Only offers record types for blocks that are on. | everyone; put it first on home |
| `now` | What is happening now and the next three things, from the day plan and calendar | people with a routine |
| `timeline` | The selected day's plan: weekly template + calendar + one-off changes. Editable as text. | students, office workers |
| `todos` | To-dos with urgency, due dates and recurring reminders (daily/weekly/monthly/yearly) | everyone |
| `calendar` | The next 7 days from Google Calendar plus dashboard events | anyone with a calendar; older users |

## Habits and health
| id | Shows |
|---|---|
| `checks` | Daily habit ticks from `settings.checks`, with x/goal this week |
| `week` | Weekly grid of habits, exercise and daily trackers |
| `sleep` | "Going to sleep" / "I'm up" buttons, last night, 7-night average, 14-night bars |
| `workout` | Exercise this week vs `goals.workout`, one chip per type in `settings.workouts`; suggests the next item when `settings.rotation` is set (e.g. Push/Pull/Legs) |
| `food` | Protein and calories vs `settings.food`, from the entry box or photos (AI estimates) |
| `weight` | Latest weight and a 30-point trend |

## Money
| id | Shows |
|---|---|
| `spend` | Month to date vs budget and on-pace amount, by category with optional category budgets |
| `txns` | This month's transactions, uncategorized bank transactions with one-tap categories, "paste statement / SMS" import, "sync bank emails" when a bank query is set |
| `recurring` | Monthly fixed bills, counted in the month total |
| `income` | Income this month |
| `savings` | Savings goals with progress |
| `insight` | On-demand Claude analysis of the month |

## Planning
| id | Shows |
|---|---|
| `deadlines` | Countdown cards: exams, applications, visa or ID renewals, bills, anything with a hard date |
| `review` | Weekly review: what went well, what to improve, next week's focus |
| `jobs` | Application tracker: want → applied → interview → offer / rejected |

## Custom trackers: `tracker:<id>`
Defined in `settings.trackers`, one block each:

| kind | Input | Period total |
|---|---|---|
| `count` | +1 / −1 buttons, or "drank 2 glasses" in the entry box | sum |
| `number` | type a value | sum |
| `check` | tick once a day | days ticked |
| `rating` | 1–5 | average |
| `list` | add text items (books, ideas, gratitude) | items |

Fields:
- `goal` applies per `period`, which is `day`, `week` or `month`.
- `chart` is `bar` (14-day bars), `streak` (adds a streak count) or `none`.

## Starting layouts (templates/presets)
| preset | Home | Other pages |
|---|---|---|
| student | entry, now, todos, deadlines, checks, timeline, vocabulary tracker | money, plan |
| worker | entry, now, todos, timeline, checks, sleep | money, health |
| jobseeker | entry, todos, jobs, deadlines, checks, applications tracker | money, plan |
| freelancer | entry, now, todos, deadlines, timeline, billable-hours tracker | money (income first), plan |
| health | entry, sleep, workout, food, checks, todos, meds tracker | health, money |
| family | entry, todos, calendar, spend, medicine + blood pressure trackers; text at 130% | (one page only) |
