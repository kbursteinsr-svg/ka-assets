import json
from card_copy import DEK, PRODUCTS, SUSY, GIFT, SUMMARY_FIX
rows = json.load(open('rows.json'))
CTA = {'BOOK': 'Book with Susy', 'SHOP': "Shop Susy's picks", 'CALL': '(941) 340-2389', 'LEARN_MORE': 'Read more'}
THEME = {'Color for the holidays': 'Holiday color'}
out = []
for r in rows:
    d = r['day']
    kind = 'product' if d in PRODUCTS else 'susy' if d in SUSY else 'gift' if d in GIFT else 'type'
    theme = THEME.get(r['theme'], r['theme'])
    out.append({'day': d, 'kind': kind, 'theme': theme, 'geo': r['geo'], 'title': r['title'],
                'dek': DEK[d], 'cta': ('Give a gift card' if d in GIFT and r['cta'] != 'CALL' else CTA.get(r['cta'], 'Book with Susy')), 'call': r['cta'] == 'CALL',
                'products': PRODUCTS.get(d, []), 'photo': SUSY.get(d)})
json.dump(out, open('cards.json', 'w'), indent=1)
print(len(out), {k: sum(1 for c in out if c['kind'] == k) for k in ('product', 'susy', 'gift', 'type')})
