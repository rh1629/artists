#!/usr/bin/env python3
"""List the products in an artworkculture.com collection.

Usage:
  fetch_collection.py <collection-slug>           # product list
  fetch_collection.py <collection-slug> --count   # just the number of products

The list is also saved to artist-pages/.store/<slug>.json so check_page.py
can confirm that every /products/<handle> link on the page is real.
"""
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

STORE = "https://artworkculture.com"
YEAR = re.compile(r"\b(1[3-9]\d\d|20[0-2]\d)\b")


def fetch_page(slug, page):
    url = f"{STORE}/collections/{slug}/products.json?limit=250&page={page}"
    req = urllib.request.Request(url, headers={"User-Agent": "artist-page-skill/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp).get("products", [])


def find_year(product):
    texts = [product.get("title", "")]
    texts += product.get("tags", []) if isinstance(product.get("tags"), list) else [product.get("tags") or ""]
    body = re.sub(r"<[^>]+>", " ", product.get("body_html") or "")
    texts.append(html.unescape(body))
    for text in texts:
        m = YEAR.search(text)
        if m:
            return m.group(1)
    return ""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    slug = args[0].strip("/").split("/")[-1]
    count_only = "--count" in sys.argv

    products, page = [], 1
    try:
        while True:
            batch = fetch_page(slug, page)
            products += batch
            if len(batch) < 250:
                break
            page += 1
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Collection '{slug}' not found (404).")
            sys.exit(2)
        print(f"Store returned HTTP {e.code} for '{slug}'.")
        sys.exit(3)
    except (urllib.error.URLError, OSError) as e:
        print(f"Could not reach {STORE}: {e}. The store may be blocked by this session's network settings.")
        sys.exit(3)

    rows = [
        {"title": p.get("title", "").strip(), "handle": p.get("handle", ""), "year": find_year(p)}
        for p in products
    ]

    os.makedirs("artist-pages/.store", exist_ok=True)
    with open(f"artist-pages/.store/{slug}.json", "w", encoding="utf-8") as f:
        json.dump({"slug": slug, "count": len(rows), "products": rows}, f, ensure_ascii=False, indent=1)

    if count_only:
        print(len(rows))
        return
    print(f"Collection: {STORE}/collections/{slug}")
    print(f"Products: {len(rows)}\n")
    for r in sorted(rows, key=lambda r: (r["year"] or "9999", r["title"].lower())):
        print(f"{r['year'] or '----'}  {r['title']}  ->  /products/{r['handle']}")
    if not rows:
        print("The collection is empty. Try another slug spelling.")


if __name__ == "__main__":
    main()
