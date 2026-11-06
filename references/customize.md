# Needs outside the presets

When a user wants something that is not in blocks.md, try these in order and stop at the first that works.

## 1. Rearrange
Most requests are already covered by an existing block under another name.

| User wants | Use |
|---|---|
| exam countdown, visa renewal, bill due date | `deadlines` |
| medication reminder at a time | a recurring to-do, or a `check` tracker |
| class timetable | the weekly schedule template |
| reading log | a `list` tracker |

Add the block to the page they want with `addBlocks`, or in the page's settings.

## 2. Make a tracker (no code)
Anything that is "a number", "a tick", "a 1–5 score" or "a list of things" per day, week or month is a tracker. Ask the user:
1. A name.
2. What they record: an amount to add up (`count`), a measurement (`number`), done or not done (`check`), a 1–5 score (`rating`), or text items (`list`).
3. The unit and goal.
4. Whether the goal is per day, week or month.
5. Whether they want a streak.

Examples:
- water 8 glasses/day → count
- piano 150 min/week → number
- took vitamins → check, with streak
- mood → rating
- books read → list
- baby feeds → count
- savings deposits → number, per month
- language lessons → check

The tracker shows up as its own block, in the weekly grid when it is daily, in the brief, and in the AI entry box ("practised piano 40 min").

To add one, append it to `settings.trackers` and its block id `tracker:<id>` to a page. Use ArtifactData `update` on `settings/main` with both fields, after reading the current version. Or let the user do it themselves in Settings, using the one-line format `name, kind, unit, goal, period`.

## 3. Write a new block (code)
Use this only when the need has its own structure, for example:
- a pet care log with several fields per entry;
- a shared shopping list;
- a plant watering schedule per plant.

Work on the user's own copy of `panel.html`, then republish to the same artifact URL.

1. **Data.** Pick a collection name and fields. Add one subscription in `connect()`:
   ```js
   sub(db.collection('pets'), l => { S.pets = l; })
   ```
   Add `pets: []` to `S`.
2. **Block.** Add an entry to `BLOCKS`:
   ```js
   pets: { size: 'm', render: () => `...` }
   ```
   - Build the HTML with `esc()` around every user value.
   - Give each input an `id` so it survives live re-renders.
   - Use `data-act="..."` on buttons.
   - Reuse the existing classes: `card`, `li`, `list`, `kpis`, `meter`, `bar`, `chip`, `pill`, `field`, `inrow`.
3. **Strings.** Add `b_pets` and `b_pets_d` to `L` as `[zh, en]`, plus any labels.
4. **Clicks.** Handle the new `data-act` values in the click listener. Write through `write(db => ...)` and pass an undo to `toast(msg, undo)` where the change can be undone.
5. **Entry box (optional).** Add the record type in three places:
   - a line in `actionSpec()`, only when the block is enabled;
   - a validator in `validAction`;
   - a branch in `runActions` that writes the record and pushes its undo.
6. **Brief (optional).** Add a `## Section` to the user's brief prompt that reads the new collection.
7. **Check.**
   - Rebuild with `scripts/build.py profile.json out --mock`.
   - Open `out/preview.html` and exercise the block: add, undo, reload.
   - Run `node --check` on the script.
   - Republish.

Keep new blocks inside the same visual system. Do not add external libraries or new fonts.
