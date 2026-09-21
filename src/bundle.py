# -*- coding: utf-8 -*-
"""
Empacota o site inteiro em um único HTML navegável.

Motivação: em pré-visualizações que servem um arquivo por vez (o preview do
Claude, por exemplo), links relativos entre documentos não funcionam. Este
empacotador extrai o <main> de cada uma das 28 páginas, embute CSS, JS, fontes
e arte, e troca a navegação por um roteador de hash. O resultado é um arquivo
só, sem nenhuma requisição externa, que navega igual ao site publicado.

Não substitui dist/: o site de produção continua sendo multipáginas real, com
uma rota HTTP por página, que é o que interessa para SEO.

    python3 bundle.py        -> ../acropole-navegavel.html
"""
import base64
import os
import re
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT) if os.path.basename(ROOT) == "src" else ROOT
DIST = os.path.join(BASE, "dist")
OUT = os.path.join(BASE, "acropole-navegavel.html")

# Fontes realmente usadas (subset latin). O latin-ext fica de fora do pacote
# para não dobrar o peso: o português cabe inteiro no subset latin.
#
# Manrope 700 estava faltando aqui: h1/h2/h3 (site.css) pedem var(--display),
# que é Manrope, mas como este arquivo nunca embutia a fonte, o navegável
# caía sempre no fallback do sistema — só nesta versão de arquivo único; o
# dist/ com fonts.css de verdade sempre esteve correto. É o que o cliente
# viu como "duas fontes diferentes no mesmo HTML".
# Desde a auditoria de performance (README, item 119) são 2 arquivos, não
# 5: a Inter virou variável (um arquivo cobre os pesos 400 a 700) e as duas
# foram reduzidas aos caracteres do site. O pacote navegável, que embute
# tudo em base64, encolheu junto — e o peso da fonte pesa em dobro aqui,
# porque base64 infla 33%.
FONTS = [
    ("Inter", "100 900", "normal", "inter-var.woff2"),
    ("Manrope", "700", "normal", "manrope-700.woff2"),
]


def route_of(rel_path):
    """sobre.html -> /sobre ; index.html -> / ; solucoes/x.html -> /solucoes/x"""
    if rel_path == "index.html":
        return "/"
    return "/" + rel_path[:-5]


def collect_pages():
    pages = {}
    for root, _, names in os.walk(DIST):
        for n in sorted(names):
            if not n.endswith(".html"):
                continue
            full = os.path.join(root, n)
            rel = os.path.relpath(full, DIST).replace(os.sep, "/")
            raw = open(full, encoding="utf-8").read()
            main = re.search(r'<main id="conteudo">(.*?)</main>', raw, re.S)
            title = re.search(r"<title>(.*?)</title>", raw, re.S)
            desc = re.search(r'<meta name="description" content="([^"]*)"', raw)
            if not main:
                continue
            pages[route_of(rel)] = {
                "html": main.group(1),
                "title": (title.group(1).strip() if title else "Acrópole Capital"),
                "desc": (desc.group(1) if desc else ""),
                "src": rel,
            }
    return pages


def rewrite_links(html, from_rel):
    """
    Converte href de arquivo em href de rota (#/...). Preserva externos e âncoras.

    Um href pode combinar arquivo E âncora na mesma string (ex.:
    "programas.html#bndes", usado pelos chips de programa público) — o "#"
    aqui não é uma âncora de página pura, é um fragmento dentro de outra
    página. Por isso o corte em "#" acontece ANTES do teste ".html": sem
    isso, "programas.html#bndes" não termina em ".html" (termina em
    "#bndes") e o link saía daqui sem conversão nenhuma, como um caminho de
    arquivo relativo quebrado dentro do pacote de arquivo único (não existe
    "programas.html" ao lado do navegável — só existe a rota /programas
    dentro do roteador). O fragmento é preservado como "?a=<fragmento>" no
    hash de rota (ex.: "#/programas?a=bndes"); o ROUTER_JS decodifica esse
    "?a=" e rola até o elemento certo depois de renderizar a rota.
    """
    from_dir = os.path.dirname(from_rel)

    def sub(m):
        attr, quote_ch, href = m.group(1), m.group(2), m.group(3)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            return m.group(0)
        file_part, _, frag = href.partition("#")
        if not file_part.endswith(".html"):
            return m.group(0)
        target = os.path.normpath(os.path.join(from_dir, file_part)).replace(os.sep, "/")
        route = route_of(target)
        suffix = f"?a={frag}" if frag else ""
        return f'{attr}={quote_ch}#{route}{suffix}{quote_ch}'

    return re.sub(r'(href)=(["\'])([^"\']+)\2', sub, html)


PAGE_SCRIPT_RE = re.compile(r'<script src="([^"]*assets/js/([^"/]+))"[^>]*></script>')


def inline_page_scripts(html):
    """
    Traz para dentro do HTML os <script src="assets/js/…"> que pertencem ao
    CONTEÚDO de uma página (hoje só o globo da home, ver emit_globe_js em
    build.py).

    O pacote navegável não faz nenhuma requisição: um <script src> dentro do
    conteúdo de uma rota simplesmente não carregaria. E o roteador daqui já
    reexecuta todo <script> inline ao renderizar a rota (ver ROUTER_JS), que
    é exatamente o que o globo precisa para voltar a desenhar quando a
    pessoa sai da home e volta.

    Não vale para site.js e config.js: esses são do documento
    inteiro, não de uma rota, e já entram uma vez no fim do arquivo.
    """
    PAGE_LEVEL = {"globe.js"}

    def sub(m):
        # build.py agora versiona esses scripts com "?v=<hash>" (cache
        # busting, ver cache_bust em build.py) — o nome do arquivo em si,
        # sem a query string, é o que importa aqui.
        name = m.group(2).split("?", 1)[0]
        if name not in PAGE_LEVEL:
            return m.group(0)
        p = os.path.join(DIST, "assets", "js", name)
        if not os.path.exists(p):
            return m.group(0)
        return "<script>" + open(p, encoding="utf-8").read() + "</script>"

    return PAGE_SCRIPT_RE.sub(sub, html)


def data_uri_svg(path):
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"\s+", " ", svg).strip()
    b64 = base64.b64encode(svg.encode()).decode()
    return "data:image/svg+xml;base64," + b64


IMG_MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
            ".webp": "image/webp", ".avif": "image/avif", ".gif": "image/gif",
            ".svg": "image/svg+xml"}


def data_uri_raster(path):
    ext = os.path.splitext(path)[1].lower()
    mime = IMG_MIME.get(ext, "application/octet-stream")
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return f"data:{mime};base64,{b64}"


# Placeholder de 1x1 transparente: o src real é aplicado por JS a partir do mapa.
BLANK = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


PICTURE_RE = re.compile(
    r'<picture>(?P<sources>(?:<source[^>]*>)*)<img(?P<attrs>[^>]*)>\s*</picture>',
    re.S,
)
SOURCE_RE = re.compile(r'<source[^>]*type="([^"]+)"[^>]*srcset="([^"]+)"[^>]*>')


def collapse_pictures(html):
    """
    No site publicado (dist/), cada foto tem <picture> com variantes AVIF e
    WebP na frente do .jpg: o navegador baixa só a que sabe decodificar, uma
    via HTTP normal. Aqui não existe esse benefício — o arquivo único não faz
    requisição nenhuma, cada byte referenciado entra embutido de uma vez só —
    então manter as três variantes só faria o pacote inchar (as três, juntas,
    em vez de uma). Por isso cada <picture> vira um <img> só, com a variante
    mais leve disponível (AVIF, senão WebP, senão o .jpg original).
    """
    def sub(m):
        sources = dict((mime, url) for mime, url in SOURCE_RE.findall(m.group("sources")))
        best = sources.get("image/avif") or sources.get("image/webp")
        attrs = m.group("attrs")
        if best:
            attrs = re.sub(r'\ssrc="[^"]*"', f' src="{best}"', attrs, count=1)
        return f"<img{attrs}>"
    return PICTURE_RE.sub(sub, html)


def inline_assets(html, art_map):
    """
    Troca o src (de <img>) ou o srcset (de <source>, usado no <picture> das
    fotos com variante AVIF/WebP) da arte (assets/art/…) e das fotos reais
    (assets/img/…, incluindo subpastas como assets/img/conteudos/…) por um
    id curto. Cada arquivo entra uma única vez em __ACR_ART__; sem isso, uma
    mesma foto (ex.: o herói, ou uma foto de artigo repetida no hub, na home
    e nos relacionados) seria embutida de novo a cada uso e o pacote inflaria.
    """
    def sub(m):
        attr, quote_ch, src = m.group(1), m.group(2), m.group(3)
        # srcset responsivo ("foto-800.avif 800w, foto-1100.avif 1100w,
        # foto.avif 1400w", ver raster_img em build.py): aqui não existe
        # negociação de largura — o arquivo único não faz requisição, cada
        # imagem entra embutida em base64 e embutir as 3 variantes da mesma
        # foto só inflaria o pacote. Fica a de 1100px, que é a que o celular
        # (a tela mais comum) escolheria no site publicado.
        if "," in src:
            cands = [c.strip().split(" ")[0] for c in src.split(",") if c.strip()]
            escolhida = next((c for c in cands if "-1100." in c), cands[0])
            src = escolhida
        is_art = "assets/art/" in src
        subdir = "art" if is_art else "img"
        # Preserva o caminho relativo inteiro depois de assets/art/ ou
        # assets/img/ (não só o nome do arquivo), para achar fotos dentro de
        # subpastas como assets/img/conteudos/ e assets/img/solucoes/, e para
        # não colidir a chave quando duas subpastas têm um arquivo de mesmo nome.
        rel = re.search(r"assets/(?:art|img)/(.+)$", src).group(1)
        p = os.path.join(DIST, "assets", subdir, *rel.split("/"))
        if not os.path.exists(p):
            return m.group(0)
        key = subdir + ":" + rel
        if key not in art_map:
            art_map[key] = data_uri_svg(p) if is_art else data_uri_raster(p)
        return f'data-art={quote_ch}{key}{quote_ch} {attr}={quote_ch}{BLANK}{quote_ch}'
    return re.sub(r'(src|srcset)=(["\'])([^"\']*assets/(?:art|img)/[^"\']+)\2', sub, html)


def build_font_css():
    css = []
    for family, weight, style, fname in FONTS:
        p = os.path.join(DIST, "assets", "fonts", fname)
        if not os.path.exists(p):
            continue
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        css.append(
            f'@font-face{{font-family:"{family}";font-style:{style};font-weight:{weight};'
            f'font-display:swap;src:url(data:font/woff2;base64,{b64}) format("woff2");}}'
        )
    return "\n".join(css)


ROUTER_JS = r"""
(function () {
  'use strict';
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  var PAGES = window.__ACR_PAGES__;
  var ART = window.__ACR_ART__ || {};
  var main = document.getElementById('conteudo');
  var titleEl = document.querySelector('title');

  function paintArt(scope) {
    (scope || document).querySelectorAll('img[data-art]').forEach(function (img) {
      var uri = ART[img.getAttribute('data-art')];
      if (uri && img.getAttribute('src') !== uri) img.src = uri;
    });
    // <source> do <picture> (variantes AVIF/WebP): mesmo mapa, mas o
    // navegador escolhe pelo srcset, não pelo src.
    (scope || document).querySelectorAll('source[data-art]').forEach(function (src) {
      var uri = ART[src.getAttribute('data-art')];
      if (uri && src.getAttribute('srcset') !== uri) src.srcset = uri;
    });
  }

  function normalize(hash) {
    var r = (hash || '').replace(/^#/, '');
    if (!r || r === '/') return '/';
    r = r.split('?')[0];
    return r.replace(/\/+$/, '') || '/';
  }

  // Extrai o "?a=<fragmento>" de um hash de rota (ex.: "#/programas?a=bndes"
  // -> "bndes"). É como rewrite_links(), no lado Python, preserva o
  // fragmento de um link "arquivo.html#âncora" ao convertê-lo para rota —
  // sem isso o roteador saberia PARA QUAL rota ir, mas não PARA QUAL
  // elemento dentro dela rolar.
  function anchorOf(hash) {
    var r = (hash || '').replace(/^#/, '');
    var i = r.indexOf('?a=');
    if (i === -1) return null;
    var rest = r.slice(i + 3).split('&')[0];
    try { return decodeURIComponent(rest); } catch (e) { return rest; }
  }

  function markNav(route) {
    document.querySelectorAll('.nav__link, .drawer__link, .megapanel__link, .foot a').forEach(function (a) {
      a.removeAttribute('aria-current');
    });
    document.querySelectorAll('.nav__item').forEach(function (i) { i.classList.remove('is-current'); });
    var sel = '[href="#' + route + '"]';
    document.querySelectorAll('.nav__link' + sel + ', .drawer__link' + sel).forEach(function (a) {
      a.setAttribute('aria-current', 'page');
    });
    // "Soluções" fica marcado em qualquer rota filha
    if (route.indexOf('/solucoes') === 0) {
      var mega = document.querySelector('.nav__item[data-mega]');
      if (mega) mega.classList.add('is-current');
    }
  }

  function render(route, anchor) {
    var page = PAGES[route];
    if (!page) { page = PAGES['/404'] || PAGES['/']; route = PAGES['/404'] ? '/404' : '/'; }

    main.innerHTML = page.html;
    // innerHTML não executa <script>: recria cada um para que rode.
    main.querySelectorAll('script').forEach(function (old) {
      var sc = document.createElement('script');
      if (old.src) {
        sc.src = old.src;
      } else {
        // Envolve em uma IIFE: uma página com script próprio (diagnóstico
        // rápido, simulador de programas) pode ser visitada, deixada e
        // revisitada várias vezes na mesma sessão do navegável — cada
        // visita recria e reexecuta o <script> do zero. Um `let`/`const`
        // de nível "solto" (sem função em volta) declara no escopo léxico
        // global do documento, que persiste entre execuções; reexecutar o
        // mesmo script uma segunda vez então falhava com "Identifier ...
        // has already been declared" e a página ficava sem a interação
        // (formulário do diagnóstico, simulador). A IIFE dá a cada
        // execução seu próprio escopo de função, descartado ao terminar,
        // então revisitar a mesma página quantas vezes for sempre funciona.
        sc.textContent = '(function(){' + old.textContent + '})();';
      }
      old.parentNode.replaceChild(sc, old);
    });
    titleEl.textContent = page.title;
    var d = document.querySelector('meta[name="description"]');
    if (d) d.setAttribute('content', page.desc);

    // O hero só existe na home: o cabeçalho muda de comportamento conforme isso.
    var mast = document.querySelector('.masthead');
    var over = !!main.querySelector('.hero, .pagehead');
    mast.classList.toggle('masthead--over', over);
    mast.classList.toggle('masthead--solid', !over);

    markNav(route);
    paintArt(main);
    if (window.Acropole && window.Acropole.bindPage) window.Acropole.bindPage(main);
    // instant, não smooth: o <html> tem scroll-behavior:smooth (para os
    // cliques em âncora), e sem forçar instant aqui a troca de rota "subia"
    // visualmente de baixo pra cima em vez de já abrir no topo.
    // Quando a rota carrega um "?a=<âncora>" (ver anchorOf/rewrite_links),
    // rola até o elemento certo dentro da página recém-renderizada em vez
    // de sempre voltar ao topo — é o caso dos chips de programa público
    // (BNDES, PEAC FGI, Pronampe, Procred 360) apontando para uma seção
    // específica de /programas.
    var target = anchor ? main.querySelector('#' + CSS.escape(anchor)) : null;
    if (target) {
      target.scrollIntoView({ behavior: 'instant', block: 'start' });
    } else {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    }
    document.dispatchEvent(new CustomEvent('acr:navigated', { detail: { route: route, anchor: anchor || null } }));
  }

  // Mesmo crossfade do site real (ver site.css, "Transição entre páginas")
  // também para a troca de ROTA VIRTUAL do pacote navegável — aqui não é a
  // navegação nativa do navegador (é innerHTML), então quem decide iniciar
  // a transição é este JS, não o `@view-transition` do CSS sozinho.
  // startViewTransition só existe em navegadores com suporte; nos demais
  // (e com "menos movimento" pedido no sistema) cai direto em render(),
  // sem transição nenhuma — nunca quebra, só não anima.
  function renderRoute(route, anchor) {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduced && document.startViewTransition) {
      document.startViewTransition(function () { render(route, anchor); });
    } else {
      render(route, anchor);
    }
  }

  window.addEventListener('hashchange', function () {
    // Só re-renderiza para uma troca de ROTA (#/algo ou vazio/#). Uma âncora
    // dentro da própria página (#s3, no sumário de Avisos legais; #conteudo,
    // no link de acessibilidade "Ir para o conteúdo") também dispara
    // hashchange, e sem esta guarda o roteador tratava esse hash como uma
    // rota desconhecida e trocava a página inteira pela 404 (ou pela home)
    // em vez de deixar o navegador rolar até o elemento — parecia, na
    // prática, que o link "não levava a lugar nenhum".
    var h = location.hash;
    if (h && h.charAt(1) !== '/') return;
    renderRoute(normalize(h), anchorOf(h));
  });

  // Fecha a gaveta ao navegar no mobile
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#/"]');
    if (!a) return;
    var drawer = document.querySelector('.drawer');
    if (drawer && drawer.getAttribute('data-open') === 'true') {
      var burger = document.querySelector('.burger');
      drawer.setAttribute('data-open', 'false');
      drawer.setAttribute('aria-hidden', 'true');
      if (burger) burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-locked');
    }
    var hrefRaw = a.getAttribute('href');
    // hashchange só dispara quando o hash MUDA. Um link para a mesma rota
    // com a mesma âncora (ou sem âncora nenhuma) não muda o hash, então sem
    // este atalho o clique não fazia nada visível — por isso força a
    // rolagem manualmente. Quando a âncora é diferente (dois chips de
    // programa diferentes na mesma rota /programas, por exemplo), o hash
    // muda de verdade e o hashchange acima cuida da rolagem sozinho.
    if (normalize(hrefRaw) === normalize(location.hash) && anchorOf(hrefRaw) === anchorOf(location.hash)) {
      e.preventDefault();
      var anchor = anchorOf(hrefRaw);
      var target = anchor ? main.querySelector('#' + CSS.escape(anchor)) : null;
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  });

  paintArt(document);
  render(normalize(location.hash), anchorOf(location.hash));
})();
"""

def main():
    if not os.path.isdir(DIST):
        sys.exit("dist/ não encontrado. Rode build.py antes.")

    pages = collect_pages()
    index_raw = open(os.path.join(DIST, "index.html"), encoding="utf-8").read()

    # Cabeçalho, gaveta e rodapé saem da home e valem para todas as rotas.
    # A classe do header carrega modificador (masthead--over), por isso o
    # seletor usa apenas o prefixo da tag.
    def grab(pattern, label):
        m = re.search(pattern, index_raw, re.S)
        if not m:
            sys.exit(f"não consegui extrair {label} de index.html")
        return m.group(1)

    header = grab(r'(<header class="masthead[^"]*">.*?</header>)', "o cabeçalho")
    drawer_html = grab(r'(<div class="drawer" id="drawer".*?)\n<main', "a gaveta")
    footer = grab(r'(<footer class="foot">.*?</footer>)', "o rodapé")
    rail = re.search(r'(<a class="rail".*?</a>)', index_raw, re.S)
    rail_html = rail.group(1) if rail else ""
    lead_modal = grab(r'(<div class="leadmodal" id="lead-modal".*?)\n<script', "o popup de captação")
    # O <symbol id="brand-mark"> definido uma vez por página em dist/ — sem
    # ele aqui, os <use href="#brand-mark"> do cabeçalho/gaveta/rodapé não
    # apontam para nada e a logo fica invisível no pacote de arquivo único.
    logo_sprite = grab(r'(<svg width="0" height="0"[^>]*>.*?</svg>)', "o sprite da logo")
    # O script síncrono que decide, antes de qualquer conteúdo, se a página
    # esconde os blocos [data-reveal] para animar a entrada no scroll — sem
    # ele aqui, o pacote de arquivo único carrega o CSS de revelação mas
    # nunca ganha a classe que a ativa.
    reveal_js = grab(r'<meta name="viewport"[^>]*>\s*<script>(.*?)</script>', "o detector de revelação")

    art_map = {}
    chrome = []
    for part in (header, drawer_html, footer, rail_html, lead_modal, logo_sprite):
        part = rewrite_links(part, "index.html")
        part = collapse_pictures(part)
        part = inline_assets(part, art_map)
        chrome.append(part)
    header, drawer_html, footer, rail_html, lead_modal, logo_sprite = chrome

    # Conteúdo de cada rota
    payload = {}
    for route, p in pages.items():
        html = rewrite_links(p["html"], p["src"])
        html = collapse_pictures(html)
        html = inline_assets(html, art_map)
        html = inline_page_scripts(html)
        payload[route] = {"html": html, "title": p["title"], "desc": p["desc"]}

    import json
    # "</" precisa ser escapado: uma página traz <script> no corpo, e o
    # </script> literal encerraria o bloco que carrega este JSON.
    pages_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    art_json = json.dumps(art_map, ensure_ascii=False).replace("</", "<\\/")

    css = open(os.path.join(DIST, "assets", "css", "site.css"), encoding="utf-8").read()
    js = open(os.path.join(DIST, "assets", "js", "site.js"), encoding="utf-8").read()
    fonts_css = build_font_css()

    doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>{reveal_js}</script>
<title>Acrópole Capital</title>
<meta name="description" content="">
<style>{fonts_css}</style>
<style>{css}</style>
</head>
<body>
{logo_sprite}
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
{header}
{drawer_html}
<main id="conteudo"></main>
{footer}
{rail_html}
{lead_modal}
<script>window.ACROPOLE_CONFIG = {{ endpoint: "", analytics: {{ provider: "", id: "" }} }};</script>
<script>window.__ACR_ART__ = {art_json};</script>
<script>window.__ACR_PAGES__ = {pages_json};</script>
<script>{js}</script>
<script>{ROUTER_JS}</script>
</body>
</html>"""

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)

    kb = os.path.getsize(OUT) / 1024
    print(f"{len(payload)} rotas empacotadas em {OUT} ({kb:.0f} KB)")
    return OUT


if __name__ == "__main__":
    main()
