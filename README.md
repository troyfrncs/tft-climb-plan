# TFT Climbing Plan

A personal Teamfight Tactics study guide for 777G0D (SEA): four comps arranged as a 2×2 grid (AD or AP items × strong or weak start), each with its final board, items, augments, level timings and best openers, plus five rules aimed at fixing busting and early spending.

It's a reference to read between games. It doesn't connect to the game or read live match data.

## How it works

- `index.html`: the whole app (HTML, CSS and JS in one file, no build step).
- `data/meta.json`: everything the page shows. To update the comps, edit this file, then run `python3 tools/icons.py` to refresh the champion, item and augment images.

To run it locally:

```
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Updating for a new patch

A scheduled Claude task checks for new TFT patches. When one comes out, it researches the new meta, rewrites `data/meta.json` and pushes the change. When a new set launches (Set 19 on 1 Dec 2026), it replaces all four comps.

Game images are loaded from CommunityDragon. TFT Climbing Plan isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
