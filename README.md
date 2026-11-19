# The World in One Page — Wednesday 18 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kampret44/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kampret44/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

An entry for the [make.fun bounty "Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118).

## The image

`entry.png` (1024×1024) is a front-page newspaper summing up **Wednesday
18 November 2026** in twelve stories across six continents:

1. **Xi meets Putin in Shenzhen** at APEC, with a Trump trilateral set for
   Thursday 19 November
2. **US strikes an Iranian missile site on Qeshm Island**; Iran answers with
   drone attacks on US bases in Bahrain and Kuwait
3. **Ukraine hits the Kerch bridge again**; part of the road span collapses
4. **Mary Peltola wins the Alaska Senate seat**; Democrats take a 56–44
   majority
5. **US loses measles elimination status** after 26 years (5,412 cases)
6. **Ebola in DR Congo passes 11,000 cases**
7. **Voyager 1 reaches one light-day from Earth**
8. **Quad leaders meet in Manila**, first leader-level meeting in 2+ years
9. **EU proposes a €45bn loan for Ukraine** in 2027
10. **Nvidia's board rejects Jensen Huang's return as CEO**, on a record
    $115.8bn quarter
11. **OpenAI launches GPT-6.2 Astra and Sol**
12. **Cyclone Akvan** strengthens in the Bay of Bengal

A world-map panel marks where each story happened. Every fact on the page
was verified against live reporting (AP, Reuters, AFP, Euronews, NASA, WHO,
PAHO) on 18–19 November 2026.

## How it is built

The page is drawn entirely in code — no AI image generation, so the text
stays crisp and legible. `render.py` renders `entry.png` with Pillow
(1024×1024, ~165 KB PNG); `main.ts` is the entrypoint and copies
`entry.png` to `/output/entry.png` at grade time. No network is used at
runtime.

```sh
python3 render.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # run the entrypoint
```

## License

MIT — see [LICENSE](LICENSE).
