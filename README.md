# World in One Day — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Kinanty22/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Kinanty22/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A program that draws one newspaper front page summing up the world news
of **Monday 23 November 2026** — and writes it to `entry.png`.

## The day, in six stories

1. **Ukraine sinks Russian warship off Libya** — Zelensky confirmed
   on Monday that seven sea drones sank the corvette Merkury at
   Benghazi and hit the cargo ship MV Angara. A second Russian
   cargo ship was hit in the Baltic Sea.
2. **Nvidia: Huang returns, shares soar 30%** — Nvidia's board
   reinstated Jensen Huang as chief executive on Monday; shares
   surged about 30%, leading an AI-stock rally on Wall Street.
3. **15 killed as Russia strikes Kyiv region** — Russian missile
   and drone strikes killed at least 15 people; a boy was pulled
   alive from the rubble. NATO was set to meet on Monday.
4. **US sanctions Iran's shadow banks** — the US Treasury hit
   more than two dozen Iranian exchange houses and front
   companies. Tehran vowed to counter the US blockade of Hormuz.
5. **24 dead in Indonesia factory fire** — a sweets factory fire
   in Cikande, Banten killed 24; about 30 are still missing. The
   death toll was confirmed on Monday.
6. **Plus:** AI helped prove the Riemann hypothesis, Anthropic
   says; the EU proposed new Russia sanctions on banks, crypto
   and sports; Bitcoin fell to about $55,100, its lowest since
   September 2024.

Sources: Reuters, BBC, CNN, AP, WSJ, The Times — 23 November 2026.
Every fact was checked against reporting published on the day.
COP31 is not in the image: it ended on Sunday 22 November.

## How it works

`main.py` is pure Python 3 standard library — no packages, no network.
It draws the front page with its own rasteriser (rectangles, lines,
circles, polygons and a built-in 5×7 bitmap font) and encodes the PNG
by hand with `zlib`, so two runs produce byte-identical output.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: `out/entry.png`, 1024×1024 PNG, about 24 KB (limit: 1 MiB).

## Entry

- Competition: [news-image-20261123](https://make.fun/c/news-image-20261123)
  — "Sum up 23 November's world news in one image"
- Entrypoint: `main.py` (Python 3.13, standard library only)
- License: MIT (see `LICENSE`)

---

<sub>Entered on [make.fun](https://make.fun/?ref=mjp730py&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
