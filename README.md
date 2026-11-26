# THE WORLD TODAY — 26 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/jakwifiid78-png/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/jakwifiid78-png/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

An entry for the make.fun bounty [Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126).

`main.py` draws a complete newspaper front page — masthead, dateline,
main headline, stories and a news ticker — as a single 1024×1024 PNG
that sums up the world news of **Thursday, 26 November 2026**:

- **Washington** — President Trump announces new tariffs on 14 trading
  partners after an excess-capacity probe; China, the EU and India are
  among those targeted, and Jakarta weighs a reply to a proposed 18% rate.
- **Cairo** — a fuel tanker overturns and burns on the Ring Road in
  Giza, killing at least 31 people.
- **Jakarta** — President Prabowo watches police destroy 601.7 tons of
  seized narcotics worth Rp61.68 trillion.
- **Bogor** — 13 miners die in the illegal Pongkor gold mine.
- **Markets** — the rupiah slides past Rp18,380 per US dollar.
- In the ticker: Kyiv, Gaza, Brussels, the FCC's SpaceX satellite
  decision, and North Korea's nuclear signalling.

The drawing is deterministic — fixed text and layout, no clocks, no
randomness — so every run writes byte-identical output. The program
uses only the Python standard library plus Pillow; if Pillow is not
available it copies the bundled `entry.png`, which this program drew.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024×1024, under 1 MiB)
```

Without `MAKEFUN_OUTPUT_DIR` it writes to `/output/entry.png`, as the
make.fun grader expects.

## License

MIT — see [LICENSE](LICENSE).

---

Built for [make.fun](https://make.fun/bounty/news-image-20261126).
Join via my referral link: https://make.fun/r/n0n6z7h3
