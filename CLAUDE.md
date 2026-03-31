# CLAUDE.md — CyberAtlas

AI assistant guide for the CyberAtlas repository.

---

## Project Overview

**CyberAtlas** is a static single-page application that displays tech events in France on an interactive map. It has a cyberpunk aesthetic (dark purple/cyan theme) and is written in French.

Created entirely with Claude AI by a non-developer (`README.md` states: "Site fait entierement avec Claude.ai je ne suis pas dev").

**Live stack:**
- HTML5 + CSS3 + Vanilla JavaScript (no framework, no build step)
- [Leaflet.js v1.9.4](https://unpkg.com/leaflet@1.9.4) — interactive map
- OpenStreetMap tiles — map background
- Google Fonts — Orbitron, Space Mono, Share Tech Mono
- `events.json` — local JSON file used as the data source

---

## Repository Structure

```
/
├── index.html      # Entire application: HTML structure, CSS, and JavaScript
├── events.json     # Event data (array of event objects)
└── README.md       # One-line description
```

No build system, no package manager, no test suite, no CI/CD.

---

## Architecture

Everything lives in `index.html`. It is divided into three sections:

### 1. `<style>` block (lines 12–428)
All CSS is embedded inline using CSS custom properties (variables). The design system is defined in `:root`.

### 2. HTML markup (lines 430–469)
Three structural regions:
- `#header` — logo, region switcher buttons, status bar
- `#sidebar` — date filter input + scrollable event card list
- `#map` — Leaflet map container

### 3. `<script>` block (lines 471–602)
All JavaScript is inline. Key globals and functions:

| Symbol | Purpose |
|---|---|
| `REGIONS` | Object with `paris`, `sud`, `france` — each has `center: [lat, lng]` and `zoom` |
| `allEvents` | Array of all event objects loaded from `events.json` |
| `markers` | Array of `{ id, layer }` — tracks active Leaflet marker layers |
| `activeCard` / `activeMarkerId` | Track currently highlighted event |
| `setRegion(name)` | Fly the map to a named region |
| `renderAll(events)` | Re-render both the sidebar list and map markers |
| `renderList(events)` | Build sidebar event cards from filtered events |
| `renderMarkers(events)` | Remove old markers and place new ones on the map |
| `focusEvent(id)` | Center map on an event and open its popup |
| `setActiveCard(id)` | Highlight a sidebar card and scroll it into view |
| `setActiveMarker(id)` | Toggle the `.active` CSS class on a map marker DOM element |
| `buildPopup(e)` | Return HTML string for a Leaflet popup |
| `formatDate(dateStr)` | Convert `"YYYY-MM-DD"` to French short format e.g. `"5 avr 2026"` |
| `clearDate()` | Reset date filter and show all events |

---

## Data Format

`events.json` is an array of event objects. Each object follows this schema:

```json
{
  "id": 1,
  "title": "Event Title",
  "description": "French description text.",
  "date": "2026-04-05",
  "time": "20:00",
  "location": {
    "lat": 48.8566,
    "lng": 2.3522,
    "label": "FabLab République, Paris"
  },
  "link": "https://example.com/event-slug",
  "tags": ["tag1", "tag2"]
}
```

- `id` — unique integer, sequential
- `date` — ISO 8601 (`YYYY-MM-DD`), used for filtering
- `time` — 24-hour `HH:MM` string, display only
- `location.lat` / `location.lng` — WGS84 decimal degrees
- `tags` — short lowercase French strings for the tag pills

---

## Design System

CSS variables defined in `:root` of `index.html`:

| Variable | Value | Role |
|---|---|---|
| `--void` | `#08060f` | Deepest background |
| `--deep` | `#0e0b1a` | Header / sidebar background |
| `--surface` | `#13102b` | Card / input background |
| `--panel` | `#1a1535` | Active card / popup background |
| `--border` | `#2a2060` | Default border color |
| `--purple` | `#7c3aed` | Primary accent |
| `--purple-hi` | `#a855f7` | Highlighted purple text |
| `--violet` | `#c084fc` | Card titles |
| `--cyan` | `#22d3ee` | Secondary accent (dates, meta) |
| `--text` | `#e2d9f3` | Default body text |
| `--text-dim` | `#7c6fa0` | Subdued text |
| `--text-muted` | `#3d3560` | Very subdued / label text |

**Fonts:**
- `Orbitron` — headings, logo, buttons, card titles (sci-fi display font)
- `Space Mono` — body text, popups (default `font-family`)
- `Share Tech Mono` — metadata, tags, inputs

The map tiles receive a CSS filter (`brightness(0.35) saturate(0.6) hue-rotate(220deg) contrast(1.1)`) to match the dark purple theme.

---

## Development Workflow

There is no build step. To work on this project:

1. Open `index.html` directly in a browser, **or** serve it from a local HTTP server (required for `fetch('events.json')` to work due to CORS restrictions on `file://` URLs):
   ```bash
   python3 -m http.server 8080
   # then open http://localhost:8080
   ```

2. Edit `index.html` for UI/logic changes.
3. Edit `events.json` to add, remove, or update events.

There is no linter, formatter, or test runner configured.

---

## Git Workflow

- **Main branch:** `main`
- **Feature branches:** use prefix `claude/` for AI-assisted work
- Commit messages are in English, concise and descriptive
- No PR template or contribution guidelines exist

To push changes:
```bash
git add index.html events.json   # or specific files
git commit -m "Describe the change"
git push -u origin <branch-name>
```

---

## Key Conventions

- **Language:** UI text and event data are in **French**. Code (variable names, comments) is in **English**.
- **No dependencies to install** — everything is loaded via CDN (`unpkg.com`, `fonts.googleapis.com`).
- **No TypeScript, no JSX, no modules** — plain ES5-compatible JavaScript.
- **All state is in-memory** — there is no localStorage, sessionStorage, or cookies.
- **IDs are integers** — event `id` values must be unique integers; increment from the highest existing value when adding events.
- **Inline HTML in JS** — `buildPopup()` and `renderList()` return raw HTML strings. Sanitize any user-facing input if it is ever introduced.
- **Map zoom levels** — Paris: 11, Sud: 8, France: 6. Use `map.flyTo()` for animated transitions.

---

## Common Tasks

### Add a new event
Append an object to `events.json` following the schema above. Increment `id` from the current maximum (currently 8).

### Add a new map region
Add an entry to the `REGIONS` object in `index.html`:
```js
const REGIONS = {
  paris:  { center: [48.857, 2.347], zoom: 11 },
  sud:    { center: [43.65,  6.15],  zoom: 8  },
  france: { center: [46.6,   2.4],   zoom: 6  },
  // add new region here
};
```
Then add a button in the `#header` HTML and wire it to `setRegion('newname')`.

### Change the color scheme
Edit the CSS variables in the `:root` block at the top of the `<style>` section. The map tile filter (`.leaflet-tile`) may also need adjusting.

### Filter events by tag
Currently no tag filter exists. To add one, filter `allEvents` by tag before passing to `renderAll()`, following the same pattern as the date filter.

---

## External Dependencies (CDN)

| Library | Version | URL |
|---|---|---|
| Leaflet CSS | 1.9.4 | `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css` |
| Leaflet JS | 1.9.4 | `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js` |
| Google Fonts | — | `https://fonts.googleapis.com/css2?...` |
| OpenStreetMap tiles | — | `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` |

Pin Leaflet to `@1.9.4` — do not upgrade without testing map marker and popup styling.
