# Aptitude test trainers

Two offline trainers for graduate-scheme aptitude tests. Each is a self-contained
HTML file that works with no internet connection, and keeps all progress in the
browser on the device you're using.

| App | Folder | Address once published |
|---|---|---|
| **Numerical Reasoning** — percentages, ratios, rates, data | `/` | `…github.io/maths/` |
| **Inductive Reasoning** — nine boxes, find the odd one out | `/inductive/` | `…github.io/maths/inductive/` |

Both install to a phone home screen separately, with their own icon, and keep
their own streak and progress.

---

## Numerical Reasoning Trainer

For the numerical reasoning used by Cappfinity (Lloyds) and Sova (Babcock).

**To use it:** open `index.html` in any browser — double-click it, or put it on your
phone and open it there. There is nothing to install and no internet connection needed.

### What's in it

- **Practice** — questions generated fresh every time, so there are no answers to
  memorise, only methods. Untimed (learn) and Timed modes, a built-in calculator,
  a mix of multiple-choice and type-the-answer questions, and a full step-by-step
  worked solution after every single question — right or wrong.
- **Learn** — nine chapters written for an adult beginner. Each one goes:
  everyday comparison → what it is → the method → one example worked through slowly
  → a "check it makes sense" step → the trap → quick reference.
- **Tips** — exam technique: pacing, sanity-checking, units and scale, when to trust
  the calculator and when not to.
- **Progress** — daily streak (current and best), sessions, average score, a bar chart
  of recent sessions, and accuracy per topic so you can see what to drill next.

Topics covered: percentages, percentage of a number, percentage change,
increase/decrease by a percentage, reverse percentages, ratios, rates (speed and
price per unit), currency conversion, data interpretation from tables and charts,
and converting between fractions, decimals and percentages.

---

## Inductive Reasoning Trainer

For the nine-box "odd one out" format — inductive, logical or diagrammatic
reasoning, and the test Aon publishes as **scales ix**.

**To use it:** open `inductive/index.html`, the same way.

### What's in it

- **Practice** — puzzles generated fresh every time, across eleven kinds of rule:
  count, shape, fill, colour, size, direction, inside/outside, odd-one-inside,
  symmetry, even/odd, and matching relationships. Gentle, mixed and hard settings;
  untimed and timed. The checklist is one tap away while you solve.
- **Learn** — eight chapters, each with real solved puzzles printed in the page so
  the words always point at something you can see. Chapter 2 is the method itself.
- **Tips** — what to do when nothing jumps out, and how to pace it.
- **Progress** — streak, sessions, and accuracy per *rule type*, which tells you
  which checklist item your eye keeps skipping.

Every generated puzzle is checked before it is shown: the engine measures each of
fourteen features across all nine boxes and refuses any puzzle where more than one
box could be argued for, or where a simpler rule than the one it explains would
also solve it.

## Installing it on your phone

The app can live on your home screen with its own icon, opening without any
browser bars and working with no connection. To do that it needs to be served
over `https://` — phones will not install a page opened from a file.

**Step 1 — put it online.** Any static host works. Upload the whole folder: both
apps, their `manifest.webmanifest`, `sw.js` and `.png` icons.

- *GitHub Pages* (free, but the repository must be public on a free plan):
  Settings → General → change visibility to public, then Settings → Pages →
  Source: *Deploy from a branch* → Branch: `claude/tender-meitner-vp8tjr` /
  `(root)` → Save. The address is `https://kjakowicz-sudo.github.io/maths/`.
- *Netlify Drop* (free, repository stays private): go to app.netlify.com/drop
  and drag the folder onto the page.
- *Cloudflare Pages / Vercel* (free, repository stays private): connect the
  repository and deploy; no build step is needed.

**Step 2 — install it.**

- *iPhone / iPad:* open the address in **Safari** (it must be Safari), tap the
  **Share** button, then **Add to Home Screen**. You can rename it there. Do it once
  per app, using each app's own address, and you get two separate icons.
- *Android:* open it in Chrome and tap **Add to home screen** when prompted, or
  use the ⋮ menu → **Add to Home screen** / **Install app**.
- *Laptop:* Chrome and Edge show an install icon in the address bar.

The app itself shows a short line telling you how to install it, but only when
you are in a browser that can actually do it.

Once installed it caches itself, so it opens instantly and works on the tube,
on a plane, or anywhere with no signal.

### One thing worth knowing

Installed to the home screen, the app may keep its saved progress separately
from the copy you were using in the browser, so a streak built up in Safari
might not follow you across. If you have practice history you care about,
install first and build the streak there.

## Privacy

Everything is stored in your browser's `localStorage`, on the device you're using.
The two apps store their progress under separate keys and keep separate streaks.
No accounts, no servers, no analytics — and no network requests of any kind once
the page has loaded. `index.html` still works entirely on its own: open it straight
from disk, with the other files deleted, and everything but the home-screen install
works exactly as before. Your progress never leaves
your device, and the Progress tab has a reset button that clears it.

A day counts towards your streak as soon as you answer one question; you don't have
to finish a whole session for it to count.
