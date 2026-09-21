# -*- coding: utf-8 -*-
"""Auditoria do site gerado: links, âncoras, ativos, headings, meta e acessibilidade básica."""
import os
import re
import sys
from html.parser import HTMLParser

_R = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(_R) if os.path.basename(_R) == "src" else _R, "dist")
problems = []
stats = {"pages": 0, "links": 0, "ids": 0}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.headings = [], set(), []
        self.imgs, self.labels, self.inputs = [], set(), []
        self.buttons_controls, self.title = [], ""
        self._in_title = False
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("link", "script", "img") and (a.get("href") or a.get("src")):
            v = a.get("href") or a.get("src")
            if not v.startswith(("http", "data:", "mailto:", "tel:")):
                self.links.append(v)
        if tag in ("h1", "h2", "h3", "h4"):
            self.headings.append(int(tag[1]))
            if tag == "h1":
                self.h1 += 1
        if tag == "img" and "alt" not in a:
            self.imgs.append(a.get("src", "?"))
        if tag == "label" and "for" in a:
            self.labels.add(a["for"])
        if tag in ("input", "select", "textarea"):
            self.inputs.append(a)
        if "aria-controls" in a:
            self.buttons_controls.append(a["aria-controls"])
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d


def audit():
    files = []
    for root, _, names in os.walk(DIST):
        for n in names:
            if n.endswith(".html"):
                files.append(os.path.join(root, n))

    for f in sorted(files):
        rel_f = os.path.relpath(f, DIST)
        stats["pages"] += 1
        raw = open(f, encoding="utf-8").read()
        p = Page()
        p.feed(raw)
        stats["ids"] += len(p.ids)

        # título e descrição
        if len(p.title) > 75:
            problems.append(f"{rel_f}: <title> com {len(p.title)} caracteres (>75)")
        m = re.search(r'<meta name="description" content="([^"]*)"', raw)
        if not m:
            problems.append(f"{rel_f}: sem meta description")
        elif not (60 <= len(m.group(1)) <= 190):
            problems.append(f"{rel_f}: meta description com {len(m.group(1))} caracteres")

        if p.h1 != 1:
            problems.append(f"{rel_f}: {p.h1} elementos h1 (esperado 1)")

        # links internos
        for href in p.links:
            if href.startswith(("http", "mailto:", "tel:", "data:", "javascript:")):
                continue
            stats["links"] += 1
            if href.startswith("#"):
                if href[1:] and href[1:] not in p.ids:
                    problems.append(f"{rel_f}: âncora inexistente {href}")
                continue
            base, _, frag = href.partition("#")
            # Assets versionados por cache_bust (build.py) levam "?v=<hash>"
            # na URL — isso não faz parte do caminho no disco (o navegador
            # também ignora a query string ao resolver o arquivo).
            base = base.split("?", 1)[0]
            target = os.path.normpath(os.path.join(os.path.dirname(f), base))
            if not os.path.exists(target):
                problems.append(f"{rel_f}: link quebrado -> {href}")

        # aria-controls precisa existir
        for c in p.buttons_controls:
            if c not in p.ids:
                problems.append(f"{rel_f}: aria-controls aponta para id inexistente '{c}'")

        # imagens sem alt
        for src in p.imgs:
            problems.append(f"{rel_f}: <img> sem alt -> {src}")

        # campos de formulário com rótulo
        for inp in p.inputs:
            iid = inp.get("id")
            if inp.get("type") in ("radio", "checkbox", "hidden"):
                continue
            if not iid:
                problems.append(f"{rel_f}: campo sem id")
            elif iid not in p.labels:
                problems.append(f"{rel_f}: campo '{iid}' sem <label for>")

        # resíduos de template: chave não interpolada, ou placeholder Python vazando.
        # Ignora <script>/<style>: JSON-LD e JS legitimamente contêm chaves duplas.
        import re as _re
        no_script = _re.sub(r"<script\b.*?</script>", "", raw, flags=_re.S | _re.I)
        no_script = _re.sub(r"<style\b.*?</style>", "", no_script, flags=_re.S | _re.I)
        # Cobre tanto {variavel} quanto {func("arg", x)} vazando no HTML.
        for m in _re.finditer(r"\{[a-zA-Z_][^{}\n]{0,120}\}", no_script):
            problems.append(f"{rel_f}: possível interpolação não resolvida -> {m.group(0)[:70]}")
        for bad in (">None<", ">undefined<"):
            if bad in no_script:
                problems.append(f"{rel_f}: resíduo '{bad}' no HTML")
        if "{{" in no_script or "}}" in no_script:
            problems.append(f"{rel_f}: chave dupla fora de <script>/<style>, possível resíduo")
        if "href=\"#\"" in raw:
            problems.append(f"{rel_f}: link vazio href=\"#\"")

    print(f"Páginas: {stats['pages']} | links internos verificados: {stats['links']}")
    if problems:
        print(f"\n{len(problems)} ocorrências:")
        for p_ in problems:
            print("  -", p_)
        return 1
    print("Nenhuma ocorrência.")
    return 0


if __name__ == "__main__":
    sys.exit(audit())
