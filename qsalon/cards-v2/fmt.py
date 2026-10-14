"""Locked text format for Q Salon Google posts.
Hook line on its own, short body paragraphs (one idea each), call to action last,
a blank line between every block. Lists use bullet lines. Hand-written versions in
OVERRIDE win; everything else goes through fmt()."""
import json, re
CTA = re.compile(r"^(book|call|shop|read|see|order|reserve|find|ask|grab|gift cards available|full guide|susy's full)\b", re.I)
def sents(s):
    s = re.sub(r"\s+", " ", s).strip()
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9$])", s) if x]
def fmt(s):
    if "\n" in s: return s.strip()
    ss = sents(s)
    if len(ss) == 1: return ss[0]
    cta = [ss.pop()] if len(ss) > 1 and CTA.match(ss[-1]) else []
    paras, cur = [ss[0]], ""
    for x in ss[1:]:
        cur = (cur + " " + x).strip()
        if len(cur) >= 70: paras.append(cur); cur = ""
    if cur:
        if len(paras) > 1 and len(cur) < 40: paras[-1] += " " + cur
        else: paras.append(cur)
    return "\n\n".join(paras + cta)

OVERRIDE = {
 4: "Susy's picks are in the Q Shop.\n\nChosen for men's hair and Siesta Key humidity:\n• Pomades and styling clay\n• Beard care\n• Sulfate-free scalp care\n• Fragrance\n• A body grooming trimmer\n\nThe hair salon finish, at home.",
 11: "Pomade, clay or cream?\n\nThe right product makes a hair salon cut look right at home:\n• Shine: American Crew Pomade\n• Matte hold: Brickell Styling Clay\n• Signature scent: 18.21 Man Made Sweet Tobacco Pomade\n\nAll three are in Susy's picks for Longboat Key weather.",
 17: "Low, mid or high skin fade?\n\n• Low: office-friendly\n• Mid: the most popular\n• High: bold contrast with a textured top\n\nNot sure? Susy will recommend one for your head shape in Longboat Key.",
 53: "Holiday family visit coming up?\n\nQ Salon gift cards from $50 work for any hair salon service. Perfect for dads, sons and grandfathers in Longboat Key.\n\nWant something to unwrap too? Susy's picks include beard kits, pomades and fragrance.",
 66: "Gift card questions, answered:\n\n• They start at $50\n• They work for any hair salon service or product\n• They're delivered digitally\n\nEasy last-minute gifts for Lido Key.",
 67: "Stocking stuffers from a barber shop pro:\n\n• DOC HOLLIDAY Beard Oil\n• A tin of 18.21 Man Made Pomade\n• The full Viking Revolution beard kit: wash, conditioner, oil, balm and comb\n\nShop Susy's picks for Sarasota gift-givers.",
 74: "Party-proof styling for a long night in Downtown Sarasota.\n\n• Work American Crew Pomade through damp hair for medium hold and shine\n• Finish with Cupids Hypnosis Eau de Parfum, citrus over warm vanilla\n\nBoth are in Susy's picks.",
 86: "A simple grooming routine for Downtown Sarasota men:\n\n• Haircut every 3 to 5 weeks\n• Fade every 2 to 3 weeks\n• Color every 4 to 6 weeks\n• Facial monthly\n\nSusy's full grooming guide is on our site.",
 88: "Restock for the new year with Susy's picks from our Sarasota hair salon:\n\n• Brickell Styling Clay for matte hold\n• The Viking Revolution beard kit\n• Cardon sulfate-free shampoo and conditioner\n• MANSCAPED Lawn Mower Ultra for upkeep between visits\n\nSiesta Key, this one's for you.",
 47: "Not sure what product fits your hair?\n\nCall The Q Salon for Men in Longboat Key and ask. We'll point you to the right pick in Susy's shop, and Susy can match you at your next visit.",
 68: "Want help choosing a gift?\n\nCall The Q Salon for Men and we'll help you pick the right gift card or service.\n\nGift cards start at $50 and work for any service or product.",
}
if __name__ == "__main__":
    rows = json.load(open("rows.json"))
    out = []
    for r in rows:
        t = OVERRIDE.get(r["day"]) or fmt(r["summary"])
        assert len(t) <= 1500
        out.append({"day": r["day"], "summary": t})
    json.dump(out, open("summaries.json", "w"), indent=1)
    for o in out: print("=== day", o["day"]); print(o["summary"]); print()
