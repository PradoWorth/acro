# -*- coding: utf-8 -*-
"""
Auditoria do sistema de design.

Mede os valores realmente computados pelo navegador em todas as páginas, em
três larguras, e acusa qualquer coisa fora da escala definida em :root.
Serve para provar que o site é consistente, em vez de confiar no olho.

    python3 design_audit.py
"""
import http.server
import json
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT) if os.path.basename(ROOT) == "src" else ROOT
DIST = os.path.join(BASE, "dist")
PORT = 8910

VIEWPORTS = [("desktop", 1440, 900), ("tablet", 768, 1024), ("mobile", 390, 844)]

# Escala tipográfica do sistema, em px (item 157: textos maiores em todo o
# site — nano/micro/sm/xs/body/lead/h3/h4 subiram, h1/h2/display ganharam um
# degrau extra por faixa; ver :root em site.css)
FONT_SIZES = {12, 13, 16, 18, 20, 22, 24, 26, 30, 32, 34, 40, 44, 48, 60}

# Grade de 8px, mais os meios-passos aceitos (4px) e valores de controle
SPACING_OK = {0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80,
              96, 112, 120, 128, 136, 160}

RADII_OK = {0, 2, 6, 16, 40, 50, 100, 1000}

FONT_WEIGHTS = {400, 500, 600, 700}

# Famílias tipográficas do sistema. Duas, de propósito: Inter (texto corrido,
# UI, h3/h4) e Manrope em negrito (h1/h2 — títulos principais e de seção; ver
# site.css e fonts.css). Qualquer família fora desse par é que acusa problema.
FONT_FAMILIES_OK = {"Inter", "Manrope"}


COLLECT = r"""
() => {
  const px = v => Math.round(parseFloat(v) * 100) / 100;
  const out = { fonts:{}, sizes:{}, weights:{}, colors:{}, radii:{}, spacing:{}, samples:{} };
  const note = (bucket, key, el) => {
    out[bucket][key] = (out[bucket][key] || 0) + 1;
    if (!out.samples[bucket + ':' + key]) {
      out.samples[bucket + ':' + key] =
        (el.tagName + '.' + (el.className||'').toString().split(' ')[0]).slice(0, 44)
        + ' :: ' + (el.innerText||'').trim().slice(0, 26);
    }
  };
  document.querySelectorAll('body *').forEach(el => {
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE' || el.tagName === 'SVG') return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const hasText = (el.innerText||'').trim() && !el.children.length;

    if (hasText) {
      note('fonts', cs.fontFamily.split(',')[0].replace(/["']/g,''), el);
      note('sizes', String(px(cs.fontSize)), el);
      note('weights', String(cs.fontWeight), el);
      note('colors', cs.color, el);
    }
    const r = px(cs.borderTopLeftRadius);
    if (r > 0) note('radii', String(r), el);

    ['marginTop','marginBottom','paddingTop','paddingBottom','paddingLeft','paddingRight','gap']
      .forEach(prop => {
        const v = cs[prop];
        if (!v || v === 'normal') return;
        const n = px(v);
        if (n > 0) note('spacing', String(n), el);
      });
  });
  return out;
}
"""


def serve():
    """Devolve a porta realmente aberta — cai para porta 0 (o sistema
    escolhe uma livre) se a preferida estiver ocupada."""
    os.chdir(DIST)
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", PORT), http.server.SimpleHTTPRequestHandler)
    except OSError:
        httpd = socketserver.TCPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1]


def all_pages():
    pages = []
    for root, _, names in os.walk(DIST):
        for n in sorted(names):
            if not n.endswith(".html"):
                continue
            pages.append(os.path.relpath(os.path.join(root, n), DIST).replace(os.sep, "/"))
    return sorted(pages)


def main():
    if not os.path.isdir(DIST):
        sys.exit("dist/ não encontrado. Rode build.py antes.")
    pages = all_pages()
    port = serve()

    agg = {k: {} for k in ("fonts", "sizes", "weights", "colors", "radii", "spacing")}
    samples = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            for u in pages:
                page.goto(f"http://127.0.0.1:{port}/{u}", wait_until="networkidle")
                page.wait_for_timeout(60)
                data = page.evaluate(COLLECT)
                for bucket in agg:
                    for k, v in data[bucket].items():
                        agg[bucket].setdefault(k, {}).setdefault(label, 0)
                        agg[bucket][k][label] += v
                for k, v in data["samples"].items():
                    samples.setdefault(k, (label, u, v))
            page.close()
        browser.close()

    problems = []

    print(f"Analisadas {len(pages)} páginas × {len(VIEWPORTS)} larguras\n")

    print("— Famílias tipográficas —")
    for f, per in sorted(agg["fonts"].items(), key=lambda x: -sum(x[1].values())):
        total = sum(per.values())
        print(f"   {f:<28} {total:>6}")
        if f not in FONT_FAMILIES_OK:
            problems.append(f"Família fora do sistema: {f} ({total} ocorrências) "
                            f"ex.: {samples.get('fonts:'+f, ('','',''))[2]}")

    print("\n— Tamanhos de fonte (px) —")
    for size, per in sorted(agg["sizes"].items(), key=lambda x: float(x[0])):
        total = sum(per.values())
        ok = float(size) in FONT_SIZES
        flag = "" if ok else "  <-- fora da escala"
        print(f"   {size:>7} px  {total:>6}{flag}")
        if not ok:
            lbl, pg, ex = samples.get("sizes:" + size, ("", "", ""))
            problems.append(f"Tamanho fora da escala: {size}px em {pg} ({lbl}) -> {ex}")

    print("\n— Pesos —")
    for wgt, per in sorted(agg["weights"].items(), key=lambda x: int(x[0])):
        total = sum(per.values())
        ok = int(wgt) in FONT_WEIGHTS
        print(f"   {wgt:>7}    {total:>6}{'' if ok else '  <-- fora do sistema'}")
        if not ok:
            problems.append(f"Peso fora do sistema: {wgt}")

    print("\n— Raios de borda (px) —")
    for r, per in sorted(agg["radii"].items(), key=lambda x: float(x[0])):
        total = sum(per.values())
        ok = float(r) in RADII_OK
        print(f"   {r:>7} px  {total:>6}{'' if ok else '  <-- fora do sistema'}")
        if not ok:
            lbl, pg, ex = samples.get("radii:" + r, ("", "", ""))
            problems.append(f"Raio fora do sistema: {r}px em {pg} -> {ex}")

    print("\n— Espaçamentos fora da grade de 8px —")
    off = []
    for sp, per in agg["spacing"].items():
        val = float(sp)
        if val in SPACING_OK:
            continue
        off.append((val, sum(per.values()), samples.get("spacing:" + sp, ("", "", ""))))
    off.sort(key=lambda x: -x[1])
    if not off:
        print("   nenhum")
    for val, total, (lbl, pg, ex) in off[:14]:
        print(f"   {val:>7} px  {total:>6}   {pg} -> {ex}")
        problems.append(f"Espaçamento fora da grade: {val}px ({total}x) -> {ex}")

    print("\n— Cores de texto distintas —")
    for c, per in sorted(agg["colors"].items(), key=lambda x: -sum(x[1].values())):
        print(f"   {c:<26} {sum(per.values()):>6}")

    print()
    if problems:
        print(f"{len(problems)} ponto(s) a padronizar.")
    else:
        print("Sistema consistente: nada fora da escala.")
    return problems


if __name__ == "__main__":
    main()
