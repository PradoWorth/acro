# -*- coding: utf-8 -*-
"""Auditoria profunda: SEO, acessibilidade, consistência estrutural e conteúdo.

Complementa audit.py (links) e design_audit.py (escala visual).
"""
import json
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

_R = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(_R) if os.path.basename(_R) == "src" else _R, "dist")

findings = defaultdict(list)


def note(cat, page, msg):
    findings[cat].append((page, msg))


class Doc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = {}
        self.og = {}
        self.headings = []          # (level, text)
        self.imgs = []              # dict de atributos
        self.links = []             # (href, text, attrs)
        self.buttons = []
        self.landmarks = []
        self.lang = None
        self.schemas = []
        self.canonical = None
        self.text_len = 0
        self.tables = 0
        self.forms = 0
        self.iframes = 0
        self._stack = []
        self._grab = None
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta":
            if a.get("name"):
                self.meta[a["name"]] = a.get("content", "")
            if a.get("property", "").startswith("og:"):
                self.og[a["property"]] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "title":
            self._grab, self._buf = "title", ""
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._grab, self._buf = tag, ""
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self._grab, self._buf = "a", ""
            self._stack.append(a)
        elif tag == "button":
            self._grab, self._buf = "button", ""
            self._stack.append(a)
        elif tag in ("main", "nav", "header", "footer", "aside"):
            self.landmarks.append(tag)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._grab, self._buf = "schema", ""
        elif tag == "table":
            self.tables += 1
        elif tag == "form":
            self.forms += 1
        elif tag == "iframe":
            self.iframes += 1

    def handle_endtag(self, tag):
        if self._grab == "title" and tag == "title":
            self.title = self._buf.strip()
        elif self._grab in ("h1", "h2", "h3", "h4", "h5", "h6") and tag == self._grab:
            self.headings.append((int(tag[1]), self._buf.strip()))
        elif self._grab == "a" and tag == "a":
            a = self._stack.pop() if self._stack else {}
            self.links.append((a.get("href", ""), self._buf.strip(), a))
        elif self._grab == "button" and tag == "button":
            a = self._stack.pop() if self._stack else {}
            self.buttons.append((self._buf.strip(), a))
        elif self._grab == "schema" and tag == "script":
            self.schemas.append(self._buf.strip())
        else:
            return
        self._grab, self._buf = None, ""

    def handle_data(self, d):
        if self._grab:
            self._buf += d
        self.text_len += len(d.strip())


def load():
    pages = {}
    for root, _, names in os.walk(DIST):
        for n in sorted(names):
            if not n.endswith(".html"):
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, DIST)
            raw = open(p, encoding="utf-8").read()
            d = Doc()
            d.feed(raw)
            pages[rel] = (d, raw)
    return pages


def main():
    pages = load()
    titles, descs = defaultdict(list), defaultdict(list)

    for rel, (d, raw) in sorted(pages.items()):
        # ---------------------------------------------------------- SEO
        if not d.title:
            note("SEO", rel, "sem <title>")
        else:
            titles[d.title].append(rel)
            if len(d.title) > 62:
                note("SEO", rel, f"title com {len(d.title)} caracteres (>62 corta no Google): {d.title!r}")
            if len(d.title) < 20:
                note("SEO", rel, f"title curto demais ({len(d.title)}): {d.title!r}")

        desc = d.meta.get("description", "")
        if not desc:
            note("SEO", rel, "sem meta description")
        else:
            descs[desc].append(rel)
            if len(desc) > 165:
                note("SEO", rel, f"meta description com {len(desc)} caracteres (>165 corta)")
            if len(desc) < 70:
                note("SEO", rel, f"meta description curta ({len(desc)})")

        # Página noindex (hoje só 404.html) não tem canonical de propósito:
        # apontar o canonical de uma página de erro para uma URL que não
        # existe de verdade, e que não está no sitemap, seria pior do que
        # não ter canonical nenhum (ver build.head_common). Cobrar canonical
        # aqui seria pedir pra desfazer uma correção de SEO já aplicada.
        if not d.canonical and "noindex" not in d.meta.get("robots", ""):
            note("SEO", rel, "sem link canonical")
        for k in ("og:title", "og:description", "og:image", "og:url", "og:type"):
            if k not in d.og:
                note("SEO", rel, f"sem {k}")
        if not d.lang:
            note("SEO", rel, "html sem atributo lang")
        if "twitter:card" not in d.meta:
            note("SEO", rel, "sem twitter:card")

        # -------------------------------------------------- estrutura/headings
        h1s = [t for lvl, t in d.headings if lvl == 1]
        if len(h1s) == 0:
            note("Estrutura", rel, "nenhum h1")
        elif len(h1s) > 1:
            note("Estrutura", rel, f"{len(h1s)} h1: {h1s}")

        prev = 0
        for lvl, txt in d.headings:
            if prev and lvl > prev + 1:
                note("Estrutura", rel, f"salto de h{prev} para h{lvl}: {txt[:48]!r}")
            prev = lvl

        for lvl, txt in d.headings:
            if not txt.strip():
                note("Estrutura", rel, f"h{lvl} vazio")

        # landmarks
        for lm in ("main", "header", "footer", "nav"):
            if lm not in d.landmarks:
                note("Estrutura", rel, f"sem landmark <{lm}>")

        # -------------------------------------------------- acessibilidade
        for img in d.imgs:
            if "alt" not in img:
                note("A11y", rel, f"img sem alt: {img.get('src','?')}")
            elif img.get("alt", "").strip() and len(img["alt"]) < 4 and img["alt"] != "":
                note("A11y", rel, f"alt suspeito {img['alt']!r}")
            # fetchpriority="high" é o sinal explícito de que a ausência de
            # loading=lazy é intencional (imagem crítica acima da dobra: hero
            # da home, topo das páginas internas) — carregar eager aí é o
            # comportamento certo, não uma omissão a apontar aqui.
            if "loading" not in img and "fetchpriority" not in img:
                note("Perf", rel, f"img sem loading=lazy: {img.get('src','?')[:60]}")
            if not (img.get("width") and img.get("height")):
                note("Perf", rel, f"img sem width/height (causa layout shift): {img.get('src','?')[:60]}")

        for href, text, a in d.links:
            label = text or a.get("aria-label", "") or a.get("title", "")
            if not label.strip():
                note("A11y", rel, f"link sem texto acessível: href={href[:50]!r}")
            if text.strip().lower() in ("clique aqui", "saiba mais", "leia mais", "aqui", "link"):
                note("A11y", rel, f"texto de link genérico: {text!r}")
            if a.get("target") == "_blank" and "noopener" not in a.get("rel", ""):
                note("A11y", rel, f"target=_blank sem rel=noopener: {href[:50]}")

        for text, a in d.buttons:
            if not (text.strip() or a.get("aria-label")):
                note("A11y", rel, "button sem rótulo acessível")

        # -------------------------------------------------- schema
        for s in d.schemas:
            try:
                json.loads(s)
            except Exception as e:
                note("Schema", rel, f"JSON-LD inválido: {e}")

        # -------------------------------------------------- conteúdo
        # Só o texto que o visitante enxerga: sem <script>/<style> e sem
        # tags. Regras de tipografia (espaço duplo, travessão) rodam aqui —
        # em JS embutido "a  +  b" é indentação, não erro de revisão.
        body = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
        body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
        text_only = re.sub(r"<[^>]+>", " ", body)

        for pat, desc_ in [
            (r"[Ll]orem ipsum", "lorem ipsum"),
            (r"\bTODO\b|\bFIXME\b", "marcador TODO/FIXME"),
            (r"\bXXX\b", "marcador XXX"),
            (r"\[inserir|\[preencher|\[definir", "placeholder entre colchetes"),
            (r"Ã©|Ã¡|Ã§|Ã£|â€", "encoding quebrado"),
        ]:
            for m in re.finditer(pat, raw):
                ctx = raw[max(0, m.start() - 40):m.start() + 40].replace("\n", " ")
                note("Conteúdo", rel, f"{desc_}: …{ctx}…")
                break

        # Espaço duplo: regra de redação, então vale só DENTRO de um nó de
        # texto e no meio da linha. Duas ressalvas que davam falso positivo
        # antes: (a) juntar o texto de tags vizinhas cria espaços que não
        # existem na página; (b) o HTML sai indentado, então quebra de linha
        # + recuo não é espaço duplo de frase. Por isso a busca é nó a nó e
        # exige um caractere visível imediatamente antes dos espaços.
        for trecho in re.split(r"<[^>]+>", body):
            m = re.search(r"\S  +[a-záéíóúâêôãõç]", trecho)
            if m:
                ctx = trecho[max(0, m.start() - 40):m.start() + 40].replace("\n", " ")
                note("Conteúdo", rel, f"espaço duplo no meio da frase: …{ctx}…")
                break

        # travessão / em dash — o cliente pediu para não usar
        for ch, nm in [("—", "travessão (em dash)"), ("–", "meia-risca (en dash)")]:
            c = text_only.count(ch)
            if c:
                note("Conteúdo", rel, f"{c}x {nm} no texto visível")

    # ----------------------------------------------------- duplicidade global
    for t, ps in titles.items():
        if len(ps) > 1:
            note("SEO", "GLOBAL", f"title duplicado em {ps}: {t!r}")
    for dsc, ps in descs.items():
        if len(ps) > 1:
            note("SEO", "GLOBAL", f"meta description duplicada em {ps}")

    # ----------------------------------------------------- relatório
    total = sum(len(v) for v in findings.values())
    for cat in sorted(findings):
        items = findings[cat]
        print(f"\n— {cat} ({len(items)}) " + "-" * (56 - len(cat)))
        shown = defaultdict(list)
        for page, msg in items:
            shown[msg.split(":")[0]].append((page, msg))
        for group, entries in shown.items():
            if len(entries) > 6:
                print(f"   [{len(entries)}x] {group}")
                for page, msg in entries[:3]:
                    print(f"      {page}: {msg[:110]}")
                print(f"      … e mais {len(entries) - 3}")
            else:
                for page, msg in entries:
                    print(f"   {page}: {msg[:130]}")
    print(f"\nTOTAL: {total} apontamentos em {len(load())} páginas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
