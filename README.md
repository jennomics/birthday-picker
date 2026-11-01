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

The site is meant to live at https://birthday.entungle.com. The `CNAME` file in this repository tells GitHub Pages that domain.

One-time setup:

1. In this repository go to Settings, then Pages. Under Build and deployment choose Deploy from a branch, pick `main` and `/ (root)`, and save.
2. At the DNS provider for entungle.com, add a CNAME record: host `birthday`, value `jennomics.github.io`.
3. Back on the Pages settings page, the custom domain shows as birthday.entungle.com. Once the DNS check passes, tick Enforce HTTPS.

The page is also reachable at https://jennomics.github.io/birthday-picker/ until the custom domain is set.

Everything a visitor does on the page stays in that visitor's browser. Nothing is sent anywhere.
