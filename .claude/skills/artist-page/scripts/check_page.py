#!/usr/bin/env python3
"""Check an /artist-page output file before it goes to review.

Usage: check_page.py artist-pages/<slug>.txt

Prints each problem found and exits 1, or prints "OK" and exits 0.
"""
import html
import json
import os
import re
import sys

SECTIONS = [
    "SEO TITLE", "META DESCRIPTION", "INTRO", "ABOUT", "STYLE AND SUBJECTS",
    "FAMOUS WORKS", "DECORATING WITH", "FAQ", "RELATED ARTISTS",
    "SHOPIFY HTML", "NOTES FOR REVIEW",
]
SEP = re.compile(r"^=+\n(.+?)\n=+\n", re.M)


def norm(text):
    text = re.sub(r"</?(p|h\d|ul|ol|li)\b[^>]*>", " ", text)  # block tags break words
    text = html.unescape(re.sub(r"<[^>]+>", "", text))  # inline tags (a, strong) do not
    return re.sub(r"\s+", " ", text).strip()


def paragraphs(text):
    return [norm(p) for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    raw = open(path, encoding="utf-8").read()
    problems = []

    head = raw[: SEP.search(raw).start()] if SEP.search(raw) else raw
    m = re.search(r"ARTIST PAGE:\s*(.+?)\s*\(", head)
    name = m.group(1).strip() if m else None
    if not name:
        problems.append("Header: missing 'ARTIST PAGE: <Name> (<dates>)' line.")
    for field in ("Collection URL:", "Prints in store:", "Generated:"):
        if field not in head:
            problems.append(f"Header: missing '{field}'.")

    # Split into sections, keyed by their heading without the "(...)" hint.
    parts = SEP.split(raw)
    sections = {}
    order = []
    for i in range(1, len(parts) - 1, 2):
        key = re.sub(r"\s*\(.*\)$", "", parts[i]).strip()
        sections[key] = parts[i + 1].strip()
        order.append(key)

    found = []
    for want in SECTIONS:
        hit = next((k for k in order if k.startswith(want)), None)
        if hit is None:
            problems.append(f"Missing section: {want}.")
        else:
            found.append(order.index(hit))
    if found != sorted(found):
        problems.append("Sections are out of order.")

    def sec(prefix):
        return next((v for k, v in sections.items() if k.startswith(prefix)), "")

    title = sec("SEO TITLE")
    if len(title) > 60:
        problems.append(f"SEO title is {len(title)} characters (max 60).")
    meta = sec("META DESCRIPTION")
    if not 140 <= len(meta) <= 155:
        problems.append(f"Meta description is {len(meta)} characters (needs 140-155).")
    intro = sec("INTRO")
    words = len(intro.split())
    if not 50 <= words <= 80:
        problems.append(f"Intro is {words} words (needs 50-80).")
    if name and not intro.startswith(f"{name} prints"):
        problems.append(f"Intro should start with '{name} prints'.")

    # The HTML must repeat the plain-text copy.
    page_html = sec("SHOPIFY HTML")
    html_text = norm(page_html)
    for key in ("INTRO", "ABOUT", "STYLE AND SUBJECTS", "DECORATING WITH"):
        for p in paragraphs(sec(key)):
            if p not in html_text:
                problems.append(f"HTML is missing or differs from this {key} paragraph: {p[:70]}...")
    for q, a in re.findall(r"^Q:\s*(.+?)\nA:\s*(.+?)$", sec("FAQ"), re.M):
        for part in (q, a):
            if norm(part) not in html_text:
                problems.append(f"HTML is missing or differs from FAQ text: {part[:70]}...")
    for line in sec("FAMOUS WORKS").splitlines():
        m = re.match(r"-\s*(.+?)\s*(\(\d{4}\)|\(etching\)|,|\.)", line)
        if m and norm(m.group(1)) not in html_text:
            problems.append(f"HTML is missing famous work: {m.group(1)}")

    if name and f"<strong>{name} prints</strong>" not in page_html:
        problems.append(f"HTML intro should open with <strong>{name} prints</strong>.")
    for bad, why in (
        (r"\sstyle=", "inline styles"), (r"\sclass=", "classes"), (r"<div", "<div>"),
        (r"<br", "<br>"), (r"<h1", "<h1>"), (r"https?://(www\.)?artworkculture\.com", "absolute store links"),
    ):
        if re.search(bad, page_html, re.I):
            problems.append(f"HTML contains {why}; use plain relative markup.")

    # Product links must exist in the store data, when we have it.
    handles = re.findall(r'href="/products/([^"]+)"', page_html)
    slug = os.path.splitext(os.path.basename(path))[0]
    cache = os.path.join(os.path.dirname(path) or ".", ".store", f"{slug}.json")
    if os.path.exists(cache):
        store = json.load(open(cache, encoding="utf-8"))
        known = {p["handle"] for p in store["products"]}
        for h in handles:
            if h not in known:
                problems.append(f"Product link /products/{h} is not in the store collection.")
        m = re.search(r"Prints in store:\s*(\d+)", head)
        if m and int(m.group(1)) != store["count"]:
            problems.append(f"'Prints in store' says {m.group(1)}, store data has {store['count']}.")
        for line in sec("RELATED ARTISTS").splitlines():
            rm = re.search(r"/collections/([a-z0-9-]+)", line)
            rcache = os.path.join(os.path.dirname(cache), f"{rm.group(1)}.json") if rm else None
            if rm and not os.path.exists(rcache):
                problems.append(f"Related artist collection '{rm.group(1)}' was not checked with fetch_collection.py --count.")
            elif rm and json.load(open(rcache, encoding="utf-8"))["count"] == 0:
                problems.append(f"Related artist collection '{rm.group(1)}' is empty.")
    elif handles:
        problems.append("No store data found (run fetch_collection.py first), so product links are unchecked.")

    if problems:
        print(f"{len(problems)} problem(s) in {path}:")
        for p in problems:
            print(f"- {p}")
        sys.exit(1)
    print(f"OK: {path} (title {len(title)} chars, meta {len(meta)} chars, intro {words} words)")


if __name__ == "__main__":
    main()
