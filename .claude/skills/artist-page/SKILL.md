---
name: artist-page
description: Write the SEO copy for an artist collection page on artworkculture.com (Shopify) - SEO title, meta description, intro, biography, style, famous works, decorating ideas, FAQ, related artists, paste-ready Shopify HTML and review notes. Use when the user types /artist-page <Artist Name>, or asks for an artist page, collection description or SEO page for an artist.
argument-hint: <Artist Name> [collection URL]
---

# /artist-page

Produce one plain-text file of SEO copy for an artist's collection page on
**artworkculture.com**, a Shopify store selling fine art prints. The file is
reviewed by a person and then pasted into Shopify, so it must be accurate,
readable and ready to paste.

`references/example-armand-apol.txt` is the gold-standard output. Read it before
writing. Match its section order, headings, separators, tone and level of detail.

## Inputs

- **Artist name** (required), e.g. `Frances Hodgkins`.
- **Collection URL** (optional). Default:
  `https://artworkculture.com/collections/<slug>`, where `<slug>` is the name
  lower-cased, accents removed, spaces and punctuation turned into hyphens
  (`Valerius De Saedeleer` → `valerius-de-saedeleer`).

If no name was given, ask for one. Ask nothing else; make sensible choices and
record them under NOTES FOR REVIEW.

## Step 1: Get the store data

Run:

```bash
python3 .claude/skills/artist-page/scripts/fetch_collection.py <slug>
```

It reads the collection's public `products.json` and prints the product count and
one line per product: title, handle, and any year found in the title, tags or
description. Product links are `/products/<handle>`.

- If the collection is empty or 404s, try the obvious slug variants (with or
  without middle names, particles like "van"/"de", accents). If nothing works,
  stop and tell the user.
- If the store is unreachable (network blocked), say so. Do not guess product
  handles. You may still write the page, but leave the Famous Works and Decorating
  links out, set "Prints in store" to `unknown`, and flag it at the top of
  NOTES FOR REVIEW.

The store data is the authority on **what is for sale**. It is not a source for
biographical facts, but product titles and dates can describe what the
collection contains (say so in the notes when you do this, as the example does
for the 1929 south-of-France works).

## Step 2: Research the artist

Use, in this order, whatever is reachable:

1. English Wikipedia, and the Wikipedia of the artist's own language
   (nl, fr, de, it, es...). These often differ; the native one is usually fuller.
2. Wikidata (dates, places, movement, notable works, collections).
3. Museum and national biography sites (Te Ara, RKD, Tate, Art UK, national
   galleries, catalogues raisonnés).
4. Web search, to fill gaps or when the sites above are blocked.

Collect: birth and death dates and places, training and teachers, groups and
movements, key moves and events, subjects and style, notable works with dates and
the museums that hold them, and any well-known namesake who gets confused with
the artist.

Rules for facts:

- Every factual claim on the page must come from a source. If you cannot source
  it, leave it out.
- When sources disagree, use the safer or more general wording on the page
  ("Brussels" rather than a district; "mid-1920s" rather than one of two dates)
  and record the conflict in NOTES FOR REVIEW.
- Never say a store product is in a museum, or is the same painting as a famous
  work, unless a source confirms it. A matching title is not confirmation.
- English translations of foreign titles are your own; note that.

## Step 3: Pick the works and related artists

**Famous works** (5 to 7 entries):

- Prefer works that are both notable and in the store. Then fill with store
  products that best show the artist's range (different subjects, dates).
- You may add one or two sourced museum works that are not in the store, to
  show significance. Give the museum, and no product link.
- Format: `Original title (English title) (year). One sentence on what it
  shows. [Available as a print]`. Omit the bracketed English when the title is
  already English, and the year when unknown. Mark `[Available as a print]` only
  for store products.

**Related artists** (3 entries, up to 5):

- Each must have a real, sourced connection: teacher, student, member of the
  same group, influence, collaborator, shared movement.
- Each must have a non-empty collection in the store. Check with
  `fetch_collection.py <their-slug> --count`. Skip artists with no products and
  note who you skipped and why.
- If the store is unreachable, list candidates in NOTES FOR REVIEW instead of
  the page, unchecked.

## Step 4: Write the page

Write in plain, warm, specific British English (colour, harbour, centre). Short
sentences. No hype ("stunning", "masterpiece", "timeless"), no exclamation marks,
no emoji, no "In this article". Write for a buyer choosing art for their home who
also wants to know who the artist was.

Sections, in this order, using the exact separator style of the example:

1. **Header**: `ARTIST PAGE: <Name> (<birth>–<death>)`, `Collection URL:`,
   `Prints in store:` (count), `Generated:` (today's date, YYYY-MM-DD).
2. **SEO TITLE** (max 60 characters). Default pattern:
   `<Name> Prints & Wall Art | Artwork Culture`. If that is over 60, use
   `<Name> Prints | Artwork Culture`.
3. **META DESCRIPTION** (140–155 characters). Starts with "Explore <Name>
   prints:" or similar, names the artist's main subjects and one or two real
   product titles, ends with "as fine art prints." or similar.
4. **INTRO** (50–80 words). First words are `<Name> prints`. Says what the
   prints show, who the artist was in one line (nationality, media, style), and
   what the collection covers.
5. **ABOUT <NAME>** (3–4 paragraphs). Life story in order: birth, training,
   groups, moves, key events, later career, where the work is held.
6. **STYLE AND SUBJECTS** (2 paragraphs). What the work looks like and what it
   shows. The second paragraph ties this to what is in the collection.
7. **FAMOUS WORKS** (see Step 3).
8. **DECORATING WITH <SURNAME> PRINTS** (2 paragraphs). Concrete room
   suggestions tied to the subjects and colours of real products; name and link
   two or three products.
9. **FAQ** (4–5 questions). Questions people actually search: what movement,
   what known for, where to see originals, how to recognise the style, and a
   namesake question if there is a known mix-up. Answers 1–3 sentences, sourced.
10. **RELATED ARTISTS**: `- Name — connection — https://artworkculture.com/collections/<slug>`.
11. **SHOPIFY HTML** (see below).
12. **NOTES FOR REVIEW**: sources used (URLs) and the store data; every
    conflict between sources; every judgement call (translations, softened
    claims, store-derived descriptions); anything left out and why; store data
    problems spotted (typos, double spaces, missing dates, duplicate products).

### Shopify HTML

Paste-ready HTML for the collection description's HTML view. It repeats the
page's body copy exactly, from INTRO to RELATED ARTISTS. It does not include the
SEO title, meta description or notes.

- Intro: one `<p>`, with `<strong>` around the opening `<Name> prints`.
- Section headings: `<h2>`, in title case (`About Armand Apol`, `Style and
  Subjects`, `Famous Works`, `Decorating with Apol Prints`, `FAQ`, `Related
  Artists`).
- FAQ questions: `<h3>`, answers: `<p>`.
- Famous works: `<ul>`, each title in `<strong>`; store products wrapped in
  `<a href="/products/<handle>">`. Drop the `[Available as a print]` marker.
- Related artists: `<a href="/collections/<slug>">Name</a>: connection`.
- Relative links only. No inline styles, classes, `<div>`, `<br>` or `<h1>`
  (the theme supplies the H1).

## Step 5: Check and save

Save the file to `artist-pages/<slug>.txt` in the repository, then run:

```bash
python3 .claude/skills/artist-page/scripts/check_page.py artist-pages/<slug>.txt
```

It checks the title and meta lengths, the intro word count, that the intro opens
with `<Name> prints`, that every section is present, that the HTML repeats the
plain-text copy, and that every product link uses a handle from the store. Fix
everything it reports and run it again until it passes.

Then commit the file, and reply to the user with:

- one line: the page is done and where the file is;
- the SEO title and meta description;
- the two or three most important items from NOTES FOR REVIEW.

Do not paste the whole page into the chat.
