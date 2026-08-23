# STATE, wangle-portfolio-site

**CURRENT as of 2026-08-23, 02:15.** Built in one session on 2026-08-22.

## The site is LIVE and sendable

**https://wangle.media** on GitHub Pages from `Wangle-Media/wangle-portfolio-site`, `main:/docs`.
HTTPS enforced, all four entry points (apex, www, http, github.io) resolve to the apex.

It exists to be sent to a warm contact who then decides whether to make an introduction. That job is
done. Everything below is refinement, not blockers.

## What it sells, and the framing that took the longest to get right

Corporate communications, **led by presentations and decks**, not film. The lead case was originally
written as "the film a listed company puts in front of its investors" and read as "we make expensive
videos", which is the wrong sale. It now leads on the presentation work and says explicitly that it
is *the same discipline as a board deck, with the stakes turned up*. Keep that framing.

Five services: presentation and deck design, conference and brand film, product visualization at
volume, design validation, versioning and optimisation. **Versioning is the differentiator** against
a design agency and it came out of Wangle's own capability deck.

## Content decisions that are settled, do not re-litigate

- **Clients named:** Pandora, LEGO, Sony, Novo Nordisk, Kia, BRIO, Playmobil. All are already public
  on wangle.studio, so naming them is not a new disclosure. Nordisk Film was removed at Geoff's ask.
- **Founded 2019**, confirmed by Geoff against the register.
- **No VES mention.** Geoff: buyers here will not recognise it. "Award-winning" only.
- **Three cases:** Pandora Capital Markets Day (lead), Pandora content supply chain, BRIO Flora.
  Kia was removed as a case but stays in the client list.
- **Partner bios** are Geoff, Henrik (co-founder, no CEO/CTO title, philosopher running the
  technology), Sune (co-founder, editor from luxury/fashion, trained statistician). Jacob is a fourth
  equal partner and is deliberately NOT on the page; Geoff named only two.

## Figures: what is published and why

Two Pandora business metrics were live for a while and were **removed**. Research could not find five
of six published anywhere by Pandora, and the sixth (22% growth) differs in scope from Pandora's own
reporting: their public figure covers a broader jewellery segment, not rings and earrings.

**Rule that came out of it: claim our own work, not the client's business results.** The cases now
carry "multi-year", "under embargo", "one model", "design to launch". Those are defensible because we
did them.

Kept: BRIO's 87% retention and Toy of the Year 2025. Geoff ruled the 87% is fine and defensible.
**The 22% figure is still in the media kit PDF.** If that deck is ever revised, fix it there too.

## Media kit form

Live at the foot of the page. Captures to a Sheet, mails the deck from Drive immediately, notifies
Geoff so he can reply while they are reading. `MAX_SENDS_PER_DAY = 40` caps sending, never recording.

- Script: `mediakit.gs`, deployed endpoint `AKfycbxOxtQrLY9...`, verified writing to the
  "Wangle media kit requests" sheet.
- Manifest `appsscript.json` pins it to `spreadsheets.currentonly` + `script.send_mail`.
- Deck lives in **Drive**, not this repo, so it can be replaced or revoked.
- Setup and the deployment traps: `MEDIAKIT_SETUP.md`.

## Build

`python build.py` reads `template.html`, embeds the logo as a data URI, writes `docs/index.html`.
**Edit `template.html`, never `docs/index.html`.** The build fails on an em-dash.

Single-file output on purpose: the same artifact serves Pages and standalone review, so there is no
second copy to drift.

## Performance shape

First paint about 400 KB (html + posters + faces). Video is `preload="none"` behind an
IntersectionObserver, so it costs nothing until a plate nears the viewport and nothing at all for a
visitor on save-data or reduced motion, who keep the poster.

**The observer must select `video[data-src]`, not `.plate video[data-src]`.** Scoping it to plates
left the studio reel showing a still forever.

## Still open

1. **Real headshots.** The partner faces are 58px idents upscaled to 96. `Company/Branding/
   ProfilePics/` holds a 2021 shoot at 5184x3456, roughly 140 unlabelled frames. Someone who can
   identify who is who could swap in proper portraits.
2. **An engagement-model line.** Nothing tells a referrer whether to send a 50k job or a 500k one.
   Geoff is handling this in the email instead, for now.
3. **A combined loop for the supply-chain plate** exists from demoreel (PTM plus turtle, 2.88 MB) and
   is unused. Would need re-encoding to about 1 MB first.
