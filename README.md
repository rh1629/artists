# Artists

SEO copy for artist collection pages on artworkculture.com.

## /artist-page

Type `/artist-page <Artist Name>` in Claude Code to research an artist and write
their collection page: SEO title, meta description, intro, biography, style,
famous works, decorating ideas, FAQ, related artists, paste-ready Shopify HTML and
notes for review. The output is saved to `artist-pages/<slug>.txt`.

The skill lives in `.claude/skills/artist-page/`:

- `SKILL.md`: the instructions.
- `references/example-armand-apol.txt`: the reference page every output follows.
- `scripts/fetch_collection.py`: lists the store's products for a collection.
- `scripts/check_page.py`: checks lengths, sections, HTML and product links.

The skill needs network access to `artworkculture.com` (for product links) and
ideally to Wikipedia and Wikidata. Without them it falls back to web search and
leaves product links out.

## Other pages

- [Frances Hodgkins](frances-hodgkins/index.html): a standalone profile page.
