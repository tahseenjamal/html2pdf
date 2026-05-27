# html2pdf

Convert HTML files to PDF using a headless Chromium browser. Fully renders CDN-linked
resources (Tailwind CSS, Google Fonts, icon libraries, etc.) before export. A full-screen
TUI lets you browse for the HTML file, enter the output name, and pick page size, margins,
and orientation — all without touching the command line beyond launching the tool.

---

## Features

- Renders HTML with a real Chromium engine — JavaScript executes, CDN stylesheets apply
- Waits for network idle before capturing, so all CDN assets are fully loaded
- Full-screen TUI powered by [Textual](https://textual.textualize.io/)
  - File browser filtered to `.html` / `.htm` files, hidden files excluded
  - Output filename field — auto-filled from the selected file, `.pdf` appended automatically
  - Page size selector (A4, A3, A5, Letter, Legal, Tabloid)
  - Margin presets (Default 10 mm, Narrow 5 mm, No Border)
  - Landscape orientation toggle
- PDF saved in the same directory as the source HTML file

---

## Requirements

- [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) (or conda / mamba)
- Internet access at conversion time (to fetch CDN resources referenced in the HTML)

---

## Setup

### 1. Create the micromamba environment

```bash
micromamba create -n html2pdf python=3.11 -y
```

### 2. Install Python packages

`playwright` is installed via pip; `textual` is installed from conda-forge:

```bash
micromamba run -n html2pdf pip install -r requirements.txt
micromamba install -n html2pdf -c conda-forge textual -y
```

### 3. Download the Chromium browser

Playwright ships without a browser — download it once (~170 MB):

```bash
micromamba run -n html2pdf python -m playwright install chromium
```

---

## Usage

```bash
micromamba run -n html2pdf python html2pdf.py [start_dir]
```

| Argument | Description |
|----------|-------------|
| `start_dir` | *(optional)* Directory the file browser opens in. Defaults to the current working directory. |

### Examples

```bash
# Open file browser in the current directory
micromamba run -n html2pdf python html2pdf.py

# Open file browser in a specific directory
micromamba run -n html2pdf python html2pdf.py ~/Documents
```

---

## TUI walkthrough

```
┌─ html → pdf ──────────────────────────────────────────────────┐
│                                                                │
│  ┌── Select HTML File ─────────────────────────────────────┐  │
│  │ 📁 /Users/you/projects/                                 │  │
│  │   📁 reports/                                           │  │
│  │     📄 invoice.html   ← navigate here and press Enter   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
│  Output:  [ invoice                             ]   .pdf       │
│                                                                │
│  ┌── Page Size ──────────────┐  ┌── Margins ───────────────┐  │
│  │ ● A4       (210 × 297 mm)│  │ ● Default    (10 mm)     │  │
│  │ ○ A3       (297 × 420 mm)│  │ ○ Narrow     (5 mm)      │  │
│  │ ○ A5       (148 × 210 mm)│  │ ○ No Border  (0 mm)      │  │
│  │ ○ Letter   (8.5 × 11 in) │  └──────────────────────────┘  │
│  │ ○ Legal    (8.5 × 14 in) │                                 │
│  │ ○ Tabloid  (11 × 17 in)  │  □ Landscape                   │
│  └──────────────────────────┘                                 │
│                                      [ Convert to PDF ]       │
│  Selected: invoice.html                                       │
└───────────────────────────────────────────────────────────────┘
```

**Workflow:**

1. Navigate the file tree to your HTML file and press `Enter` (or click) — the output filename is auto-filled with the file stem
2. Edit the output name in the input field if needed
3. Choose page size and margins with `↑ ↓`
4. Tick **Landscape** with `Space` if needed
5. Tab to **Convert to PDF** and press `Enter`
6. The status bar shows progress and the saved path when done

**Keyboard reference:**

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Move focus between panels |
| `↑` / `↓` | Navigate file tree or radio options |
| `Enter` | Select highlighted file / activate focused button |
| `Space` | Toggle Landscape checkbox |
| `q` | Quit |

---

## Page sizes

| Size | Dimensions |
|------|------------|
| A4 | 210 × 297 mm |
| A3 | 297 × 420 mm |
| A5 | 148 × 210 mm |
| Letter | 8.5 × 11 in |
| Legal | 8.5 × 14 in |
| Tabloid | 11 × 17 in |

## Margin presets

| Preset | All sides |
|--------|-----------|
| Default | 10 mm |
| Narrow | 5 mm |
| No Border | 0 (edge-to-edge) |

---

## Activating the environment (optional)

Activate once per terminal session to avoid prefixing every command:

```bash
micromamba activate html2pdf
python html2pdf.py
micromamba deactivate   # when done
```
