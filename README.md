# html2pdf

Convert HTML files to PDF using a headless Chromium browser. Fully renders CDN-linked
resources (Tailwind CSS, Google Fonts, icon libraries, etc.) before export. A full-screen
TUI lets you browse for the HTML file, set the output name, pick page size and margins.

---

## Features

- Renders HTML with a real Chromium engine — JavaScript executes, CDN stylesheets apply
- Waits for network idle before capturing, so lazy-loaded assets are included
- Full-screen TUI with a file browser, radio buttons, and a Convert button (powered by `textual`)
- Output filename entered in-app — `.pdf` extension is added automatically
- Landscape orientation toggle in the TUI

---

## Requirements

- [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) (or conda/mamba)
- Internet access at conversion time (for CDN resources in the HTML)

---

## Setup

### 1. Create the micromamba environment

```bash
micromamba create -n html2pdf python=3.11 -y
```

### 2. Install Python dependencies

```bash
micromamba run -n html2pdf pip install -r requirements.txt
```

### 3. Install Textual via conda-forge

```bash
micromamba install -n html2pdf -c conda-forge textual -y
```

### 4. Download the Chromium browser

Playwright needs a bundled Chromium binary (downloaded once, ~170 MB):

```bash
micromamba run -n html2pdf python -m playwright install chromium
```

---

## Usage

```
micromamba run -n html2pdf python html2pdf.py [start_dir]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `start_dir` | *(optional)* Directory to open in the file browser. Defaults to the current working directory. |

### Examples

```bash
# Open file browser starting from the current directory
micromamba run -n html2pdf python html2pdf.py

# Open file browser starting from a specific directory
micromamba run -n html2pdf python html2pdf.py ~/Documents
```

### Interactive TUI

A full-screen Textual interface opens with everything in one view:

```
┌─ html → pdf ──────────────────────────────────────────────┐
│                                                            │
│  ┌── Select HTML File ───────────────────────────────────┐ │
│  │ 📁 /Users/you/                                        │ │
│  │   📁 Documents/                                       │ │
│  │   📁 Desktop/                                         │ │
│  │     📄 report.html   ← click or Enter to select       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                            │
│  Output:  [report                          ]  .pdf         │
│                                                            │
│  ┌── Page Size ──────────┐  ┌── Margins ────────────────┐  │
│  │ ● A4  (210 × 297 mm) │  │ ● Default    (10 mm)      │  │
│  │ ○ A3  ...            │  │ ○ Narrow     (5 mm)       │  │
│  │ ○ ...                │  │ ○ No Border  (0 mm)       │  │
│  └──────────────────────┘  └───────────────────────────┘  │
│                                                            │
│  □ Landscape                      [ Convert to PDF ]       │
│  Selected: report.html                                     │
└────────────────────────────────────────────────────────────┘
```

**Workflow:**
1. Browse the file tree and click (or press `Enter`) on an HTML file — the output name is auto-filled with the file stem
2. Edit the output filename if needed (`.pdf` is appended automatically, saved next to the source file)
3. Pick page size and margins using `↑ ↓`
4. Tick Landscape if needed (`Space`)
5. Tab to `Convert to PDF` and press `Enter`

**Keyboard shortcuts:**

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Move focus between panels |
| `↑ ↓` | Navigate file tree / radio options |
| `Space` | Toggle Landscape checkbox / activate button |
| `Enter` | Select file / press focused button |
| `q` | Quit |

---

## Page sizes

| Option | Dimensions |
|--------|------------|
| A4 | 210 × 297 mm |
| A3 | 297 × 420 mm |
| A5 | 148 × 210 mm |
| Letter | 8.5 × 11 in |
| Legal | 8.5 × 14 in |
| Tabloid | 11 × 17 in |

## Margin presets

| Option | All sides |
|--------|-----------|
| Default | 10 mm |
| Narrow | 5 mm |
| No Border | 0 (edge-to-edge) |

---

## Activating the environment (optional)

If you prefer to activate the environment once per session instead of prefixing every command:

```bash
micromamba activate html2pdf
python html2pdf.py
```

Deactivate when done:

```bash
micromamba deactivate
```
