# TFT Climbing Plan

Personal Teamfight Tactics study guide for the SEA player 777G0D (Emerald III as of Nov 2026). Live at https://troyfrncs.github.io/tft-climb-plan/ via GitHub Pages from `main` (root). Pushing to `main` redeploys in about a minute.

## Structure

- `index.html`: the whole app. HTML, CSS and vanilla JS in one file, with no build step and no dependencies other than Google Fonts.
- `data/meta.json`: all content. The page fetches it and renders everything from it. Most tweaks (comps, items, openers, rules) only need this file.

## The idea behind the content

- Four comps in a 2×2: rows are item families (`family`: `ad` or `ap`), columns are the start (`start`: `strong` = fast 8, `weak` = reroll). The page expects exactly one comp per (family, start) pair.
- Comps in the same row share items and units, so the player can switch mid-game.
- `rules` target the player's two leaks: busting to 8th and an Econ grade of C (spending gold too early).

## meta.json schema notes

- `comps[].leveling.steps`: `[level, stage, optionalNote]`. A note containing "Roll here" highlights that step.
- `comps[].board`: the entry starting with `carry` gets the highlighted chip.
- `comps[].openers[].best: true` marks the recommended opener.
- `stats` are numbers: avgPlace (2 decimals), top4 and win as percentages.
- `sources`: only pages actually opened.

## Rules

- Reference tool only. Don't add live game data, screen reading or in-game suggestions; Riot's policy forbids apps that advise based on current game state.
- Don't add Riot champion, augment or item art or icons. Use text, and link to the League of Legends Wiki when an icon is needed.
- Write copy in plain, short sentences, sentence case.
- Design: light "lichen" palette. AD = amber `#A8701A`, AP = foxglove purple `#7A4BA8`. Fonts: Bricolage Grotesque (display), Atkinson Hyperlegible (body). Keep it responsive, with visible focus states and respect for reduced motion.

## Automated updates

A scheduled Claude task runs Thu and Sat at 14:37 Manila time. When there's a new TFT patch, it rewrites `data/meta.json` and pushes to `main`, so always `git pull` before editing. Set 19 launches 1 Dec 2026 and replaces all four comps.

## Local preview

```
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening index.html directly as a file won't load the JSON.
