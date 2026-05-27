#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, RadioSet, RadioButton, Button,
    Label, Checkbox, Static, Input, DirectoryTree,
)
from textual.containers import Horizontal, Vertical, Container
from textual import work, on

from playwright.sync_api import sync_playwright

# ── Data ──────────────────────────────────────────────────────────────────────

PDF_SIZES = [
    ("A4       (210 × 297 mm)",  {"width": "210mm", "height": "297mm"}),
    ("A3       (297 × 420 mm)",  {"width": "297mm", "height": "420mm"}),
    ("A5       (148 × 210 mm)",  {"width": "148mm", "height": "210mm"}),
    ("Letter   (8.5 × 11 in)",   {"width": "8.5in", "height": "11in"}),
    ("Legal    (8.5 × 14 in)",   {"width": "8.5in", "height": "14in"}),
    ("Tabloid  (11 × 17 in)",    {"width": "11in",  "height": "17in"}),
]

MARGINS = [
    ("Default    (10 mm)",  {"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"}),
    ("Narrow     (5 mm)",   {"top": "5mm",  "bottom": "5mm",  "left": "5mm",  "right": "5mm"}),
    ("No Border  (0 mm)",   {"top": "0",    "bottom": "0",    "left": "0",    "right": "0"}),
]

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
Screen {
    background: $surface;
    layout: vertical;
}

/* ── File browser ── */
#browser-panel {
    border: round $accent;
    height: 14;
    margin: 1 1 0 1;
    padding: 0 1;
}

#browser-title {
    color: $accent;
    text-style: bold;
    padding: 0 0 1 0;
}

#file-tree {
    height: 1fr;
    scrollbar-gutter: stable;
}

/* ── Output row ── */
#output-row {
    height: 3;
    margin: 1 1 0 1;
    align: left middle;
}

#output-label {
    width: 10;
    color: $text-muted;
}

#output-input {
    width: 1fr;
}

#ext-label {
    width: 5;
    color: $accent;
    text-style: bold;
    padding-left: 1;
}

/* ── Size / Margin panels ── */
#panels {
    height: auto;
    margin: 1 1 0 1;
}

.panel {
    border: round $accent;
    padding: 1 2;
    margin: 0 1 0 0;
    width: 1fr;
    height: auto;
}

.panel:last-of-type {
    margin-right: 0;
}

.panel-title {
    text-style: bold;
    color: $accent;
    padding-bottom: 1;
}

/* ── Bottom bar ── */
#bottom-row {
    height: 3;
    margin: 1 1 0 1;
    align: left middle;
}

#landscape-check {
    width: 1fr;
}

#convert-btn {
    width: 22;
    height: 1;
    border: none;
    background: $accent;
    color: $background;
    text-style: bold;
}

#convert-btn:hover {
    background: $accent-lighten-1;
}

#convert-btn:focus {
    border: none;
    background: $accent-darken-1;
}

/* ── Status ── */
#status {
    height: 2;
    margin: 0 2;
    text-align: center;
}

.status-idle    { color: $text-muted; }
.status-working { color: $warning;  text-style: bold; }
.status-done    { color: $success;  text-style: bold; }
.status-error   { color: $error;    text-style: bold; }
"""

# ── Widgets ───────────────────────────────────────────────────────────────────

class HtmlFileTree(DirectoryTree):
    """DirectoryTree that shows only directories and HTML files."""

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [
            p for p in paths
            if not p.name.startswith(".")
            and (p.is_dir() or p.suffix.lower() in {".html", ".htm"})
        ]

# ── App ───────────────────────────────────────────────────────────────────────

class Html2PdfApp(App):
    CSS = CSS
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, start_dir: Path):
        super().__init__()
        self.start_dir  = start_dir
        self.html_path: Path | None = None
        self._size_index   = 0
        self._margin_index = 0
        self._landscape    = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        # File browser
        with Container(id="browser-panel"):
            yield Static("Select HTML File", id="browser-title")
            yield HtmlFileTree(self.start_dir, id="file-tree")

        # Output filename
        with Horizontal(id="output-row"):
            yield Static("Output:", id="output-label")
            yield Input(placeholder="enter output filename…", id="output-input")
            yield Static(".pdf", id="ext-label")

        # Page size + margins
        with Horizontal(id="panels"):
            with Vertical(classes="panel"):
                yield Static("Page Size", classes="panel-title")
                with RadioSet(id="size-set"):
                    for i, (label, _) in enumerate(PDF_SIZES):
                        yield RadioButton(label, value=(i == 0))

            with Vertical(classes="panel"):
                yield Static("Margins", classes="panel-title")
                with RadioSet(id="margin-set"):
                    for i, (label, _) in enumerate(MARGINS):
                        yield RadioButton(label, value=(i == 0))

        # Landscape + Convert
        with Horizontal(id="bottom-row"):
            yield Checkbox("Landscape", id="landscape-check")
            yield Button("Convert to PDF", variant="default", id="convert-btn")

        yield Static("Select an HTML file to begin", id="status", classes="status-idle")
        yield Footer()

    # ── Events ────────────────────────────────────────────────────────────────

    @on(DirectoryTree.FileSelected, "#file-tree")
    def file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.html_path = event.path
        output_input = self.query_one("#output-input", Input)
        output_input.value = event.path.stem
        self._set_status(f"Selected: {event.path.name}", "status-idle")

    @on(RadioSet.Changed, "#size-set")
    def size_changed(self, event: RadioSet.Changed) -> None:
        self._size_index = event.index

    @on(RadioSet.Changed, "#margin-set")
    def margin_changed(self, event: RadioSet.Changed) -> None:
        self._margin_index = event.index

    @on(Checkbox.Changed, "#landscape-check")
    def landscape_changed(self, event: Checkbox.Changed) -> None:
        self._landscape = event.value

    @on(Button.Pressed, "#convert-btn")
    def convert_pressed(self) -> None:
        if self.html_path is None:
            self._set_status("Please select an HTML file first.", "status-error")
            return

        output_name = self.query_one("#output-input", Input).value.strip()
        if not output_name:
            self._set_status("Please enter an output filename.", "status-error")
            return

        output_path = self.html_path.parent / (output_name + ".pdf")
        self._run_convert(output_path)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_status(self, msg: str, css_class: str) -> None:
        status = self.query_one("#status", Static)
        status.update(msg)
        status.set_classes(css_class)

    @work(thread=True)
    def _run_convert(self, output_path: Path) -> None:
        btn = self.query_one("#convert-btn", Button)

        self.call_from_thread(self._set_status, "Rendering — please wait…", "status-working")
        self.call_from_thread(setattr, btn, "disabled", True)

        try:
            _, page_size = PDF_SIZES[self._size_index]
            _, margin    = MARGINS[self._margin_index]

            url = self.html_path.resolve().as_uri()
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page    = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=60_000)
                page.pdf(
                    path=str(output_path),
                    width=page_size["width"],
                    height=page_size["height"],
                    landscape=self._landscape,
                    print_background=True,
                    margin=margin,
                )
                browser.close()

            self.call_from_thread(self._set_status, f"Saved: {output_path.resolve()}", "status-done")
        except Exception as exc:
            self.call_from_thread(self._set_status, f"Error: {exc}", "status-error")
        finally:
            self.call_from_thread(setattr, btn, "disabled", False)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an HTML file to PDF (CDN-aware).")
    parser.add_argument(
        "start_dir",
        nargs="?",
        default=str(Path.cwd()),
        help="Directory to open in the file browser (default: current directory)",
    )
    args = parser.parse_args()

    start_dir = Path(args.start_dir)
    if not start_dir.is_dir():
        print(f"Error: '{start_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    Html2PdfApp(start_dir).run()


if __name__ == "__main__":
    main()
