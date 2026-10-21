# Q Salon tracking, October 21, 2026

## Website analytics

Existing Google Analytics account: The Q Salon for Men, 378414969.
Property: 517291470. Web stream: 13180402016, https://www.theqsalonsrq.com.
Measurement ID: G-V0NPW7N594 (public site configuration, not a secret).

Production uses Netlify Snippet injection before `</body>`, named Q Salon analytics and Amazon clicks. The same tested `tracking.js` can be loaded as a versioned asset when the repository write connection is restored. A guard prevents duplicate initialization if both copies load. It records
standard GA4 page views and an `amazon_click` event for each shop product button.
Parameters: `product_id`, `product_name`, `product_category`, `affiliate_channel`,
`affiliate_link_status`, `link_url`, and `link_domain`. An actual
`affiliate_tracking_id` is included only for a full Amazon URL that exposes it.
Google signals and advertising personalization signals are disabled in the tag.
An Amazon click is not a purchase or a completed booking.

Source is kept in sessionStorage across internal navigation with a 30-minute
inactivity expiry between pages. An explicit new UTM source replaces it.
Recognized sources: google/gbp, facebook/fb, instagram/ig. Recognized Google,
Facebook and Instagram referrers also set the channel. Other sources use website.
GA4 retains its own standard acquisition dimensions, including the original UTMs.

| Placement | Website landing URL | Amazon tracking ID |
| --- | --- | --- |
| Google Business Profile website button | https://www.theqsalonsrq.com/?utm_source=google&utm_medium=gbp&utm_campaign=profile&utm_content=website_button | qsalongoogle-20 |
| Google Business Profile product cards | https://www.theqsalonsrq.com/shop?utm_source=google&utm_medium=gbp&utm_campaign=products&utm_content=PRODUCT_SLUG#CATEGORY | qsalongoogle-20 |
| Instagram shop link | https://www.theqsalonsrq.com/shop?utm_source=instagram&utm_medium=social&utm_campaign=profile&utm_content=bio | qsalonig-20 |
| Facebook shop link | https://www.theqsalonsrq.com/shop?utm_source=facebook&utm_medium=social&utm_campaign=profile&utm_content=shop_link | qsalonfb-20 |
| Other website visits | https://www.theqsalonsrq.com/shop | qsalonweb-20 |

The Google website button and 16 product URLs were submitted in GBP. Social
profile links have not been changed in this session.

Registered event-scoped custom dimensions: Amazon product (`product_name`), Amazon referral channel (`affiliate_channel`), Amazon product category (`product_category`), Amazon link verification (`affiliate_link_status`).

Verified in GA4 Realtime on October 21: page views and an `amazon_click` event
with product_name `Brickell Styling Clay Pomade` and affiliate_channel `website`.
The QA visit used utm_source=qa, utm_medium=verification, and
utm_campaign=tracking_setup. These test events are not customer purchases.

## Amazon link status: verification required

All 17 current product destinations in `../shop/products.json` are `link.amazon`
short links. Their tokens are not ASINs. Do not construct `/dp/` URLs from them or
append `tag` to a shortened URL and assume it changes commission attribution.
Existing short URLs remain intact and click events label them
`short_link_unverified`. Channel-specific Amazon sales attribution is NOT yet
verified, even though website source and product clicks can be measured.

To finish, obtain each exact full Amazon product URL from the existing link or
Amazon SiteStripe, verify its product and variant, and replace the corresponding
`link` in products.json. The script only updates tags for HTTPS amazon.com or
www.amazon.com `/dp/ASIN` or `/gp/product/ASIN` URLs with a ten-character ASIN.
Then rebuild, test and deploy. Check the resulting links using Amazon's Link
Checker or Associates support. Amazon Associates rejected the cloud browser's
session. A public product click resolved Brickell's short link to ASIN
B0842Z6Y9H with tag kbdfinds-20 and the matching scented 2 oz product.
The next product navigation was blocked by browser security policy; remaining
destinations have not been verified. The existing short links are preserved.

Use GA4 `amazon_click` events to assess product interest by acquisition source.
Use Associates reports filtered by tracking ID for ordered/shipped items and
commissions after verified tags are installed. These cannot identify individual
buyers or reconstruct historical source attribution from old untagged visits.

## Build and deployment

GitHub integration rejected tree writes with 403 Resource not accessible by
integration. Browser upload is the authorized fallback for these changes.
Verify the production Netlify deploy and live pages after merging.
Site-wide snippet injection is independent of Git builds, so it persists across
deploys. Do not remove the snippet until a repository version is live and verified.

## Google Search Console

The verified property is https://www.theqsalonsrq.com/. The sitemap was
successfully submitted and read October 21, discovering all 17 current pages.
The latest Pages report (October 11) showed 11 indexed. Indexing requests were
accepted for shop, about, mens-hair-salon-sarasota, skin-fade-sarasota,
mens-hair-color-sarasota, and kids-haircut-sarasota. Acceptance does not guarantee
indexing; Google controls crawl and index timing.

Manual actions and security issues: none detected. HTTPS: no issues.
Breadcrumbs: 10 valid, zero invalid. Review snippets: zero current valid or
invalid items. Core Web Vitals: insufficient usage data, not a passing score.
The one historical noindex URL, /beard-trim-sarasota, now returns 404 and is
outside the current sitemap. Do not mark all historical 404s fixed: only the
explicitly mapped legacy routes should redirect.


Run `python3 build.py` from this directory. Production Netlify project:
`tranquil-yeot-e8ab44`, KB Digital team. Production branch `qsalon-live`, base
`qsalon/site`, publish `dist`. Commit built pages and the versioned script.
Preserve unrelated differences between `main` and `qsalon-live`; do not reset
the production branch to an unrelated main snapshot.
