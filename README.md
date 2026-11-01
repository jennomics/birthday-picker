# Best Day Ever!

A one-page planner for a 16th-birthday weekend in Los Angeles. The page walks through four steps: browse the kinds of day, rank them, review priorities, and fit the picks into the weekend.

## Files

- `index.html` is the whole site. Open it in any browser or host it as a static page.
- `images/` holds the photos and illustrations the page uses.
- `src/page_template.html` is the page with a data placeholder.
- `src/build.py` fills the template from `src/data/` and writes `index.html`.
- `src/data/` holds the venue research, the venue list, and the original Google Earth export.

## Rebuild after editing

```
python3 src/build.py
```

Edit copy, categories, hooks, or schedule rules in `src/build.py` and `src/page_template.html`, then rebuild and commit `index.html`.

## Host it

GitHub Pages: in this repository go to Settings, then Pages, choose Deploy from a branch, pick `main` and `/ (root)`, and save. The page appears at the Pages URL within a minute or two. To use your own domain, enter it under Custom domain on that same settings page and add the DNS record GitHub shows you at your registrar.

Everything a visitor does on the page stays in that visitor's browser. Nothing is sent anywhere.
