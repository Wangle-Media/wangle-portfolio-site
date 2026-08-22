# Wangle, corporate communications

Source for Wangle Media's corporate-communications site: presentation and deck design, conference
and brand film, product visualization, and versioning and optimisation.

Wangle's animation and moving-image work lives separately at [wangle.studio](https://www.wangle.studio).

## Build

```
python build.py
```

Reads `template.html`, embeds the brand mark, writes `docs/index.html`. No dependencies beyond the
standard library. GitHub Pages serves `/docs` from `main`.

Edit `template.html`. Never edit `docs/index.html`, it is generated.

The build fails if an em-dash character reaches the output. That is a house style rule, enforced so
it cannot regress quietly.

## Layout

| Path | What it is |
|---|---|
| `template.html` | the page, content and styles |
| `build.py` | embeds the logo, writes `docs/`, runs the style check |
| `docs/index.html` | generated output, served by Pages |
| `docs/assets/` | brand mark source files |
| `DESIGN-DIRECTION.md` | why the page looks the way it does |
| `STATE.md` | what is current and what is still open |

## Contact

geoff@wanglemedia.com
