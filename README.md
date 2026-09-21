# Numerical Reasoning Trainer

A single self-contained HTML file for practising the numerical reasoning used in
graduate-scheme aptitude tests (Cappfinity, as used by Lloyds; Sova, as used by Babcock).

**To use it:** open `index.html` in any browser — double-click it, or put it on your
phone and open it there. There is nothing to install and no internet connection needed.

## What's in it

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

## Installing it on your phone

The app can live on your home screen with its own icon, opening without any
browser bars and working with no connection. To do that it needs to be served
over `https://` — phones will not install a page opened from a file.

**Step 1 — put it online.** Any static host works. The files to upload are
`index.html`, `manifest.webmanifest`, `sw.js` and the four `.png` icons.

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
  **Share** button, then **Add to Home Screen**. You can rename it there.
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
No accounts, no servers, no analytics — and no network requests of any kind once
the page has loaded. `index.html` still works entirely on its own: open it straight
from disk, with the other files deleted, and everything but the home-screen install
works exactly as before. Your progress never leaves
your device, and the Progress tab has a reset button that clears it.

A day counts towards your streak as soon as you answer one question; you don't have
to finish a whole session for it to count.
