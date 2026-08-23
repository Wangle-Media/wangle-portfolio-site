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

## The contact form

**One form, not a mailto plus a separate kit request.** A mailto is the highest-friction control on
a page: it launches an app, hands over a blank draft, and loses whoever gets distracted. It is now a
plain text link below the form.

Email, name, company, and an **optional message**. Leave it blank and you get the deck; write in it
and Geoff gets an enquiry. **No opt-out checkbox on purpose:** every checkbox is a decision, and
decisions are the friction being removed.

**The reply adapts, and that is what makes the no-checkbox choice safe.** Someone who wrote a note
gets "Geoff has your note and will reply personally" with the deck second, and the owner
notification is subject-lined ENQUIRY and leads with what they wrote. A canned "here is the deck" in
answer to a real message reads as a robot ignoring them.

`MAX_SENDS_PER_DAY = 40` caps sending, never recording. Both paths verified end to end against the
sheet on 2026-08-23.

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

## Open decisions, parked deliberately

1. **Does the hero h1 keep the logo face?** "Some rooms you only get once." is currently set in
   M PLUS Rounded 1c 800, the lockup face; every other heading is Familjen Grotesk. Geoff is
   sleeping on it, 2026-08-23.
   - **For:** ties the hero to the identity, and at display size the roundness reads confident.
   - **Against:** it is a logo face doing headline work, it reads soft for a corporate buyer, and
     the dark banner now establishes the identity at the top of the page anyway, so the h1 no
     longer needs to.
   - Reverting is one line: drop the `.hero h1` font-family override.
2. **Type `message` into cell E1** of the media kit sheet. The header row predates that column, and
   the script only writes headers into a completely empty sheet. Cosmetic; the data lands correctly.

## Still open

1. **Real headshots.** The partner faces are 58px idents upscaled to 96. `Company/Branding/
   ProfilePics/` holds a 2021 shoot at 5184x3456, roughly 140 unlabelled frames. Someone who can
   identify who is who could swap in proper portraits.
2. **An engagement-model line.** Nothing tells a referrer whether to send a 50k job or a 500k one.
   Geoff is handling this in the email instead, for now.
3. **A combined loop for the supply-chain plate** exists from demoreel (PTM plus turtle, 2.88 MB) and
   is unused. Would need re-encoding to about 1 MB first.
