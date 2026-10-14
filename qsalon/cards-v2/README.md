# Q Salon GBP post cards (v2, locked layout)

Regenerate all 90 cards: `python3 make_cards_json.py && node render.mjs` (needs Playwright; set PW_REQUIRE to a package.json whose node_modules has playwright).
Output goes to `out/`; copy to `../cards/` (the post engine pulls `qsalon/cards/qNN.png` from GitHub raw).

Layout rules (do not change per card):
- 1200x900. Eyebrow on one line (area name dropped if it won't fit). Headline max 2 lines (full) / 3 lines (split), auto-shrinks. Hand-written dek per card in `card_copy.py`, never truncated.
- Full-width navy "type" card: 96px side margins, footer rule with brand + CTA pill.
- Split cards: text 600px left, picture 600px right. Product posts show the real product photos (`PRODUCTS`), Meet Susy posts show Susy's photo (`SUSY`), gift posts show the gold gift card (`GIFT`).
