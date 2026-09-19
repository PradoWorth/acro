# -*- coding: utf-8 -*-
"""Captura telas do site em várias larguras e detecta overflow horizontal."""
import http.server
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(ROOT) if os.path.basename(ROOT) == "src" else ROOT, "dist")
SHOTS = os.path.join(ROOT, "shots")
PORT = 8765

VIEWPORTS = {
    "360": (360, 800), "390": (390, 844), "430": (430, 932),
    "768": (768, 1024), "1024": (1024, 768), "1366": (1366, 900),
    "1440": (1440, 900), "1920": (1920, 1080),
    "desktop": (1440, 900), "tablet": (768, 1024), "mobile": (390, 844),
}


def serve():
    os.chdir(DIST)
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main(pages, widths, full=True):
    os.makedirs(SHOTS, exist_ok=True)
    serve()
    issues = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in widths:
            vw, vh = VIEWPORTS[w]
            ctx = browser.new_context(viewport={"width": vw, "height": vh},
                                      device_scale_factor=1, locale="pt-BR")
            page = ctx.new_page()
            for name in pages:
                url = f"http://127.0.0.1:{PORT}/{name}"
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(450)
                if full:
                    page.evaluate("""async () => {
                      const h = document.body.scrollHeight;
                      for (let y = 0; y < h; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
                      window.scrollTo(0, 0);
                    }""")
                    page.wait_for_timeout(700)
                    # As faixas de conteúdo usam content-visibility:auto (ver
                    # site.css, seção das .band): o navegador pula a
                    # renderização do que está fora da tela, e numa captura de
                    # página inteira essas faixas saem EM BRANCO — a página
                    # publicada está certa, a foto é que engana. Desligar a
                    # regra só na hora da captura devolve a página inteira
                    # desenhada. Não vale para a impressão, onde o Chrome já
                    # renderiza tudo (conferido gerando o PDF).
                    page.add_style_tag(content="*{content-visibility:visible!important}")
                    page.wait_for_timeout(350)
                over = page.evaluate(
                    "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if over > 0:
                    culprits = page.evaluate("""() => {
                      const out = [];
                      const lim = document.documentElement.clientWidth;
                      document.querySelectorAll('*').forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (r.width > 0 && (r.right > lim + 1 || r.left < -1)) {
                          out.push(el.tagName + '.' + (el.className || '').toString().slice(0, 60)
                                   + ' [' + Math.round(r.left) + '..' + Math.round(r.right) + ']');
                        }
                      });
                      return out.slice(0, 6);
                    }""")
                    issues.append(f"{name} @{w}: overflow {over}px -> {culprits}")
                out = os.path.join(SHOTS, f"{name.replace('/', '_').replace('.html', '')}--{w}.png")
                page.screenshot(path=out, full_page=full)
            ctx.close()
        browser.close()
    if issues:
        print("PROBLEMAS:")
        for i in issues:
            print(" -", i)
    else:
        print("Sem overflow horizontal.")


if __name__ == "__main__":
    pages = sys.argv[1].split(",") if len(sys.argv) > 1 else ["index.html"]
    widths = sys.argv[2].split(",") if len(sys.argv) > 2 else ["desktop"]
    full = (len(sys.argv) <= 3 or sys.argv[3] != "viewport")
    main(pages, widths, full)
