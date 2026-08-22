# Design direction

**Adopted 2026-08-22.** Why the page looks the way it does. Read before changing the visuals.

## The constraint that decides everything

This site sells the ability to make a corporate message land. **So the site itself is the proof.**
A portfolio of presentation design that is hard to scan has already lost the argument on page one.
Craft here means clarity, hierarchy and restraint, not visual noise.

## What already exists, and why this site is different

`wangle.studio` is live and is Wangle's animation-studio face. Measured 2026-08-22:

- Black ground (`#000`), SF Pro type, image-led, minimal chrome, custom build with no CMS.
- Meta description: "Wangle Studio is an animation studio for motion and design".
- Publicly names ten clients, so client naming is an established practice for this company.
- Says nothing about presentations, decks, conference film or product visualization.

`wanglemedia.com` is the corporate entity site. `wangle.agency` and `wanglemotion.com` both
redirect into `wangle.studio`.

**The gap is real:** nothing Wangle currently publishes speaks to a marketing or internal-comms
buyer. That buyer is not shopping for an animation studio.

## The direction: deliberate contrast, not a sibling clone

Do NOT copy the black minimalist studio language. Two reasons.

1. **A second black studio site with less content looks like a worse version of the first.** We
   cannot out-image the animation reel, and we should not try.
2. **The audience is different.** A creative director enjoys a moody black canvas. A marketing
   director evaluating a supplier wants to understand the offer in fifteen seconds.

So: **light, editorial, tightly structured.** Generous whitespace, strong typographic hierarchy,
a disciplined grid, colour used sparingly and purposefully. The work supplies the colour; the page
supplies the calm. This reads as a professional communications partner, and it is the harder thing
to execute well, which is itself the demonstration.

## The visual system: a drafting sheet

Wangle's mark is a CAD line drawing, and the pitch is that real production infrastructure sits
behind the imagery. So the page borrows the vernacular of a technical drawing: sheet references down
the left rail, measured rules, monospace annotation, and case studies presented as annotated plates
with corner registration marks.

The conceit lives in structure and detail only. The content itself stays plainly legible, because
the audience is a marketing director scanning, not a designer admiring.

## Palette, derived from the mark rather than invented

The gradient W runs violet through blue and cyan into pink. Rather than pick an unrelated accent,
the page takes that violet and deepens it for legibility.

| Token | Light | Dark |
|---|---|---|
| accent (`--mark`) | `#4A42E0` | `#8B86FF` |
| paper | `#EFEFF3` | `#101014` |
| ink | `#16161D` | `#E9E9EF` |

Measured, not assumed: accent on paper is **5.82:1**, white on accent **6.67:1**, accent on dark
paper **6.28:1**. All clear WCAG AA for body text. The neutrals carry a slight violet bias so they
read as chosen rather than defaulted.

**The page stays quiet on purpose. The mark is the one saturated thing on it.**

## Type, three roles

- **Familjen Grotesk** for display. A Swedish grotesque, which suits a Copenhagen and Stockholm
  studio, and carries more character than the usual safe sans.
- **Public Sans** for body. Already one of Wangle's brand fonts, and openly licensed, so there is
  no font-licensing exposure on a commercial site.
- **DM Mono** for annotation: sheet references, labels, figures.

## Structure

Ordered by what a referral visitor needs, not by what we have most of.

1. **Hero.** The stakes, in one line, plus what we make. No cleverness, no scroll-jacking.
2. **Selected clients.** Names, immediately. A referral visitor is silently asking whether we are
   real, and this answers it before any argument is made.
3. **Selected work.** Three cases, each with an evidence figure, not just a description. A
   consistent shape across all three so they can be compared.
4. **What we do.** Four services in plain language, named the way a buyer would search for them.
   Versioning and optimisation is the pillar that separates this from a design agency.
5. **The studio.** Credibility: a company with infrastructure, not a freelancer with a template.
6. **Who you work with.** A named human. Referral buyers hire people, not logos.
7. **Contact.** One action. Static site, so a plain mailto rather than a form backend.

## The thing that makes it convert, if anything does

A portfolio site rarely converts cold traffic. It closes a loop someone else opened, which here
means a warm introduction. Its job is to remove doubt fast.

That is why every case carries a number. **A sentence asks to be believed; a figure gets checked and
remembered.** Any figure published here must be one Wangle can defend if a buyer challenges it.

## Rules for the build

- Every case study slot must render acceptably with a **designed abstraction** in place, so the
  site is presentable end to end before any client asset is cleared. Real stills swap in later.
- Responsive, accessible contrast, fast. No heavy video on first load; poster frames that play on
  demand.
- Light and dark both handled, since the page will be opened on every kind of screen.
- No em-dash characters anywhere. The build enforces this.

