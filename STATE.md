# STATE, wangle-portfolio-site

**CURRENT as of 2026-08-22.**

## What this is

Wangle Media's corporate-communications site. It sells presentation and deck design, conference and
brand film, product visualization at volume, and versioning/optimisation. The audience is a
marketing or internal-communications buyer, which is a different buyer from the one `wangle.studio`
speaks to.

The site must itself demonstrate design competence, so its own craft is part of the deliverable.

## Decisions made

| Decision | Value |
|---|---|
| Hosting | GitHub Pages, `/docs` on `main` |
| Repo | `Wangle-Media/wangle-portfolio-site`, PUBLIC |
| Domain | not yet cut over, no CNAME committed (see CLAUDE.md) |
| Positioning | corporate communications, not animation or visual effects |
| Contact | geoff@wanglemedia.com |

## Content status

Three case studies, each with an evidence figure rather than only a description:

- **Pandora**, content supply chain
- **BRIO**, new product line launch
- **Kia**, European EV9 launch

Copy is drawn from Wangle's own capability and case-note material. No confidential figures are used
anywhere in this repo.

## Still open

1. **Images.** The three case plates are designed placeholders. Real stills drop straight in. Each
   needs sign-off before publication.
2. **Domain.** Then DNS, then CNAME, strictly in that order.
3. **Defensibility of published figures.** Any performance number on the page must be one Wangle can
   stand behind if a buyer challenges it. Review before promoting the site widely.

## Conventions

Edit `template.html`, then run `python build.py`. Never edit `docs/index.html` by hand.
