"""Build a personal dashboard from a profile.

    python build.py profile.json OUT_DIR [--mock]

Writes OUT_DIR/settings.json (the db doc settings/main) and OUT_DIR/panel.html (the page to publish).
--mock also writes OUT_DIR/preview.html: the page with an in-memory stand-in for window.claude, for a local look before publishing.

profile.json (all fields optional except preset):
  preset        student | worker | jobseeker | freelancer | health | family | blank
  lang          "zh" | "en" | any BCP-47 code (other languages need "i18n": {key: text} and translated names)
  currency      ISO code, e.g. "CNY", "GBP"
  weekStart     1 = Monday, 0 = Sunday
  title, name, about, budget, bankQuery
  addBlocks     {"pageId": ["blockId", ...]}   append blocks to a page (creates the page if new)
  removeBlocks  ["blockId", ...]               drop from every page
  checks / trackers / cats / workouts / rotation / templates / goals / food / weightUnit / scale   override the preset
  i18n          {key: text} UI strings for languages other than zh/en
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / 'templates'


def pick(v, lang):
    """Presets keep names as {"zh":..,"en":..}; choose the user's language (English for anything else, Claude translates afterwards)."""
    if isinstance(v, dict) and set(v) <= {'zh', 'en'} and v:
        return v.get(lang) or v.get('en') or next(iter(v.values()))
    if isinstance(v, list):
        return [pick(x, lang) for x in v]
    if isinstance(v, dict):
        return {k: pick(x, lang) for k, x in v.items()}
    return v


def make_settings(prof):
    lang = prof.get('lang', 'zh')
    pid = prof.get('preset', 'blank')
    pre = json.loads((TPL / 'presets' / f'{pid}.json').read_text(encoding='utf-8')) if pid != 'blank' else {
        'layout': {'pages': [{'id': 'home', 'name': '', 'blocks': ['entry', 'now', 'todos', 'checks']}]}, 'checks': [], 'trackers': [],
        'goals': {'workout': 0}, 'workouts': [], 'rotation': [], 'food': {'protein': 0, 'kcal': 0}, 'ui': {'scale': 1}, 'templates': [''] * 7}
    pre = pick(pre, 'zh' if lang == 'zh' else 'en')
    s = {
        'profile': {'name': prof.get('name', ''), 'about': prof.get('about', '')},
        'locale': {'lang': lang, 'currency': prof.get('currency', 'USD'), 'weekStart': prof.get('weekStart', 1)},
        'ui': {'scale': prof.get('scale', pre['ui']['scale'])},
        'layout': pre['layout'],
        'checks': prof.get('checks', pre['checks']),
        'trackers': pre['trackers'] + prof.get('trackers', []),
        'cats': prof.get('cats', []),
        'budget': prof.get('budget', 0),
        'goals': {**pre['goals'], **prof.get('goals', {})},
        'workouts': prof.get('workouts', pre['workouts']),
        'rotation': prof.get('rotation', pre['rotation']),
        'food': {**pre['food'], **prof.get('food', {})},
        'weightUnit': prof.get('weightUnit', 'kg'),
        'templates': prof.get('templates', pre['templates']),
        'bank': {'query': prof.get('bankQuery', '')},
    }
    pages = s['layout']['pages']
    rm = set(prof.get('removeBlocks', []))
    for p in pages:
        p['blocks'] = [b for b in p['blocks'] if b not in rm]
    for pg, blocks in prof.get('addBlocks', {}).items():
        page = next((p for p in pages if p['id'] == pg), None)
        if not page:
            page = {'id': pg, 'name': '', 'blocks': []}
            pages.append(page)
        page['blocks'] += [b for b in blocks if b not in page['blocks']]
    # A tracker the user added must be visible somewhere.
    shown = {b for p in pages for b in p['blocks']}
    for t in prof.get('trackers', []):
        if 'tracker:' + t['id'] not in shown:
            pages[0]['blocks'].append('tracker:' + t['id'])
    return s, pre.get('brief', [])


def main():
    prof_path, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    mock = '--mock' in sys.argv
    prof = json.loads(prof_path.read_text(encoding='utf-8'))
    settings, brief = make_settings(prof)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'settings.json').write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'brief_sections.json').write_text(json.dumps(brief), encoding='utf-8')
    cfg = {'title': prof.get('title', ''), 'lang': settings['locale']['lang']}
    if prof.get('i18n'):
        cfg['i18n'] = prof['i18n']
    title = prof.get('title') or ('我的面板' if settings['locale']['lang'] == 'zh' else 'My dashboard')
    html = (TPL / 'panel.html').read_text(encoding='utf-8')
    html = html.replace('{{TITLE}}', title.replace('<', '')).replace('{{CONFIG_JSON}}', json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/'))
    (out / 'panel.html').write_text(html, encoding='utf-8')
    if mock:
        shim = (ROOT / 'dev' / 'mock-claude.js').read_text(encoding='utf-8')
        seed = json.dumps({'settings/main': settings}, ensure_ascii=False).replace('</', '<\\/')
        page = ('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1">'
                f'</head><body><script>window.__SEED__={seed};</script><script>{shim}</script>{html}</body></html>')
        (out / 'preview.html').write_text(page, encoding='utf-8')
    print(f'wrote {out}/settings.json, panel.html' + (', preview.html' if mock else ''))


if __name__ == '__main__':
    main()
