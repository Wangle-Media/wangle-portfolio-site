# CLAUDE.md, wangle-portfolio-site

Wangle Media's corporate-communications site: presentation and deck design, conference and brand
film, product visualization, and versioning/optimisation. Separate from `wangle.studio` (the
animation and moving-image face of the same company).

**Purpose:** a link that can be sent to a warm contact, so the recipient can judge quickly whether
Wangle is worth an introduction. Presentable end to end beats complete.

## THIS REPO IS PUBLIC

Everything committed here is world-readable and permanent in git history. Assume no take-backs.

**Never commit:**

- Any client budget, bid figure, quote, rate card, or invoice amount. Not a number, not a range.
- Internal file paths, folder structures, project codenames, or shot codes.
- Contract terms, delivery schedules, or unreleased campaign details.
- Any client asset that has not been explicitly cleared for public use.
- Credentials of any kind.

**Allowed:** naming a client and describing the kind of work done, where that client is already
publicly associated with Wangle. Published performance figures are allowed only where Wangle can
defend them if challenged.

**Committing is publishing.** Stage anything uncleared outside this tree.

## Build

`python build.py` reads `template.html`, embeds the brand mark as a data URI, and writes
`docs/index.html`. GitHub Pages serves `/docs` from `main`.

Output is deliberately a single self-contained file: the same artifact can be served from Pages and
reviewed as a standalone page, which removes the drift risk of maintaining two copies.

**The build fails if an em-dash character appears anywhere in the output.** That is intentional and
it is a house style rule, not a bug. Use a comma, colon, parentheses, or a spaced hyphen.

## Editing content

Copy lives in `template.html`. Edit there, never in `docs/index.html`, which is generated and will
be overwritten on the next build.

## Design

`DESIGN-DIRECTION.md` records why the page looks the way it does, including the palette derivation
and the contrast measurements. Read it before making visual changes, so a change is a decision
rather than a drift.

## Domain

**Do not add `docs/CNAME` until DNS actually resolves to this site.** A committed CNAME makes Pages
claim the custom domain, which 301s the working github.io URL to wherever that domain currently
points. A sibling site took a live outage from exactly this mistake. Verify first, commit second.
