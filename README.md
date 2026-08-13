# Government of Malta — Structure Register

Maps Malta's 22 government ministries and their officially appointed bodies (boards, committees,
authorities, agencies, companies), with individual bio pages for identified chairs, CEOs, and board
members. Cross-checked against the Malta Data Portal's AdminRegister API, gov.mt, and ministry/news
sources.

## Status (13 Aug 2026)

This repository holds the full production dataset: 22 ministries, ~400 entities, 17 fully or partially
researched chair/CEO/board records, and 63 individual bio pages.

Most recently updated: **Pierre Fenech** (CEO, Institute of Tourism Studies) — expanded with full career
history, education, both public controversies (the 2019 Rosianne Cutajar consultancy and the 2021 ITS
architect order), and a complete source list. The Mediterranean Conference Centre entry reflects his
March/April 2025 handover of that role to **Nigel Vella**.

## Architecture

- `index.html` — static shell (vanilla JS) that fetches `data.json` at runtime and renders the register
  client-side: ministry list with completion %, expandable entity lists, and a searchable People
  Directory.
- `data.json` — combined data layer: `ministries[]` (name, abbreviation, minister, entity list) and
  `chairs{}` (keyed by entity name, holding chair/CEO/board data, per-person bios, and source URLs).
- `bios/` — individual bio HTML pages, one per person with a `bios{}` entry in `data.json`, generated
  from the same content. Filename pattern: `bios/{slug(entity)}-{slug(person)}.html`, matching the
  `bioHref()` function in `index.html` exactly.

## Updating

1. Edit `data.json` (add/update entries under `chairs`).
2. Regenerate bio pages for changed entries (or hand-edit the specific `bios/*.html` file to match).
3. Keep `index.html`'s `bioHref()`/`slug()` logic in sync with the filename pattern above — if either
   changes, "Read bio" links will 404.
4. Deploy `index.html`, `data.json`, and the full `bios/` folder together — this is a static snapshot,
   so partial deploys will remove files not included.
