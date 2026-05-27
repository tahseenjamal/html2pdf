#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

import questionary
from questionary import Style
from playwright.sync_api import sync_playwright

TUI_STYLE = Style([
    ("qmark",        "fg:#00afd7 bold"),
    ("question",     "bold"),
    ("answer",       "fg:#00afd7 bold"),
    ("pointer",      "fg:#00afd7 bold"),
    ("highlighted",  "fg:#00afd7 bold"),
    ("selected",     "fg:#ffffff bg:#00afd7 bold"),
    ("separator",    "fg:#444444"),
    ("instruction",  "fg:#888888"),
])

PDF_SIZES = [
    ("A4     (210 × 297 mm)",  {"width": "210mm", "height": "297mm"}),
    ("A3     (297 × 420 mm)",  {"width": "297mm", "height": "420mm"}),
    ("A5     (148 × 210 mm)",  {"width": "148mm", "height": "210mm"}),
    ("Letter (8.5 × 11 in)",   {"width": "8.5in", "height": "11in"}),
    ("Legal  (8.5 × 14 in)",   {"width": "8.5in", "height": "14in"}),
    ("Tabloid (11 × 17 in)",   {"width": "11in",  "height": "17in"}),
]

MARGINS = [
    ("Default   (10 mm)",  {"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}),
    ("Narrow    (5 mm)",   {"top": "5mm",  "bottom": "5mm",  "left": "5mm",  "right": "5mm"}),
    ("No Border (0 mm)",   {"top": "0",    "bottom": "0",    "left": "0",    "right": "0"}),
]


def choose(prompt: str, choices: list[tuple]) -> dict:
    labels = [label for label, _ in choices]
    answer = questionary.select(
        prompt,
        choices=labels,
        style=TUI_STYLE,
        use_shortcuts=False,
    ).ask()

    if answer is None:
        print("\nAborted.", file=sys.stderr)
        sys.exit(1)

    return next(value for label, value in choices if label == answer)


def convert(html_path: Path, output_path: Path, page_size: dict, margin: dict, landscape: bool) -> None:
    url = html_path.resolve().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=60_000)
        page.pdf(
            path=str(output_path),
            width=page_size["width"],
            height=page_size["height"],
            landscape=landscape,
            print_background=True,
            margin=margin,
        )
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an HTML file to PDF (CDN-aware).")
    parser.add_argument("html_file", help="Path to the HTML file")
    parser.add_argument("-o", "--output", help="Output PDF path (default: same name as input)")
    parser.add_argument("--landscape", action="store_true", help="Use landscape orientation")
    args = parser.parse_args()

    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"Error: '{html_path}' not found.", file=sys.stderr)
        sys.exit(1)
    if html_path.suffix.lower() not in {".html", ".htm"}:
        print("Warning: file does not have an .html/.htm extension, proceeding anyway.")

    output_path = Path(args.output) if args.output else html_path.with_suffix(".pdf")

    print()
    page_size = choose("Page size:", PDF_SIZES)
    margin    = choose("Margins:",   MARGINS)

    print(f"\nRendering '{html_path}' …")
    convert(html_path, output_path, page_size, margin, args.landscape)
    print(f"Saved: {output_path.resolve()}")


if __name__ == "__main__":
    main()
