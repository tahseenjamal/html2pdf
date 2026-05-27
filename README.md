# html2pdf

Convert HTML files to PDF using a headless Chromium browser. Fully renders CDN-linked
resources (Tailwind CSS, Google Fonts, icon libraries, etc.) before export. An interactive
TUI lets you choose page size and margins without touching any flags.

---

## Features

- Renders HTML with a real Chromium engine — JavaScript executes, CDN stylesheets apply
- Waits for network idle before capturing, so lazy-loaded assets are included
- Arrow-key TUI for page size and margin selection (powered by `questionary`)
- Landscape orientation via `--landscape`
- Custom output path via `-o`

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

### 3. Download the Chromium browser

Playwright needs a bundled Chromium binary (downloaded once, ~170 MB):

```bash
micromamba run -n html2pdf python -m playwright install chromium
```

---

## Usage

```
micromamba run -n html2pdf python html2pdf.py <html_file> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `html_file` | Path to the input HTML file |
| `-o, --output` | Output PDF path (default: same directory and name as input, `.pdf` extension) |
| `--landscape` | Render in landscape orientation |

### Examples

```bash
# Basic — output saved as report.pdf next to report.html
micromamba run -n html2pdf python html2pdf.py report.html

# Custom output path
micromamba run -n html2pdf python html2pdf.py report.html -o ~/Desktop/report.pdf

# Landscape
micromamba run -n html2pdf python html2pdf.py slides.html --landscape

# Landscape with custom output
micromamba run -n html2pdf python html2pdf.py slides.html --landscape -o slides.pdf
```

### Interactive prompts

After the command runs you will see two arrow-key menus:

```
? Page size:
  ❯ A4     (210 × 297 mm)
    A3     (297 × 420 mm)
    A5     (148 × 210 mm)
    Letter (8.5 × 11 in)
    Legal  (8.5 × 14 in)
    Tabloid (11 × 17 in)

? Margins:
  ❯ Default   (10 mm)
    Narrow    (5 mm)
    No Border (0 mm)
```

Use `↑ ↓` to navigate and `Enter` to confirm. Press `Ctrl+C` to abort.

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
python html2pdf.py report.html
```

Deactivate when done:

```bash
micromamba deactivate
```
