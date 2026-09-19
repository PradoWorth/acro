# -*- coding: utf-8 -*-
"""Auditoria de renderização: overflow, contraste, alvos de toque, colunas
desbalanceadas, órfãos tipográficos e consistência entre páginas equivalentes.
"""
import http.server
import os
import socketserver
import sys
import threading
from collections import defaultdict

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT) if os.path.basename(ROOT) == "src" else ROOT
DIST = os.path.join(BASE, "dist")
PORT = 9135

VIEWPORTS = [("desktop", 1440, 900), ("tablet", 768, 1024), ("mobile", 390, 844)]

CHECK = r"""
() => {
  const out = { overflow: [], contrast: [], tap: [], gaps: [], orphan: [], misc: [] };
  const vw = document.documentElement.clientWidth;

  // --- overflow horizontal
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    // Atalho de teclado escondido fora da tela pela técnica clássica: só
    // aparece no foco, não é conteúdo transbordando.
    if (r.right < 0 && r.left < -2000) return;
    if (r.right > vw + 2 || r.left < -2) {
      // ignora o que está deliberadamente em carrossel com overflow próprio
      let p = el.parentElement, scrolls = false;
      while (p && p !== document.body) {
        const pc = getComputedStyle(p);
        if (pc.overflowX === 'auto' || pc.overflowX === 'scroll' || pc.overflowX === 'hidden') { scrolls = true; break; }
        p = p.parentElement;
      }
      if (!scrolls) out.overflow.push({
        sel: el.tagName + '.' + String(el.className || '').split(' ')[0],
        left: Math.round(r.left), right: Math.round(r.right), vw,
        text: (el.innerText || '').trim().slice(0, 40)
      });
    }
  });

  // --- contraste de texto (WCAG)
  const lum = (r, g, b) => {
    const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const parse = s => (s.match(/[\d.]+/g) || []).map(Number);
  const bgOf = el => {
    let p = el;
    while (p && p !== document.documentElement) {
      const c = getComputedStyle(p).backgroundColor;
      const v = parse(c);
      if (v.length >= 3 && (v.length < 4 || v[3] > 0.5)) return v;
      p = p.parentElement;
    }
    return [255, 255, 255];
  };
  // O que está realmente pintado atrás do texto. Subir a árvore procurando uma
  // cor de fundo erra quando o elemento é transparente sobre uma arte escura
  // (é o caso do cabeçalho sobre o hero): a busca chega no body branco e acusa
  // texto branco sobre branco que na tela nunca acontece.
  const paintedBg = el => {
    const r = el.getBoundingClientRect();
    const x = r.left + Math.min(r.width / 2, 40), y = r.top + r.height / 2;
    if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) return null;
    for (const e of document.elementsFromPoint(x, y)) {
      if (e === el || el.contains(e)) continue;
      const cs = getComputedStyle(e);
      const v = parse(cs.backgroundColor);
      if (v.length >= 3 && (v.length < 4 || v[3] > 0.5)) return v;
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;  // arte: não dá para medir
      if (e.tagName === 'IMG' || e.tagName === 'SVG' || e.querySelector('img, svg')) return null;
    }
    return null;
  };

  const seen = new Set();
  document.querySelectorAll('body *').forEach(el => {
    if (!el.innerText || el.children.length) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.5) return;
    const painted = paintedBg(el);
    if (painted === null) return;              // fora da viewport ou sobre arte
    const fg = parse(cs.color), bg = painted;
    if (fg.length < 3) return;
    const L1 = lum(fg[0], fg[1], fg[2]), L2 = lum(bg[0], bg[1], bg[2]);
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    if (ratio < need) {
      const key = cs.color + '|' + bg.join(',') + '|' + Math.round(size);
      if (!seen.has(key)) {
        seen.add(key);
        out.contrast.push({
          ratio: Math.round(ratio * 100) / 100, need, color: cs.color,
          bg: 'rgb(' + bg.slice(0, 3).join(',') + ')', size,
          sel: el.tagName + '.' + String(el.className || '').split(' ')[0],
          text: el.innerText.trim().slice(0, 40)
        });
      }
    }
  });

  // --- alvos de toque pequenos (mobile)
  // Conta a área que o dedo realmente acerta, e não só a caixa do elemento:
  // vários links ganham um ::after invisível justamente para ampliar o alvo
  // sem mexer na tipografia, e ignorar isso acusaria erro onde já foi tratado.
  if (vw <= 480) {
    document.querySelectorAll('a, button, input, select, [role=tab], label.choice').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      if (el.closest('[hidden], [aria-hidden=true], .sr')) return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      const after = getComputedStyle(el, '::after');
      let h = r.height, w = r.width;
      if (after && after.content && after.content !== 'none') {
        const ah = parseFloat(after.height);
        if (!isNaN(ah)) h = Math.max(h, ah);
      }
      // Um input dentro de (ou ligado a) um <label> é acionado clicando em
      // qualquer ponto do rótulo — é ELE o alvo que o dedo acerta. Medir só
      // a caixinha de 24px do checkbox acusaria um problema que não existe.
      if (el.tagName === 'INPUT') {
        const lab = el.closest('label') ||
                    (el.id ? document.querySelector('label[for="' + CSS.escape(el.id) + '"]') : null);
        if (lab) {
          const lr = lab.getBoundingClientRect();
          if (lr.width && lr.height) { h = Math.max(h, lr.height); w = Math.max(w, lr.width); }
        }
      }
      if (h < 40 || w < 40) {
        // links inline dentro de parágrafo são aceitáveis
        const inline = el.tagName === 'A' && cs.display === 'inline';
        if (!inline) out.tap.push({
          sel: el.tagName + '.' + String(el.className || '').split(' ')[0],
          w: Math.round(w), h: Math.round(h),
          text: (el.innerText || '').trim().slice(0, 30)
        });
      }
    });
  }

  // --- colunas muito desbalanceadas (buraco branco)
  if (vw >= 1000) {
    document.querySelectorAll('.cols').forEach(el => {
      const kids = [...el.children].filter(k => getComputedStyle(k).display !== 'none');
      if (kids.length !== 2) return;
      const h = kids.map(k => k.getBoundingClientRect().height);
      const contentH = kids.map(k => {
        const cs = [...k.querySelectorAll('*')].map(c => c.getBoundingClientRect());
        if (!cs.length) return k.getBoundingClientRect().height;
        const top = Math.min(...cs.map(r => r.top)), bot = Math.max(...cs.map(r => r.bottom));
        return bot - top;
      });
      const diff = Math.abs(contentH[0] - contentH[1]);
      const sticky = el.className.includes('sticky');
      if (diff > 260 && !sticky) out.gaps.push({
        cls: el.className, h0: Math.round(contentH[0]), h1: Math.round(contentH[1]),
        diff: Math.round(diff),
        text: (kids[0].innerText || '').trim().slice(0, 44).replace(/\n/g, ' ')
      });
    });
  }

  // --- órfãos: título cuja última linha tem 1 palavra curta
  document.querySelectorAll('h1, h2, h3').forEach(el => {
    const t = (el.innerText || '').trim();
    if (!t || t.split(/\s+/).length < 4) return;
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()];
    if (rects.length < 2) return;
    const lastTop = Math.max(...rects.map(r => r.top));
    const lastLine = rects.filter(r => Math.abs(r.top - lastTop) < 3);
    const width = lastLine.reduce((s, r) => s + r.width, 0);
    const total = el.getBoundingClientRect().width;
    if (width > 0 && width / total < 0.16) out.orphan.push({
      tag: el.tagName, pct: Math.round(width / total * 100), text: t.slice(0, 56)
    });
  });

  // --- diversos
  document.querySelectorAll('[style*="font-size"]').forEach(el => {
    out.misc.push({ kind: 'font-size inline', sel: el.tagName + '.' + String(el.className || '').split(' ')[0] });
  });
  return out;
}
"""


def serve():
    """Sobe o servidor local e devolve (srv, porta).

    allow_reuse_address precisa estar na CLASSE antes de instanciar: o bind
    acontece dentro do __init__, então setar no objeto depois não tem efeito
    nenhum (era essa a causa dos "Address already in use" em socket ainda em
    TIME_WAIT). E se a porta preferida estiver mesmo ocupada, cai para porta
    0 e deixa o sistema escolher uma livre, em vez de abortar a auditoria.
    """
    os.chdir(DIST)
    h = http.server.SimpleHTTPRequestHandler
    h.log_message = lambda *a, **k: None
    socketserver.TCPServer.allow_reuse_address = True
    try:
        srv = socketserver.TCPServer(("127.0.0.1", PORT), h)
    except OSError:
        srv = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def pages():
    out = []
    for root, _, names in os.walk(DIST):
        for n in sorted(names):
            if n.endswith(".html"):
                out.append(os.path.relpath(os.path.join(root, n), DIST))
    return sorted(out)


def main():
    srv, port = serve()
    buckets = defaultdict(list)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for vname, w, h in VIEWPORTS:
            # has_touch faz o navegador reportar pointer:coarse. Sem isso o
            # Chromium headless se apresenta como mouse e as regras de alvo de
            # toque não entram, então a medição acusaria erro em algo que no
            # celular de verdade já está resolvido.
            pg = b.new_page(viewport={"width": w, "height": h},
                            has_touch=(vname == "mobile"),
                            is_mobile=(vname == "mobile"))
            for rel in pages():
                pg.goto(f"http://127.0.0.1:{port}/{rel}", wait_until="networkidle")
                pg.evaluate("document.querySelectorAll('[data-reveal]').forEach(e=>e.classList.add('is-revealed'))")
                pg.wait_for_timeout(120)
                res = pg.evaluate(CHECK)
                for k, items in res.items():
                    for it in items:
                        buckets[k].append((vname, rel, it))
            pg.close()
        b.close()
    srv.shutdown()

    order = ["overflow", "contrast", "tap", "gaps", "orphan", "misc"]
    names = {"overflow": "Overflow horizontal", "contrast": "Contraste abaixo do WCAG AA",
             "tap": "Alvo de toque < 40px (mobile)", "gaps": "Colunas desbalanceadas (buraco branco)",
             "orphan": "Órfão tipográfico em título", "misc": "font-size inline"}
    total = 0
    for k in order:
        items = buckets.get(k, [])
        total += len(items)
        print(f"\n— {names[k]} ({len(items)}) " + "-" * max(4, 46 - len(names[k])))
        if not items:
            print("   nenhum")
            continue
        seen = set()
        for vname, rel, it in items:
            sig = (k, it.get("sel") or it.get("cls") or it.get("text", ""), it.get("text", "")[:24], vname)
            if sig in seen:
                continue
            seen.add(sig)
            if len(seen) > 40:
                print(f"   … (+{len(items) - 40} ocorrências)")
                break
            print(f"   [{vname}] {rel}: {it}")
    print(f"\nTOTAL: {total}")


if __name__ == "__main__":
    sys.exit(main() or 0)
