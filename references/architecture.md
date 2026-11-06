# Architecture

The dashboard is one HTML file, `templates/panel.html`, published as a claude.ai Artifact. It has no build step and no server of its own. At view time it gets three runtime capabilities:

| Capability | Used for | Without it |
|---|---|---|
| `db` | all data (Firestore-like documents, live `onSnapshot`) | read-only template with a banner |
| `sample` | the AI entry box, photo entry, bank parsing, monthly analysis | entry box says Claude is unavailable; everything else works |
| `mcp` | Google Calendar `list_events` / `create_event` / `delete_event`; Gmail `search_threads` / `get_thread` for bank alerts | calendar blocks show dashboard events only; no bank email sync |

Publish declaration:
```json
{
  "db": {}, "user": {}, "sample": {"images": true},
  "mcp": {"servers": [
    {"server": "Gmail", "tools": ["search_threads", "get_thread"]},
    {"server": "Google Calendar", "tools": ["list_events", "create_event", "delete_event"]}
  ]}
}
```
Drop the Gmail entry when the user has no bank alerts. Drop `mcp` entirely when neither connector is connected.

## Code layout (panel.html)
| Area | What it holds |
|---|---|
| `#cfg` JSON | `title`, `lang`, optional `i18n` overrides. The only per-user part baked into the HTML; everything else is in db. |
| `L` | UI strings as `[zh, en]`. `t(key)` picks by `settings.locale.lang`, with `CFG.i18n` winning. |
| `DEFAULTS` + `mergeSettings` | the shape of `settings/main` |
| `BLOCKS` | the registry: `{ size: 'm' or 'l', edge?, render() → HTML }`. `trackerBlock(tr)` builds `tracker:<id>` blocks. |
| `actionSpec` / `validAction` / `runActions` | the AI entry contract (below) |
| `render()` | redraws the current page from state and keeps typed input values by element id. Clicks are delegated through `data-act`. |
| `connect()` | `claude.use('db' / 'sample' / 'mcp')` and one subscription per collection |

## Data model (db)
| Path | Fields |
|---|---|
| `settings/main` | `profile{name,about}`, `locale{lang,currency,weekStart}`, `ui{scale}`, `layout{pages:[{id,name,blocks[]}]}`, `checks[{k,n,goal}]`, `trackers[{id,name,kind,unit,goal,period,chart}]`, `cats[{k,n,budget}]`, `budget`, `goals{workout}`, `workouts[]`, `rotation[]`, `food{protein,kcal}`, `weightUnit`, `templates[7]` (Monday first; lines `HH:MM-HH:MM text #kind`), `bank{query}` |
| `days/{YYYY-MM-DD}` | `checks{k:true}`, `workouts[{type,mins}]`, `food[{n,p,k,at}]`, `weight`, `override` (that day's plan text) |
| `todos/{id}` | `text`, `done`, `doneAt`, `urgency` 1–3, `due`, `repeat{freq,monthday,remind}`, `lastDone`, `createdAt` |
| `events/{id}` | `title`, `date`, `start`, `end`, `location`. Only used when Google Calendar is not available. |
| `sleeps/{id}` | `bed`, `wake` (ISO; wake null while asleep), `src` |
| `expenses/{id}` | `date`, `month`, `amount`, `cat`, `note` or `merchant`, `src` (`manual` / `bank`), `ignored`, `createdAt`. Ids: `bank-<email message id>`, `paste-<ref>`, or random. |
| `recurring/{id}` | `name`, `amount`, `cat` |
| `income/{id}` | `date`, `month`, `amount`, `from`, `note` |
| `savgoals/{id}` | `name`, `target`, `saved`, `date` |
| `insights/{YYYY-MM}` | `headline`, `points[]`, `tips[]` |
| `deadlines/{id}` | `title`, `date`, `note`, `done` |
| `reviews/{weekStart date}` | `good`, `bad`, `next` |
| `jobs/{id}` | `company`, `title`, `status`, `url`, `updated_at` |
| `entries/{trackerId_date}` | `tracker`, `date`, `value` (for count, number, check and rating) |
| `entries/{random}` | `tracker`, `date`, `text` (for list) |
| `sync/bank` | `seen[]` thread ids, `lastAt` |

Claude reads and writes all of these with the ArtifactData tool, which is how the morning brief works. Seeds always go in after publish, never into the HTML.

## AI entry contract
`planEntry` sends one prompt to `sample.json` with:
- today's date;
- the user's `about`;
- `actionSpec()`: only the record types whose blocks are enabled, plus the user's own habits, trackers and categories;
- `dashFacts()`: open to-dos with ids, uncategorized transactions with ids, today's and tomorrow's plan, deadlines, weekly progress.

Claude returns `{"actions":[...],"reply":"..."}`. `validAction` rejects anything malformed or pointing at ids that do not exist, and at most 8 actions are kept. `runActions` writes each one and pushes an undo closure; the toast's Undo runs them in reverse. Deletions show a confirm preview first.

To add a record type, extend all three functions. customize.md has the recipe.

## Two writers, same ids
Both the page ("Sync bank emails") and the morning brief write bank transactions as `expenses/bank-<message id>`. Neither overwrites an existing document, so they never double-count or clobber a category the user picked.
