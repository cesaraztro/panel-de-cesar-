#!/usr/bin/env python3
"""Arma una propuesta AztroTech (máximo 2 hojas) a partir del cuerpo HTML.

Uso:
  python3 build.py cuerpo.html salida_sin_extension --title "Propuesta · Cliente · AZTROTECH" [--previews DIR]

Genera <salida>.html (autocontenido: fuentes y logo embebidos) y <salida>.pdf.
Sale con código 2 si el PDF tiene más de 2 hojas.
"""
import argparse, os, pathlib, re, shutil, subprocess, sys

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
MAX_PAGES = 2


def find_chromium():
    for c in (os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium", shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if c and os.path.exists(c):
            return c
    return None


def render_pdf(html_path, pdf_path):
    chrome = find_chromium()
    if chrome:
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    from playwright.sync_api import sync_playwright  # respaldo
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        pg.goto(html_path.resolve().as_uri()); pg.wait_for_timeout(1200)
        pg.pdf(path=str(pdf_path), format="Letter", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()


def count_pages(pdf_path):
    try:
        out = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        if m:
            return int(m.group(1))
    except FileNotFoundError:
        pass
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf_path.read_bytes()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("body"); ap.add_argument("out"); ap.add_argument("--title", required=True)
    ap.add_argument("--previews")
    a = ap.parse_args()

    body = pathlib.Path(a.body).read_text(encoding="utf-8")
    html = ("<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<title>{a.title}</title>\n<style>\n"
            + (ASSETS / "fonts.css").read_text(encoding="utf-8")
            + (ASSETS / "style.css").read_text(encoding="utf-8")
            + "</style>\n</head>\n<body>\n"
            + (ASSETS / "logo-symbol.svg").read_text(encoding="utf-8").strip() + "\n"
            + body + "\n</body>\n</html>\n")

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    html_path, pdf_path = out.with_suffix(".html"), out.with_suffix(".pdf")
    html_path.write_text(html, encoding="utf-8")
    render_pdf(html_path, pdf_path)
    pages = count_pages(pdf_path)

    if a.previews and shutil.which("pdftoppm"):
        pathlib.Path(a.previews).mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "80", "-png", str(pdf_path), str(pathlib.Path(a.previews) / "hoja")], check=True)

    print(f"{pdf_path} · {pages} hoja(s)")
    if pages > MAX_PAGES:
        print(f"ERROR: la propuesta pasa de {MAX_PAGES} hojas. Recorta contenido, no la tipografía.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
