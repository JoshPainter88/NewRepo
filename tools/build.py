#!/usr/bin/env python3
"""Build Cable Desk into one self-contained HTML file.

  python tools/build.py --data app/sample-data.json --out dist/demo.html
  python tools/build.py --data private/kb/os_data.json --files files.json --out dist/cable-desk.html
  python tools/build.py --data ... --artifact --out dist/artifact.html   # page body only, for claude.ai

The data file is the knowledge base (see README "Data contract"). --files is the optional
index written by tools/Build-FileIndex.ps1. Output with real data must stay out of git.
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "app" / "src"


def js_literal(obj) -> str:
    """JSON that is safe to place inside a <script> element."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def font_faces() -> str:
    """@font-face rules with the fonts inlined, so the local copy makes no network request."""
    import base64
    fonts_dir = ROOT / "app" / "fonts"
    rules = []
    for f in json.loads((fonts_dir / "fonts.json").read_text(encoding="utf-8")):
        b64 = base64.b64encode((fonts_dir / f["file"]).read_bytes()).decode("ascii")
        stretch = f"font-stretch:{f['stretch']};" if f.get("stretch") else ""
        rules.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%s;%sfont-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}" % (f["family"], f["weight"], stretch, b64)
        )
    return "<style>" + "".join(rules) + "</style>"


GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">' "\n"
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' "\n"
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900'
    '&family=JetBrains+Mono:wght@100..800&display=swap">'
)


def build(data_path, files_path, out_path, artifact):
    shell = (SRC / "shell.html").read_text(encoding="utf-8")
    css = (SRC / "styles.css").read_text(encoding="utf-8")
    app = (SRC / "app.js").read_text(encoding="utf-8")
    data = json.loads(pathlib.Path(data_path).read_text(encoding="utf-8"))
    files = None
    if files_path:
        raw = pathlib.Path(files_path).read_text(encoding="utf-8-sig").strip()
        if raw.startswith("window.OS_FILES"):
            raw = raw.split("=", 1)[1].strip().rstrip(";")
        files = json.loads(raw)

    page = (
        shell.replace("/*__CSS__*/", css)
        .replace("/*__DATA__*/", js_literal(data))
        .replace("/*__FILES__*/", js_literal(files))
        .replace("/*__APP__*/", app.replace("</script", "<\\/script"))
    )
    # Local copy: fonts inlined (no network), plus the optional file index Build-FileIndex.ps1 writes next to the page.
    page = page.replace("<!--__FONTS__-->", GOOGLE_FONTS if artifact else font_faces())
    local_scripts = '' if artifact else '<script src="cabledesk-files.js"></script>'
    page = page.replace("<!--__LOCAL_SCRIPTS__-->", local_scripts)
    if not artifact:
        page = (
            '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + page.replace('<div id="app"', '</head>\n<body>\n<div id="app"', 1)
            + "\n</body>\n</html>\n"
        )
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="knowledge-base JSON")
    ap.add_argument("--files", help="optional file index (files.json or files.js)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--artifact", action="store_true", help="emit page body only (claude.ai adds the document skeleton)")
    a = ap.parse_args()
    build(a.data, a.files, a.out, a.artifact)
