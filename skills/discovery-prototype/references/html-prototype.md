# HTML prototype

## Purpose

Turn the PRD, the PR/FAQ, and the riskiest assumption into a prototype that looks and behaves like a real product: a user flow of several screens, shown on a phone and in a desktop browser, that people can click through. It is still one self-contained `index.html` file, so anyone can open it in a browser and share it, with no build and no server.

## Start from the shell

Every version starts as a copy of `prototype-shell.md`. The shell is the product frame: the top bar, the three views, the phone and browser frames, routing, steppers, and the test moment toggle. You fill only the region between its `EDIT BELOW` and `EDIT ABOVE` markers: the settings and the screens. The rest of this page describes what the finished file does and how to write good screens.

## What the file contains

The file opens on a top bar with the product name and three views:

1. **Flow.** A design board: every screen of the core flow side by side in phone frames, in order, each with a step number, a short title, and an arrow to the next. This is the view people look at first and screenshot for the readout.
2. **Mobile.** One phone frame in the center with the live, clickable prototype. Tapping moves between screens exactly as the flow describes.
3. **Desktop.** The same product in a browser window frame (address bar, tabs), with a layout designed for a wide screen, not a stretched phone.

A **Show test moment** toggle highlights the screen and element where the riskiest assumption is tested, with a one-line note on what the team wants to learn there.

## The screens

- **One screen per step of the core flow,** usually 4 to 8: entry point, the main task in its steps, confirmation, and the main unhappy path (an error, a late or missing state). Every P0 requirement appears on at least one screen.
- **Real states.** Empty, loading, success, and one failure state for the step the riskiest assumption depends on.
- **Navigation that works.** Buttons, tabs, and back links move between screens with hash routes (`#/screen-id`), and small state survives navigation, for example a changed quantity or a chosen slot.
- **Views in the address.** Opening the file with `#/flow`, `#/mobile`, or `#/desktop` shows that view, so `compare.html` can show each version on its Flow view.
- **Realistic content** from the personas and the signals: real-looking product names, prices, times, and the persona's name. Never placeholder text.

## Visual quality

Design the prototype as a product team would show it to its sponsor:

- **A small design system first,** as CSS custom properties at the top: one neutral palette with a single accent color, a type scale (a serif or a distinctive sans for headings, a system sans for body, using local font stacks only), a 4 or 8-pixel spacing scale, one corner radius, and one shadow. Use the team's design standards instead when it gave them.
- **Device frames drawn in CSS:** a phone with rounded corners, status bar (time, signal, battery), and home indicator; a browser window with three dots, an address bar showing a plausible URL, and a tab.
- **Hierarchy and restraint:** one primary action per screen, generous white space, clear headings, consistent icon style (inline SVG), no more than one accent color.
- **Accessible:** text contrast of at least 4.5:1, tap targets of at least 44 pixels, visible focus, and readable at 100% zoom.
- **Calm motion only:** short fades or slides between screens, respecting `prefers-reduced-motion`.

In AWS Quick, also follow the bundled `html_design` skill's design principles where they apply.

## Technical rules

- **One file:** HTML, CSS, and JavaScript inline. No CDN, no external fonts or images, no build step. Images are inline SVG or CSS.
- **No backend:** all data is hard-coded sample content in a small JavaScript object.
- **Works offline,** in Chrome, Edge, Safari, and Firefox, and on a phone browser.
- **Size:** keep it under about 200 KB.

## Writing screens for the shell

- One `<template data-screen id="..." data-title="..." data-caption="...">` per step, in flow order. The title is the step name on the Flow board; the caption is one line on what the step proves.
- Use the shell's building blocks: `s-title`, `s-sub`, `card`, `row`, `pill ok|warn|bad`, `btn`, `btn secondary`, `stepper`, `muted`, `small`.
- Link screens with `data-go="next-screen-id"` on any button or card.
- Steppers: `<span class="stepper"><button data-dec="key">−</button><b data-bind="key"></b><button data-inc="key">+</button></span>`, with the starting value in `PROTOTYPE.state`.
- Mark the screen under test with `data-test-moment`, and the element under test with `class="test-moment"`.
- A screen that needs a different wide layout gets a second `<template data-desktop="same-id">`.

## Prompt template

### System prompt
```
You are a senior product designer and front-end prototyper. You build polished, clickable product prototypes as a single self-contained HTML file, the way a product team shows a concept to its sponsor. You define a small design system before designing screens, and you design every screen for the persona's real context.
```

### User prompt template
```
Build the prototype described below as one self-contained index.html.

## Screens and flow (confirmed by the team)
{screen_plan}

## The riskiest assumption and the test moment
{riskiest_assumption}

## PRD (P0 and P1 requirements)
{prd_content}

## PR/FAQ (headline, benefit, voice)
{prfaq_content}

## Personas and signals (context and realistic content)
{research_content}

## Design standards (optional)
{design_standards}

Follow the structure in this reference: a top bar with Flow, Mobile, and Desktop views; a Show test moment toggle; one screen per flow step with real states; working hash-route navigation; realistic content; a design system defined as CSS custom properties. Output only the HTML file.
```

## Flow

1. **Plan the screens with the team** (Step 1 of the skill): the flow, one line per screen, and the test moment.
2. **Generate** the whole file.
3. **Check it** against the quality bar below, and fix what fails before showing it.
4. **Save** it as the next version, `discovery/[project]/prototype/v[N].html`, never over an earlier one, copy it to `prototype/index.html`, and open it for a live preview (Quick: `open_in_session_tab`; other tools: open the file in a browser).

## Quality bar

| Check | Must |
|-------|:----:|
| One self-contained file, no external requests | Yes |
| Flow, Mobile, and Desktop views all work, and open from `#/flow`, `#/mobile`, `#/desktop` | Yes |
| Every P0 requirement appears on a screen | Yes |
| Every screen is reachable by clicking, and back works | Yes |
| The test moment is reachable in two taps from the start | Yes |
| Realistic content, no placeholder text | Yes |
| One accent color, consistent type and spacing | Yes |
| Contrast and tap-target sizes meet the accessibility rules | Yes |
