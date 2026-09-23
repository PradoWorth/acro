# -*- coding: utf-8 -*-
"""
Gerador do site institucional da Acrópole Capital.

Cada página do menu é um documento HTML real, com rota própria.
Não há navegação por âncora fingindo ser página.

    python3 build.py            -> gera ./dist
"""
import base64
import datetime
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

try:
    import rjsmin
    import rcssmin
    HAVE_MINIFIERS = True
except ImportError:
    HAVE_MINIFIERS = False

# terser é opcional (ver minify_assets): sem ele, o JS ainda sai minificado
# via rjsmin (espaço/comentário fora), só sem *mangling* de identificador.
TERSER_BIN = shutil.which("terser")

# csso é opcional (ver minify_assets): passo extra sobre o que o rcssmin já
# faz — rcssmin só tira espaço/comentário; csso também reestrutura regras
# (funde seletores duplicados, encurta notação de cor, remove unidade em
# zero) com segurança para produção, ganho de mais uns 3% sobre o que já
# sai minificado. Sem csso instalado (npm install -g csso-cli), o CSS
# segue só com o rcssmin, exatamente como antes.
CSSO_BIN = shutil.which("csso")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content.site import (SITE, SOLUTIONS, NAV, PUBLIC_PROGRAMS,
                          LEGAL_LINE, PENDENTE, IMAGES, VIDEOS, CARGOS, PORTES, FATURAMENTOS)
from content import art

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(ROOT) if os.path.basename(ROOT) == "src" else ROOT, "dist")

PAGES = []          # preenchido pelos módulos de conteúdo


# ------------------------------------------------------------------ utilidades
def rel(from_path, to_path):
    """Caminho relativo entre dois documentos do site."""
    depth = from_path.count("/")
    if to_path.startswith(("http", "mailto:", "tel:", "#")):
        return to_path
    return ("../" * depth) + to_path


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def slugify(s):
    s = s.lower()
    for a, b in (("á", "a"), ("â", "a"), ("ã", "a"), ("à", "a"), ("é", "e"), ("ê", "e"),
                 ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"), ("ú", "u"), ("ç", "c")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clean_url(path):
    """URL pública: sobre.html -> /sobre ; index.html -> /"""
    if path == "index.html":
        return "/"
    return "/" + path[:-5]


# ------------------------------------------------------------------ componentes
ART_FILES = {}


def emit_art(dist):
    """
    A arte vive em arquivos .svg, não embutida no HTML.
    O navegador baixa cada peça uma única vez e reaproveita em todas as páginas,
    o que mantém os documentos leves e o first load rápido.
    """
    out = os.path.join(dist, "assets", "art")
    os.makedirs(out, exist_ok=True)
    # Os diagramas de solução (flux, elevation, chassis...) não entram aqui:
    # eles vão inline no HTML de cada página (ver inline_diagram), porque
    # cada um carrega sua própria animação de entrada — algo que um
    # <img src="…svg"> não permite fazer com CSS/SMIL.
    pieces = {"hero": art.hero()}
    for i in range(3):
        pieces[f"pagehead-{i}"] = art.pagehead(i)
    for name, svg in pieces.items():
        # Colapsa o espaço em branco de formatação entre tags (a mesma
        # limpeza que bundle.py já faz ao embutir esta arte no arquivo
        # único) — só a indentação do gerador some, nenhum conteúdo visível.
        svg = re.sub(r">\s+<", "><", svg.strip())
        with open(os.path.join(out, name + ".svg"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>' + svg)
        ART_FILES[name] = f"assets/art/{name}.svg"
    return pieces


# Proporção intrínseca de cada arte, igual ao viewBox gerado em content/art.py.
# Vai como width/height no <img> para que o navegador já reserve a caixa certa
# antes de baixar o SVG: sem isso a página encolhe e reflui quando a arte
# chega, e esse pulo conta como layout shift.
ART_DIMS = {"hero": (1600, 1000), "pagehead-0": (1600, 520),
            "pagehead-1": (1600, 520), "pagehead-2": (1600, 520)}


def art_img(path, name, alt="", cls="", eager=False):
    src = rel(path, f"assets/art/{name}.svg")
    c = f' class="{cls}"' if cls else ""
    hidden = ' aria-hidden="true"' if not alt else ""
    loading = ' fetchpriority="high"' if eager else ' loading="lazy"'
    w, h = ART_DIMS.get(name, (0, 0))
    dims = f' width="{w}" height="{h}"' if w else ""
    return f'<img{c} src="{src}" alt="{esc(alt)}"{loading} decoding="async"{dims}{hidden}>'


def _sibling(rel_src, new_ext):
    """Caminho, em static/, de uma variante da foto (ex.: .jpg -> .avif)."""
    return os.path.join(ROOT, "static", *os.path.splitext(rel_src)[0].split("/")) + new_ext


_DIM_CACHE = {}


def _img_dims(rel_src):
    """Dimensões reais do arquivo, lidas do cabeçalho da imagem no build.

    Vão como width/height no <img> para o navegador reservar a caixa antes de
    a foto chegar. Lê do arquivo em vez de manter uma tabela à mão porque uma
    tabela desatualiza silenciosamente na primeira troca de foto.
    """
    if rel_src in _DIM_CACHE:
        return _DIM_CACHE[rel_src]
    path = os.path.join(ROOT, "static", *rel_src.split("/"))
    dims = None
    try:
        with open(path, "rb") as f:
            head = f.read(32)
        if head[:2] == b"\xff\xd8":                      # JPEG
            with open(path, "rb") as f:
                f.read(2)
                while True:
                    b = f.read(1)
                    if not b:
                        break
                    if b != b"\xff":
                        continue
                    marker = f.read(1)
                    while marker == b"\xff":
                        marker = f.read(1)
                    if marker[0] in (0xD8, 0xD9) or 0xD0 <= marker[0] <= 0xD7:
                        continue
                    seg = f.read(2)
                    length = int.from_bytes(seg, "big")
                    if 0xC0 <= marker[0] <= 0xCF and marker[0] not in (0xC4, 0xC8, 0xCC):
                        data = f.read(5)
                        dims = (int.from_bytes(data[3:5], "big"),
                                int.from_bytes(data[1:3], "big"))
                        break
                    f.seek(length - 2, 1)
        elif head[:8] == b"\x89PNG\r\n\x1a\n":            # PNG
            dims = (int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big"))
    except OSError:
        dims = None
    _DIM_CACHE[rel_src] = dims
    return dims


IMG_WIDTHS = (800, 1100)   # variantes geradas por gerar_imagens.py


def raster_img(path, rel_src, alt="", cls="", eager=False, sizes="100vw"):
    """
    <img> de uma foto real, ou <picture> com variantes AVIF/WebP na frente
    quando elas existem ao lado do .jpg em static/ — o navegador escolhe a
    mais leve que souber decodificar, com o .jpg de sempre como último
    recurso. Sem variantes geradas para uma foto, cai para o <img> simples,
    então nada quebra para uma foto nova que ainda não passou pela conversão.

    `sizes` descreve a largura em que a foto aparece, para o navegador
    escolher entre a variante de 800px e a cheia (ver gerar_imagens.py):
    numa tela de celular, a de 800px pesa menos da metade e é
    indistinguível na prática. Quando a variante pequena não existe, o
    srcset sai com uma entrada só e o `sizes` não muda nada.
    """
    c = f' class="{cls}"' if cls else ""
    hidden = ' aria-hidden="true"' if not alt else ""
    # Três modos, e a diferença entre os dois primeiros importa para o LCP:
    #   eager="auto"  -> carrega junto com a página, mas sem prioridade
    #                    especial. É o certo para a FOTO DECORATIVA do topo
    #                    de página: com fetchpriority="high" ela disputava
    #                    banda com as fontes e virava, ela mesma, o maior
    #                    elemento pintado — o Lighthouse media o LCP na foto,
    #                    em ~1,7s, em vez de medir no título, que aparece em
    #                    0,9s. Sem a prioridade alta, o texto (o conteúdo de
    #                    verdade) pinta primeiro e a arte entra logo atrás.
    #   eager=True    -> fetchpriority="high", para imagem que É o conteúdo.
    #   eager=False   -> loading="lazy", para tudo que está abaixo da dobra.
    if eager == "auto":
        loading = ' fetchpriority="auto"'
    elif eager:
        loading = ' fetchpriority="high"'
    else:
        loading = ' loading="lazy"'
    wh = _img_dims(rel_src)
    dims = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    img_tag = (f'<img{c} src="{rel(path, rel_src)}" alt="{esc(alt)}"{loading} '
               f'decoding="async"{dims}{hidden}>')
    base, _ = os.path.splitext(rel_src)
    full_w = wh[0] if wh else None
    sources = ""
    for ext, mime in ((".avif", "image/avif"), (".webp", "image/webp")):
        if not os.path.exists(_sibling(rel_src, ext)):
            continue
        entries = []
        for w in IMG_WIDTHS:
            variant = base + f"-{w}" + ext
            if full_w and full_w > w and os.path.exists(os.path.join(ROOT, "static", *variant.split("/"))):
                entries.append(f"{rel(path, variant)} {w}w")
        entries.append(f"{rel(path, base + ext)}" + (f" {full_w}w" if entries and full_w else ""))
        srcset = ", ".join(entries)
        sizes_attr = f' sizes="{sizes}"' if len(entries) > 1 else ""
        sources += f'<source type="{mime}" srcset="{srcset}"{sizes_attr}>'
    return f"<picture>{sources}{img_tag}</picture>" if sources else img_tag


def photo_or_art(path, slot, fallback_name, alt="", cls="", eager=False, sizes="100vw"):
    """
    Usa a foto real de content.site.IMAGES[slot] assim que o cliente
    fornecer o arquivo (ver comentário no bloco IMAGES). Até lá, cai para a
    arte SVG institucional — a seção nunca fica sem imagem.
    """
    src = IMAGES.get(slot)
    if is_placeholder(src):
        return art_img(path, fallback_name, alt, cls, eager=eager)
    return raster_img(path, src, alt, cls, eager=eager, sizes=sizes)


def card_photo(path, slot, alt=""):
    """
    Miniatura opcional no topo de um cartão (ver .lift__img no CSS). Sem
    entrada em content.site.IMAGES para este slot, não renderiza nada — o
    cartão continua exatamente como é hoje, só texto.

    `sizes` explícito (em vez do "100vw" padrão de raster_img): o cartão
    nunca ocupa a largura inteira da viewport, mesmo no mobile — é uma
    célula de grade (.rows--3, ver site.css) que estabiliza perto de
    ~380-400px de largura mesmo em telas grandes. Com "100vw" o navegador
    baixava a variante de 1400px cheia para um cartão que renderiza a um
    quarto desse tamanho — até 4x mais bytes que o necessário.
    """
    src = IMAGES.get(slot)
    if is_placeholder(src):
        return ""
    return f'<div class="lift__img">{raster_img(path, src, alt, sizes="(min-width: 48rem) 400px, 100vw")}</div>'


def artrow_img(path, src, alt=""):
    """
    Miniatura opcional no topo do bloco de metadados de uma linha de artigo
    (ver .artrow__img no CSS), acima da categoria. Sem imagem informada no
    campo "image" do artigo, não renderiza nada — a linha continua
    exatamente como é hoje, só texto.
    """
    if is_placeholder(src):
        return ""
    return f'<div class="artrow__img">{raster_img(path, src, alt)}</div>'


def artrow(path, href, image, category, title, excerpt, foot="", extra_attrs=""):
    """
    Uma linha de listagem de artigo (ver .artrow no CSS: usada em Conteúdos,
    nos destaques da home e nos relacionados de cada artigo).

    A categoria fica sempre no topo da coluna de texto, com foto ou sem. Antes
    ela mudava de lugar conforme houvesse imagem, e numa lista em que só parte
    dos artigos tem foto isso produzia duas ancoragens diferentes na mesma
    lista: metade das categorias numa margem, metade em outra. A coluna
    estreita passa a ser só da foto, então o texto de todas as linhas começa
    exatamente no mesmo ponto e a presença da imagem é a única diferença.
    """
    img_html = artrow_img(path, image, title)
    foot_html = f'<p class="artrow__foot">{foot}</p>' if foot else ""
    return f"""<a class="artrow" href="{rel(path, href)}"{extra_attrs}>
      <div class="artrow__meta">{img_html}</div>
      <div class="artrow__content"><p class="artrow__cat">{category}</p><h3>{title}</h3><p>{excerpt}</p>{foot_html}</div>
    </a>"""


def _thumb_variant(rel_src):
    """
    Caminho da miniatura quadrada dedicada (sufixo "-thumb", gerada à parte
    em 216x216 — ver LEIA-ME.txt) quando ela existe ao lado da foto
    original, para não servir o arquivo de 720x480 inteiro numa caixa de
    72px (.sidearts__img). Sem miniatura gerada para a foto, cai para o
    arquivo original, então nada quebra para uma foto nova.
    """
    base, ext = os.path.splitext(rel_src)
    thumb_rel = base + "-thumb" + ext
    if os.path.exists(os.path.join(ROOT, "static", *thumb_rel.split("/"))):
        return thumb_rel
    return rel_src


def sidearticle(path, href, image, title, foot=""):
    """
    Cartão compacto de artigo para a coluna lateral estreita (ver .sidearts
    no CSS: usado na barra de "outros conteúdos" ao lado do corpo do
    artigo). Miniatura pequena e quadrada + título + data, em vez do layout
    horizontal largo do artrow, que não cabe numa coluna de 4/12.
    """
    img_html = ""
    if not is_placeholder(image):
        img_html = f'<div class="sidearts__img">{raster_img(path, _thumb_variant(image), title)}</div>'
    foot_html = f'<p class="sidearts__foot">{foot}</p>' if foot else ""
    return f"""<a class="sidearts__item" href="{rel(path, href)}">
      {img_html}
      <div class="sidearts__body"><p class="sidearts__title">{title}</p>{foot_html}</div>
    </a>"""


_ICON_MAIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/></svg>')

_ICON_CHECK_CIRCLE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
                       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                       '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9"/></svg>')
_ICON_ALERT_CIRCLE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
                       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                       '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5"/>'
                       '<circle cx="12" cy="16.3" r=".6" fill="currentColor" stroke="none"/></svg>')


def form_status(kind, html):
    """
    Mensagem de confirmação/erro pós-envio (`.formstate`, ver site.js — o
    JS só alterna `data-show`, o HTML de cada estado já sai pronto do
    build). Ícone + texto na cor do estado, sem caixa nem borda lateral —
    o visual de "alerta" genérico foi trocado por algo mais discreto.
    `kind`: "ok" ou "err". `html` pode incluir markup (ex.: <strong>).
    """
    icon = _ICON_CHECK_CIRCLE if kind == "ok" else _ICON_ALERT_CIRCLE
    role = "status" if kind == "ok" else "alert"
    return (f'<div class="formstate formstate--{kind}" role="{role}">'
            f'<span class="formstate__icon" aria-hidden="true">{icon}</span>'
            f'<span>{html}</span></div>')


def newsletter_box(path):
    """
    Bloco de captação de e-mail para a coluna lateral do artigo, logo abaixo
    dos "Outros conteúdos" (ver .capture no CSS). Reaproveita a mesma
    engrenagem de envio dos outros formulários do site
    (`form[data-endpoint-form]`, ver site.js): sem endpoint configurado em
    ACROPOLE_CONFIG, cai em modo demonstração.
    """
    return f"""<div class="capture">
      <div class="capture__icon">{_ICON_MAIL}</div>
      <p class="capture__eyebrow">Inscreva-se</p>
      <p class="capture__heading">Receba conteúdos sobre crédito empresarial</p>
      <form class="capture__form" data-endpoint-form novalidate>
        <div class="field">
          <label for="nl-nome" class="sr-only">Seu nome</label>
          <input type="text" id="nl-nome" name="nome" placeholder="Seu nome" required aria-describedby="nl-nome-err">
          <span class="field__err" id="nl-nome-err">Informe seu nome.</span>
        </div>
        <div class="field">
          <label for="nl-email" class="sr-only">Seu e-mail</label>
          <input type="email" id="nl-email" name="email" placeholder="Seu e-mail ativo" data-validate="email" required aria-describedby="nl-email-err">
          <span class="field__err" id="nl-email-err">Informe um e-mail válido.</span>
        </div>
        <div class="hp" aria-hidden="true">
          <label for="nl-company">Não preencha este campo</label>
          <input type="text" id="nl-company" name="company_website" tabindex="-1" autocomplete="off">
        </div>
        <button type="submit" class="btn capture__submit" data-step-submit>
          <span class="spinner" aria-hidden="true"></span>Receber novidades
        </button>
        {form_status("ok", "Inscrição confirmada. Você passa a receber nossos conteúdos por e-mail.")}
        {form_status("err", "Não foi possível enviar agora. Tente novamente em instantes.")}
      </form>
    </div>"""


def comments_section(slug):
    """
    Comentários por artigo de Conteúdos, atrás de login com Google (pedido
    da cliente). Sem endpoint serverless nativo (o site é estático), então
    isto fala com deploy-extra/api/comments-*.php — hospedagem que roda PHP
    (Hostinger compartilhada, ver README item 181) com um banco MySQL
    próprio (deploy-extra/sql/schema.sql). Enquanto ACROPOLE_CONFIG.googleClientId
    não estiver preenchido, initComments() (site.js) mostra um aviso
    discreto no lugar do botão de login, em vez de uma seção quebrada/vazia.

    Publicação é automática, sem fila de moderação (decisão da cliente) —
    por isso cada pessoa só pode excluir o próprio comentário (endpoint
    comments-delete.php confere o "sub" do Google contra o autor do
    comentário) e existe um endpoint separado de exclusão por admin
    (comments-admin-delete.php, protegido por token) como válvula de
    segurança manual, sem precisar mexer direto no banco.
    """
    field_id = f"comment-body-{slug}"
    # A seção nasce com [hidden]: o HTML é gerado no build e não sabe se
    # ACROPOLE_CONFIG.googleClientId (config.js) e o backend em PHP já
    # estão configurados de verdade — initComments() (site.js) só tira o
    # [hidden] depois de confirmar os dois, em vez de arriscar mostrar a
    # seção quebrada (sem login, sem comentário nenhum carregando) antes da
    # cliente terminar de publicar o backend na Hostinger.
    return f"""<section class="band comments" id="comentarios" data-comments data-article="{slug}" hidden>
  <div class="shell">
    <h2 class="comments__heading">Comentários</h2>
    <p class="comments__sub">Entre com sua conta Google para comentar. Comentários publicados ficam visíveis para outros leitores.</p>

    <div class="comments__auth">
      <div class="comments__gsi"></div>
      <div class="comments__signedin" hidden>
        <img class="comments__avatar" alt="" width="32" height="32" loading="lazy">
        <span class="comments__username"></span>
        <button type="button" class="btn btn--line btn--sm comments__signout">Sair</button>
      </div>
    </div>

    <form class="comments__form" novalidate hidden>
      <div class="field">
        <label for="{field_id}" class="sr-only">Seu comentário</label>
        <textarea id="{field_id}" name="body" maxlength="2000" placeholder="Escreva seu comentário..." required></textarea>
        <span class="field__err">Escreva um comentário antes de publicar.</span>
      </div>
      <button type="submit" class="btn btn--sm comments__submit">
        <span class="spinner" aria-hidden="true"></span>Publicar comentário
      </button>
      {form_status("ok", "Comentário publicado.")}
      {form_status("err", "Não foi possível publicar agora. Tente novamente em instantes.")}
    </form>

    <ul class="comments__list" aria-live="polite"></ul>
    <p class="comments__empty" hidden>Seja a primeira pessoa a comentar.</p>
    <p class="comments__loaderr" hidden>Não foi possível carregar os comentários agora.</p>
  </div>
</section>"""


def video_grid(path):
    """
    Vitrine de vídeos do YouTube (ver content.site.VIDEOS). Cada cartão linka
    para o vídeo no próprio YouTube, sem player embutido — a miniatura vem de
    i.ytimg.com, liberado especificamente para isso no _headers. Com a lista
    vazia, não renderiza nada: sem vídeo real, não há seção a mostrar.
    """
    if not VIDEOS:
        return ""
    cards = []
    for v in VIDEOS:
        yid = v["youtube_id"]
        thumb = f"https://i.ytimg.com/vi/{yid}/hqdefault.jpg"
        url = f"https://www.youtube.com/watch?v={yid}"
        cards.append(f'''<a class="lift videocard" href="{esc(url)}"
        target="_blank" rel="noopener noreferrer">
        <div class="lift__img videocard__img"><img src="{esc(thumb)}" alt=""
          loading="lazy" decoding="async" aria-hidden="true">
          <span class="videocard__play" aria-hidden="true"></span></div>
        <span class="tag">{esc(v.get("canal", ""))}</span>
        <h3 style="margin-top:1rem">{esc(v["titulo"])}</h3>
        <p class="small muted">{esc(v.get("assunto", ""))}</p>
      </a>''')
    return f'''<section class="band band--stone band--snug">
  <div class="shell">
    {sechead("Referências", "Panorama internacional, direto da fonte.",
             "Uma curadoria de vídeos em inglês sobre estruturação de crédito, home equity e capital de giro. Conteúdo de terceiros, selecionado para complementar a leitura das páginas acima, aberto no próprio YouTube.")}
    <div class="rows rows--3">{"".join(cards)}</div>
  </div>
</section>'''


def is_placeholder(v):
    """Dado ainda não fornecido: None, vazio, ou marcado entre colchetes."""
    if v is None:
        return True
    v = str(v).strip()
    return not v or v.startswith("[")


def clink(label, href, cls="", pendente=None, attrs=""):
    """
    Nunca gera link fictício. Sem o dado, devolve um rótulo neutro em texto,
    e nunca um <a> que não leva a lugar nenhum.
    """
    c = f' class="{cls}"' if cls else ""
    if is_placeholder(label) or is_placeholder(href):
        return f'<span{c} data-pendente>{pendente or "A definir"}</span>'
    return f'<a{c} href="{href}"{attrs}>{label}</a>'


def mail_link(cls=""):
    addr = SITE["email"]
    c = f' class="{cls}"' if cls else ""
    if is_placeholder(addr):
        return f'<span{c} data-pendente>{PENDENTE["email"]}</span>'
    return f'<a{c} href="mailto:{addr}">{addr}</a>'


def field_row(dt, value, pendente):
    """Linha de dado que sempre existe, mas nunca fica vazia nem vira link morto."""
    if is_placeholder(value):
        inner = f'<span data-pendente>{pendente}</span>'
    else:
        inner = str(value)
    return f'<div class="deflist__row"><dt>{dt}</dt><dd>{inner}</dd></div>'



def btn(label, href, path, variant="", attrs=""):
    cls = "btn" + (" " + variant if variant else "")
    return f'<a class="{cls}" href="{rel(path, href)}"{attrs}>{label}</a>'


def tlink(label, href, path):
    return f'<a class="tlink" href="{rel(path, href)}">{label}</a>'


def fit_desc(lead, suffix="", limit=160):
    """Meta description dentro do que o Google exibe.

    Junta o sufixo institucional só quando ele cabe inteiro: uma descrição
    cortada no meio de uma frase é pior do que uma descrição mais curta.
    """
    lead = " ".join(lead.split())
    if not suffix:
        return lead[:limit].rstrip()
    joined = f"{lead} {suffix}".strip()
    return joined if len(joined) <= limit else lead[:limit].rstrip()


def sechead(tag, title, lead=None, wide=False, extra="", note=None, link=None, path=None):
    """Cabeçalho de seção: rótulo, título e, opcionalmente, apoio.

    Único caminho para montar esse bloco no site inteiro. Antes metade das
    seções o montava à mão, com margin-top inline no h2 e sem limite de medida,
    então a mesma manchete quebrava em pontos diferentes conforme a página em
    que estivesse.

    'lead' é a frase de abertura da seção; 'note' é um apontamento secundário
    (para onde ir ver o assunto completo) e 'link' o atalho correspondente.
    """
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    note_html = f'<p class="muted small measure-narrow mt-2">{note}</p>' if note else ""
    link_html = f'<div class="mt-2">{tlink(link[0], link[1], path)}</div>' if link else ""
    cls = "sechead sechead--wide" if wide else "sechead"
    return f"""<div class="{cls}" data-reveal>
      <span class="tag sechead__tag">{tag}</span>
      <h2>{title}</h2>
      {lead_html}{note_html}{link_html}{extra}
    </div>"""


def crumbs(items, path, light=False):
    """items: [(label, href|None)] — o último é a página atual."""
    lis = []
    for label, href in items:
        if href:
            lis.append(f'<li><a href="{rel(path, href)}">{label}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{label}</span></li>')
    cls = "crumbs crumbs--light" if light else "crumbs"
    return f'<nav class="{cls}" aria-label="Trilha de navegação"><ol>{"".join(lis)}</ol></nav>'


def accordion(items, ident="faq"):
    rows = []
    for i, (q, a) in enumerate(items):
        pid = f"{ident}-p-{i}"
        bid = f"{ident}-b-{i}"
        body = "".join(f"<p>{p}</p>" for p in (a if isinstance(a, list) else [a]))
        rows.append(f"""<div class="acc__item">
        <h3 style="margin:0"><button class="acc__btn" id="{bid}" aria-expanded="false" aria-controls="{pid}">
          <span>{q}</span><span class="acc__sign" aria-hidden="true"></span>
        </button></h3>
        <div class="acc__panel" id="{pid}" role="region" aria-labelledby="{bid}" data-open="false"><div>{body}</div></div>
      </div>""")
    return f'<div class="acc">{"".join(rows)}</div>'


def sequence(steps):
    rows = []
    for i, (title, desc) in enumerate(steps, 1):
        body = "".join(f"<p>{p}</p>" for p in (desc if isinstance(desc, list) else [desc]))
        rows.append(f"""<div class="seq__step" data-reveal>
        <div class="seq__n figures">{i:02d}</div>
        <div class="seq__t">{title}</div>
        <div class="seq__d">{body}</div>
      </div>""")
    return f'<div class="seq">{"".join(rows)}</div>'


def deflist(rows, split=False):
    """Lista de definições. Com split=True ela se divide em 2 colunas.

    Duas deflists lado a lado dentro de um .cols pareciam a solução óbvia,
    mas cada uma calcula a altura das próprias linhas: quando uma descrição
    tinha uma linha a mais que a vizinha, os filetes das duas colunas paravam
    de coincidir e a seção ficava com réguas tortas. Em uma lista só, dividida
    em 2 colunas pelo grid, os itens de uma mesma fileira compartilham altura
    e os filetes voltam a se alinhar.
    """
    out = "".join(
        f'<div class="deflist__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows
    )
    cls = "deflist deflist--split" if split else "deflist"
    return f'<dl class="{cls}" data-reveal>{out}</dl>'


def pointlist(items, split=False):
    out = "".join(f"<li>{i}</li>" for i in items)
    if split:
        return f'<ul class="pointlist pointlist--split" data-reveal>{out}</ul>'
    return f'<ul class="pointlist" data-reveal>{out}</ul>'


_ICONCARD_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                    '<path d="M20 6 9 17l-5-5"/></svg>')

# Ícones de traço fino, um por conceito, para a grade "Objetivo / Estrutura /
# Patrimônio e garantias / Capacidade e risco" — usados com iconcards(...,
# variant="line") para o selo ficar sem fundo, na cor do botão de CTA.
ICON_TARGET = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/>'
               '<circle cx="12" cy="12" r=".6" fill="currentColor" stroke="none"/></svg>')
ICON_LAYERS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="M3 13l9 5 9-5"/></svg>')
ICON_SHIELD = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M12 3 5 6v5c0 5 3 8 7 10 4-2 7-5 7-10V6l-7-3Z"/></svg>')
ICON_GAUGE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M12 16 15 10"/>'
              '<circle cx="12" cy="16" r="1" fill="currentColor" stroke="none"/></svg>')


def iconcards(items, four=False, variant=None):
    """
    Grade de cartões com selo circular, título em negrito e descrição curta —
    o formato "por que escolher" de uma página de produto. Cada item é
    (título, descrição) ou (título, descrição, svg_do_ícone); sem o terceiro
    valor, usa um selo de confirmação genérico.

    variant="line": selo sem fundo, traço fino, na cor do CTA — para grades
    onde cada item já tem seu próprio ícone (ver ICON_* acima).
    """
    cls = "iconcards iconcards--4" if four else "iconcards"
    card_cls = "iconcard iconcard--line" if variant == "line" else "iconcard"
    cards = []
    for it in items:
        title, desc = it[0], it[1]
        icon = it[2] if len(it) > 2 else _ICONCARD_CHECK
        cards.append(f'''<div class="{card_cls}" data-reveal>
      <span class="iconcard__badge">{icon}</span>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>''')
    return f'<div class="{cls}">{"".join(cards)}</div>'


def media_row(path, slot, fallback_art, body_html, alt=""):
    """
    Mesmo painel de media_aside (imagem à esquerda, foto real assim que
    existir e arte SVG até lá; conteúdo à direita, imagem primeiro no
    celular) mas para um bloco de texto qualquer, já pronto em HTML, em vez
    do formato fixo eyebrow/título/lead/bullets/cta. Usado onde um trecho de
    texto corrido (não um card de produto) precisa do mesmo padrão visual.
    """
    img = photo_or_art(path, slot, fallback_art, alt=alt, cls="mediarow__img",
                       sizes="(min-width: 760px) min(42vw, 500px), 100vw")
    return f'''<div class="mediarow" data-reveal>
      <div class="mediarow__media">{img}</div>
      <div class="mediarow__body">{body_html}</div>
    </div>'''


def media_aside(path, slot, fallback_art, eyebrow, title, lead, bullets, cta=None, alt="", reverse=False):
    """
    Painel com imagem de um lado (foto real assim que existir, arte SVG até
    lá) e conteúdo do outro: título, texto curto, lista de itens com selo e
    um CTA opcional. Mesmo formato do bloco de crédito BNDES nas páginas de
    produto de referência. `bullets` é uma lista de strings curtas (uma
    linha cada); `cta` é (rótulo, href) ou None.
    """
    img = photo_or_art(path, slot, fallback_art, alt=alt, cls="mediarow__img",
                       sizes="(min-width: 760px) min(42vw, 500px), 100vw")
    items = "".join(
        f'<li><span class="mediarow__bullet">{_ICONCARD_CHECK}</span>{b}</li>' for b in bullets
    )
    cta_html = f'<div class="mt-2">{btn(cta[0], cta[1], path)}</div>' if cta else ""
    order = " mediarow--reverse" if reverse else ""
    return f'''<div class="mediarow{order}" data-reveal>
      <div class="mediarow__media">{img}</div>
      <div class="mediarow__body">
        <span class="tag sechead__tag">{eyebrow}</span>
        <h3 style="margin-top:1rem">{title}</h3>
        <p class="muted small measure-narrow mt-1">{lead}</p>
        <ul class="mediarow__list">{items}</ul>
        {cta_html}
      </div>
    </div>'''


# Script mínimo e síncrono, direto no <head>, antes de qualquer conteúdo:
# só ele decide se a página vai esconder os blocos [data-reveal] para
# animar a entrada no scroll. Sem isso rodando antes da primeira pintura,
# um bloco escondido por CSS e nunca revelado (JS desabilitado, ou sem
# suporte a IntersectionObserver) ficaria invisível para sempre — por
# isso a classe some do <html>, não aparece por padrão.
#
# O mesmo bloco também desliga a restauração automática de scroll do
# navegador: por padrão, voltar (ou avançar) para uma página que você já
# tinha rolado devolve exatamente aquele ponto de rolagem, em vez do topo
# — cada página deve sempre abrir do início. Precisa rodar síncrono e cedo
# (antes do navegador aplicar a posição salva) para não piscar a posição
# errada por uma fração de segundo antes de corrigir. O "behavior:instant"
# explícito é essencial: o site usa scroll-behavior:smooth no <html> (para
# os cliques em âncora), e sem forçar instant aqui esse scroll-to-topo
# herdava a animação suave — a página abria embaixo e "subia" visualmente
# até o topo, em vez de já abrir no topo.
REVEAL_DETECT_JS = (
    "(function(){try{"
    "if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches"
    "&&'IntersectionObserver' in window){"
    "document.documentElement.classList.add('js-reveal')}"
    "}catch(e){}"
    "try{"
    "if('scrollRestoration' in history){history.scrollRestoration='manual'}"
    "var toTop=function(){window.scrollTo({top:0,left:0,behavior:'instant'})};"
    "toTop();"
    "window.addEventListener('pageshow',toTop);"
    "}catch(e){}"
    "})();"
)

# Logo "Acrópole Capital" vetorizado (traçado a partir da arte oficial em
# PNG/WebP com potrace) e definido uma única vez como <symbol>, reaproveitado
# via <use> no cabeçalho, na gaveta e no rodapé — evita repetir o path inteiro
# em cada um dos três lugares por página.
#
# O traçado passou por uma simplificação de coordenadas (svgo, precisão 0):
# 27 KB -> 16 KB, sem diferença visível. O potrace saía com casas decimais
# num viewBox de 3308 unidades de largura — uma casa decimal ali equivale a
# 0,004 px na tela, num logo que aparece com 133 px. Como este path vai
# INLINE em toda página (é o preço de poder pintá-lo com currentColor, claro
# no cabeçalho escuro e escuro no claro), os 11 KB economizados saem do
# caminho crítico das 58 páginas. Comparado pixel a pixel antes e depois, em
# 264 px e 800 px de largura: só a antisserrilhagem das bordas muda.
LOGO_MARK_VB = "0 0 3308 992"
LOGO_MARK_D = "M241 25c-2 1-1 14 1 15q2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 0 2 8c-1 8 0 7-2 8q-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6t-2 6c1 6 0 5-2 6q-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6t-2 6c1 6 0 5-2 6q-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 6q1 6-2 6-2 0-2 8v7l43 1h43l7-7 7-9 2-4 2-4q0-3 6-8l6-8q0-2 14-16t14-16c0-3 9-12 12-12q2 0 16-14t16-14l8-6q6-6 8-6t6-4 6-4 6-4 6-4 4-2 4-2 4-2 4-2 6-4 6-4 4-2 4-2 4-2 4-2 4-2 4-2 4-2 4-2 4-2 6-2q6 1 6-2 1-2 4-2t4-2 4-2 4-2 6-2q6 1 6-2 1-2 4-2t4-2 6-2q6 1 6-2 1-2 4-2t4-2 6-2q6 1 6-2t6-2c6 1 5 0 6-2q1-2 6-2c5 0 14 8 14 12l2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4q3 1 2 6-1 6 2 6 2 1 2 4t2 4 2 4 2 4q3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6q2 1 2 4t2 4 2 4 2 4q3 1 2 6-1 6 2 6l2 4q0 2 5 7c5 5 5 5 77 5s72 0 75-3c4-4 4-11 1-13q-2-1-2-6 1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-4-2-4-2-6q1-6-2-6t-2-6c1-6 0-5-2-6q-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-5-5-9c-5-5-5-5-81-5zm60 162 3 5 2 4q2 1 2 6-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 4 2 4 2 6q-1 6 2 6t2 6c-1 6 0 5 2 6q2 1 2 4t2 4 2 4 2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4 2 6q-1 6 2 6 2 1 2 4t2 4q2 0 2 8c-1 8-1 8-4 8q-3 0-4 2-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2q0 3-8 2c-8-1-7 0-8 2s-2 2-8 2-7 0-8 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2s-2 2-8 2-7 0-8 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2q0 3-8 2c-8 0-8 0-8-4q0-3 2-4t2-4 2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4 2-4 2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4 2-4 2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4 2-4q1-8 9-1M2856 30q-1 2-4 2t-4 2q0 3-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2q0 3-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2s-2 2-8 2-7 0-8 2q0 3-10 2c-10-1-9 0-10 2l-4 2q-6 2-8 8c-2 6 5 8 8 8l4 2q1 3 6 2 6-1 6 2 1 2 4 2t4 2l4 2q2 0 7 5c5 5 5 5 5 35s0 31 2 32 2 2 2 208 0 207-2 208-2 2-2 34 0 33-2 34l-2 4q0 2-5 7c-5 5-5 5-19 5s-14 0-19 5c-6 6-6 8 0 14 5 5 5 5 101 5s96 0 99-3q4-1 3-9c0-10-2-12-18-12-12 0-13 0-14-2l-4-2q-7-1-8-10 1-5-2-6c-2-1-2-2-2-24s0-23-2-24-2-2-2-248 0-247 2-248 2-2 2-36 0-34-3-37c-4-4-11-4-13-1M1611 75c-7 7-7 7-7 11q1 5-2 6-2 1-2 6 1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6t-2 6c1 6 0 5-2 6q-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 6q1 7 4 6 3 1 4-2l4-2 8-6q6-6 8-6t8-6l8-6q2 0 12-10t12-10l10-8q8-8 10-8l8-6 8-6q2 0 10-8t10-8 12-10 12-10l8-6 8-6q3 0 5-3 5-3 0-6c-5-3-3-3-57-3h-55zM828 266q0 3-10 2c-10-1-9 0-10 2q0 3-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2-1 2-4 2t-4 2-4 2-4 2-4 2-4 2-4 2-6 4-6 4-10 8l-10 8c-3 0-24 21-24 24q0 3-6 8-6 6-6 8 0 3-4 6-4 4-4 6 0 3-2 4t-2 4-2 4-2 4-2 4-2 4-2 4-2 6q1 6-2 6t-2 6c1 6 0 5-2 6q-2 0-2 8c0 8 0 7-2 8s-2 2-2 16 0 15-2 16-2 2-2 20 0 19 2 20 2 2 2 16 0 15 2 16q3 0 2 8c-1 8 0 7 2 8q3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6q2 1 2 4t2 4 2 4 2 4 2 4 2 4 2 4 4 6 4 6a343 343 0 0 0 60 56q3 0 4 2t4 2 4 2q1 3 6 2 6-1 6 2 1 2 4 2t4 2q0 3 8 2c8-1 7 0 8 2s2 2 14 2 13 0 14 2c2 3 26 3 28 0 1-2 2-2 14-2s13 0 14-2 2-2 10-2 9 0 10-2q1-2 6-2 6 1 6-2 1-2 4-2t4-2 4-2 4-2 4-2 6-4 6-4 8-6l8-6 29-27c27-26 27-27 27-31 0-10-11-14-18-6q-3 4-6 4t-6 4-6 4-4 2-4 2q-2 0-6 4-3 4-6 4t-4 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2s-2 2-6 2-5 0-6 2-2 2-30 2-29 0-30-2q-1-2-6-2-6 1-6-2t-6-2c-6 1-5 0-6-2q-1-2-4-2-2 0-6-4-3-3-6-4a122 122 0 0 1-32-34q-4-3-4-6t-4-6-4-6-2-4-2-6q1-6-2-6t-2-6c1-6 0-5-2-6s-2-2-2-6 0-5-2-6q-2 0-2-10c0-10 0-9-2-10s-2-2-2-48 0-47 2-48q3 0 2-10c-1-10 0-9 2-10q3-1 2-6-1-6 2-6t2-6c-1-6 0-5 2-6q2-1 2-4t2-4 2-4 4-6 4-6 4-6 4-6 7-9 9-7 6-4 6-4 4-2 4-2 4-2q0-2 8-2c8 0 7 0 8-2q0-2 10-2c10 0 9 0 10 2q1 3 6 2 6-1 6 2 1 3 6 2c4 0 4 0 13 9q9 9 9 11 1 3 4 6 5 3 4 8 0 5 2 6 3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6q3 0 2 8c-1 8 0 7 2 8q3 1 2 6 0 5 5 9c5 4 5 5 9 5q5 0 6 2 0 3 10 2c10-1 9 0 10-2s2-2 10-2c13 0 14-1 14-20 0-14 0-15 2-16s2-2 2-24 0-22-9-31l-11-9-4-2q-1-2-4-2t-4-2-4-2-4-2-4-2-4-2-4-2-4-2-6-2q-6 1-6-2 0-2-8-2c-8 0-7 0-8-2s-2-2-12-2-11 0-12-2-2-2-30-2-29 0-30 2m344 0q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2q0 3-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2q0 3-8 2c-8-1-7 0-8 2s-2 2-8 2-7 0-8 2-2 2-8 2-7 0-8 2q0 3-10 2c-10-1-9 0-10 2q-1 3-6 2-4 0-7 3-6 5 2 12c5 5 5 5 11 5q8 0 8 2l4 2 11 9c9 9 9 9 9 15q0 8 2 8c2 1 2 2 2 108s0 107-2 108-2 2-2 34 0 33-2 34q-2 0-2 8 0 11-8 12l-4 2c-1 2-2 2-16 2s-14 0-19 5c-6 6-6 8 0 14 5 5 5 5 105 5s100 0 103-3q4-1 3-9c0-11-2-12-20-12-14 0-15 0-16-2l-4-2q-7-1-8-10 1-5-2-6c-2-1-2-2-2-14s0-13-2-14-2-2-2-112 0-111 2-112q3-1 2-6-1-4 6-10l6-8c0-3 9-12 12-12l4-2q1-2 4-2t4-2c1-2 2-2 22-2s21 0 22 2q1 3 6 2 6-1 6 2t6 2 8 4q4 4 6 4t6 4 6 4 4 2c2 4 13 3 17-1 3-3 3-3 3-17s0-15 2-16 2-2 2-14 0-13 2-14 2-2 2-20 0-18-5-23q-4-5-9-5-5 1-6-2c-1-2-2-2-20-2s-19 0-20 2q-1 3-6 2-6-1-6 2-1 2-4 2-2 0-6 4-3 4-6 4c-3 0-28 25-28 28l-8 10q-8 8-8 10l-6 8-6 8q-1 6-9 8c-3 0-3 0-3-30 0-28 0-29 2-30 4-2 3-21-1-25q-5-6-9-1m364 0c-1 2-2 2-12 2s-11 0-12 2q0 3-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2q-1 2-4 2t-4 2-4 2-4 2-4 2-6 4-6 4-8 6-8 6a168 168 0 0 0-38 40q-6 6-6 8 0 3-4 6-4 4-4 6 0 3-2 4t-2 4-2 4-2 4-2 4-2 6q1 6-2 6t-2 6c1 6 0 5-2 6q-2 0-2 8c0 8 0 7-2 8q-2 0-2 10c0 10 0 9-2 10s-2 2-2 30 0 29 2 30 2 2 2 12 0 11 2 12q3 1 2 6-1 6 2 6t2 8c-1 8 0 7 2 8q2 1 2 4t2 4 2 4 2 4 2 4 2 4 2 4 2 4l2 4q0 3 6 8l6 8a129 129 0 0 0 36 34q6 6 8 6t6 4 6 4 4 2 4 2 6 4q3 5 8 4 5 0 6 2t4 2 4 2q1 3 6 2 6-1 6 2t6 2c6-1 5 0 6 2s2 2 12 2 11 0 12 2 2 2 36 2 35 0 36-2 2-2 10-2 9 0 10-2q1-2 6-2 6 1 6-2t6-2c6 1 5 0 6-2q1-2 4-2t4-2 4-2 4-2 4-2 4-2 4-2 4-2l4-2 8-6 8-6a302 302 0 0 0 52-56q0-3 2-4t2-4 2-4 2-4 2-4 2-4 2-4 2-4 2-4q3-1 2-6-1-6 2-6t2-6c-1-6 0-5 2-6q3 0 2-10c-1-10 0-9 2-10s2-2 2-36 0-35-2-36q-2 0-2-8c0-8 0-7-2-8s-2-2-2-8 0-7-2-8q-2-1-2-6 1-6-2-6-2-1-2-4t-2-4-2-4-2-4-2-4-2-4-2-4-4-6-4-6-6-8-6-8a168 168 0 0 0-40-38q-5-6-8-6l-4-2q-1-2-4-2t-4-2-4-2-4-2-4-2-4-2-4-2-4-2-4-2-4-2q0-2-8-2c-8 0-7 0-8-2q-1-2-6-2-6 1-6-2c-1-2-2-2-12-2s-11 0-12-2-2-2-26-2-25 0-26 2m36 24q1 3 6 2 6-1 6 2 1 2 4 2t4 2l4 2a150 150 0 0 1 36 38q4 4 4 6 0 3 2 4t2 4 2 4 2 4 2 4q3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6s2 2 2 6 0 5 2 6 2 2 2 12 0 11 2 12 2 2 2 12 0 11 2 12 2 2 2 54 0 53-2 54q-2 0-2 10c0 10 0 9-2 10q-2 0-2 8c0 8 0 7-2 8q-2 1-2 6 1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 4-4 6q-3 3-4 6c0 3-21 24-24 24l-4 2q-1 2-4 2t-4 2-4 2-4 2c-1 2-2 2-22 2s-21 0-22-2q-1-2-4-2t-4-2-4-2-6-4q-3-3-6-4c-3 0-24-21-24-24q0-3-4-6t-4-6-2-4-2-4-2-4-2-4-2-4-2-4-2-4-2-4-2-4-2-6q1-6-2-6t-2-6c1-6 0-5-2-6s-2-2-2-12 0-11-2-12-2-2-2-12 0-11-2-12-2-2-2-44 0-43 2-44 2-2 2-14 0-13 2-14 2-2 2-10 0-9 2-10q2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4 2-4 4-6 4-6c0-3 29-32 32-32l4-2q1-2 4-2t4-2 6-2q6 1 6-2c1-2 2-2 14-2s13 0 14 2m488-24q0 3-8 2c-8-1-7 0-8 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2q-1 2-4 2t-4 2-4 2-4 2-4 2-6 4-6 4-8 6l-8 6q-2 0-16 14c-14 14-14 14-17 11-4-3-5-23-1-25 2-1 2-2 2-20l-1-19-9-1q-10 0-10 2-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2s-2 2-8 2-7 0-8 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2s-2 2-8 2-7 0-8 2-2 2-8 2-7 0-8 2-2 2-8 2-7 0-8 2-2 2-8 2q-6-1-9 3c-6 6-1 13 7 13q5 0 6 2 1 3 6 2 6-1 6 2 1 2 4 2t4 2l4 2c4 0 12 9 12 14q0 5 2 6a11409 11409 0 0 1-2 486c0 16 0 16-7 23s-7 7-19 7-13 0-14 2l-4 2q-7 1-8 10 0 4 3 7c5 5 202 5 206 0q7-7-2-16c-5-5-5-5-17-5s-13 0-14-2l-4-2q-7-1-8-10 1-5-2-6c-2-1-2-2-2-22s0-21-2-22-2-2-2-60 0-58 3-61q5-6 9-1 1 2 4 2t4 2q0 3 8 2c8-1 7 0 8 2q0 3 10 2c10-1 9 0 10 2s2 2 28 2 27 0 28-2 2-2 12-2 11 0 12-2q0-2 8-2c8 0 7 0 8-2q1-2 6-2 6 1 6-2 1-2 4-2t4-2 6-2q6 1 6-2 1-2 4-2t6-4 6-4 4-2 4-2 6-4q3-3 6-4c3 0 52-49 52-52l2-4q2-1 2-4 0-2 4-6 4-3 4-6t2-4 2-4 2-4 2-4 2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3 0 2-10c-1-10 0-9 2-10q3 0 2-8c-1-8 0-7 2-8s2-2 2-36 0-35-2-36-2-2-2-10 0-9-2-10q-2 0-2-8c0-8 0-7-2-8q-2-1-2-6 1-6-2-6t-2-6c1-6 0-5-2-6q-2-1-2-4t-2-4-2-4-2-4-2-4-4-6-4-6-4-6q-3-3-4-6a158 158 0 0 0-38-36q-4-4-6-4-3 0-4-2t-4-2-4-2-4-2-4-2-6-2q-6 1-6-2 0-2-8-2c-8 0-7 0-8-2s-2-2-12-2-11 0-12-2-2-2-14-2-13 0-14 2m-16 60q1 3 6 2 6-1 6 2 1 2 4 2t4 2 4 2 6 4 6 4c3 0 24 21 24 24q1 3 4 6 4 4 4 6 0 3 2 4t2 4 2 4 2 4 2 4 2 4 2 4q3 1 2 6-1 6 2 6t2 10c-1 10 0 9 2 10s2 2 2 12 0 11 2 12 2 2 2 40 0 39-2 40-2 2-2 12 0 11-2 12q-2 0-2 8c0 8 0 7-2 8q-2 1-2 4t-2 4-2 4-2 4-2 4-2 4-2 4-4 6q-3 3-4 6c0 3-29 32-32 32l-4 2q-1 2-4 2t-4 2-4 2-4 2q0 3-10 2c-10-1-9 0-10 2-2 3-14 3-16 0-1-2-2-2-12-2s-11 0-12-2q-1-2-4-2t-4-2-4-2-6-4q-3-3-6-4c-3 0-12-9-12-12q0-3-4-6t-4-6-2-4-2-6q1-6-2-6t-2-6c1-6 0-5-2-6s-2-2-2-14 0-13-2-14-2-2-2-104V366l9-9 11-9 8-6 8-6 4-2q1-2 4-2t4-2 6-2q6 1 6-2c1-2 2-2 24-2s23 0 24 2m424-60c-1 2-2 2-12 2s-11 0-12 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2q-1 2-4 2t-4 2-4 2-4 2-4 2-4 2-4 2-6 4-6 4-8 6-8 6a168 168 0 0 0-38 40q-6 6-6 8 0 3-4 6-4 4-4 6 0 3-2 4t-2 4-2 4-2 4-2 4-2 6q1 6-2 6-2 1-2 4t-2 4q-2 0-2 8c0 8 0 7-2 8s-2 2-2 12 0 11-2 12-2 2-2 32 0 31 2 32 2 2 2 12 0 11 2 12q3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6s2 2 2 6 0 5 2 6q2 1 2 4t2 4 2 4 2 4l2 4q0 3 6 8l6 8a213 213 0 0 0 56 50q1 2 4 2t6 4 6 4 4 2 4 2 4 2q1 3 6 2 6-1 6 2t6 2c6-1 5 0 6 2s2 2 6 2 5 0 6 2 2 2 12 2 11 0 12 2a280 280 0 0 0 92-4q1-2 6-2 6 1 6-2t6-2c6 1 5 0 6-2q1-2 4-2t4-2 4-2 4-2 4-2 4-2 4-2 4-2l4-2 8-6 8-6a262 262 0 0 0 54-60q2-1 2-4t2-4 2-4 2-4q3-1 2-6-1-6 2-6t2-6c-1-6 0-5 2-6s2-2 2-6 0-5 2-6q3 0 2-10c-1-10 0-9 2-10s2-2 2-16 0-15 2-16 2-2 2-14 0-13-2-14-2-2-2-14 0-13-2-14-2-2-2-10 0-9-2-10q-2-1-2-6 1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4 0-2-4-6-4-3-4-6t-4-6q-3-3-4-6a343 343 0 0 0-54-52q-4-4-6-4-3 0-4-2t-4-2-4-2-4-2-4-2-4-2-4-2-6-2q-6 1-6-2t-6-2c-6 1-5 0-6-2q0-2-8-2c-8 0-7 0-8-2s-2-2-12-2-11 0-12-2-2-2-28-2-27 0-28 2m44 24q1 2 4 2t4 2 4 2 4 2l4 2c3 0 28 25 28 28q1 3 4 6 4 4 4 6 0 3 2 4t2 4 2 4 2 4 2 4 2 4 2 4q3 1 2 6-1 6 2 6t2 8c-1 8 0 7 2 8s2 2 2 8 0 7 2 8 2 2 2 8 0 7 2 8 2 2 2 22 0 21 2 22 2 2 2 30 0 29-2 30-2 2-2 20 0 19-2 20q-2 0-2 8c0 8 0 7-2 8q-2 1-2 6 1 6-2 6-2 1-2 4t-2 4-2 4-2 4-2 4-2 4l-2 4q0 3-6 8l-6 8c0 3-9 12-12 12q-3 1-6 4-4 4-6 4-3 0-4 2t-4 2-4 2c-1 2-2 2-22 2s-21 0-22-2q-1-2-4-2t-4-2-4-2-4-2l-4-2a150 150 0 0 1-40-44q0-3-2-4t-2-4-2-4-2-4-2-4-2-4-2-4-2-6q1-6-2-6-2 0-2-8c0-8 0-7-2-8s-2-2-2-8 0-7-2-8-2-2-2-12 0-11-2-12-2-2-2-50 0-49 2-50 2-2 2-12 0-11 2-12q3 0 2-8c-1-8 0-7 2-8q3-1 2-6-1-6 2-6t2-6c-1-6 0-5 2-6q2-1 2-4t2-4 2-4 4-6 4-6 2-4l2-4c0-3 17-20 20-20q3 0 6-4 4-4 6-4 3 0 4-2t6-2q6 1 6-2c1-2 2-2 18-2s17 0 18 2m584-24q0 3-10 2c-10-1-9 0-10 2q-1 3-6 2-6-1-6 2t-8 2c-8-1-7 0-8 2q-1 2-4 2t-4 2-4 2-6 4-6 4-4 2l-4 2-12 10q-10 10-12 10-6 2-8 8 0 2-10 12t-10 12-4 6-4 6-2 4-2 4-2 4-2 4-2 4-2 4-2 4-2 4-2 4-2 6q1 6-2 6-2 0-2 8c0 8 0 7-2 8q-2 0-2 10c0 10 0 9-2 10s-2 2-2 18 0 17-2 18q-2 0-2 8c0 8 0 7 2 8s2 2 2 16 0 15 2 16 2 2 2 10 0 9 2 10q3 0 2 8c-1 8 0 7 2 8q3 1 2 6-1 6 2 6 2 1 2 4t2 4 2 4 2 4 2 4 2 4 2 4 2 4 2 4 4 6 4 6a239 239 0 0 0 46 44q4 4 6 4 3 0 4 2t4 2 4 2 4 2 4 2 4 2 4 2q1 3 6 2 6-1 6 2t8 2c8-1 7 0 8 2s2 2 12 2 11 0 12 2c2 3 30 3 32 0 1-2 2-2 14-2s13 0 14-2q0-2 8-2c8 0 7 0 8-2q1-2 6-2 6 1 6-2 1-2 4-2t4-2 4-2 4-2 4-2 6-4 6-4 8-6l8-6a213 213 0 0 0 44-46c8-7 8-8 8-12 0-10-11-14-18-6q-3 4-6 4t-6 4-6 4-6 4q-4 4-6 4-3 0-4 2t-4 2-4 2-4 2-4 2q-1 3-6 2-6-1-6 2t-6 2c-6-1-5 0-6 2s-2 2-32 2-31 0-32-2q-1-2-6-2-6 1-6-2-1-2-4-2t-4-2-4-2-6-4q-3-3-6-4c-3 0-36-33-36-36l-2-4q-2-1-2-4 0-2-4-6-4-3-4-6t-2-4-2-6q1-6-2-6t-2-6c1-6 0-5-2-6q-2 0-2-8c0-8 0-7-2-8s-2-2-2-30 0-28 3-31l5-3 4-2c1-2 2-2 120-2 140 0 124 3 124-22 0-16 0-17-2-18s-2-2-2-12 0-11-2-12q-2-1-2-6 1-6-2-6-2-1-2-4t-2-4-2-4-2-4-2-4-2-4-2-4-4-6q-3-3-4-6a158 158 0 0 0-38-36q-4-4-6-4-3 0-4-2t-4-2-4-2-4-2-4-2-6-2q-6 1-6-2t-6-2c-6 1-5 0-6-2q0-2-10-2c-10 0-9 0-10-2s-2-2-24-2-23 0-24 2m28 24q1 2 4 2t4 2 4 2 4 2l4 2c3 0 12 9 12 12l6 8 6 8 2 4q2 1 2 4t2 4q3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6s2 2 2 14 0 13 2 14c3 2 3 9-1 13-5 5-150 5-154 0-4-4-5-19-1-21q3 0 2-10c-1-10 0-9 2-10q3-1 2-6-1-6 2-6t2-6c-1-6 0-5 2-6q2-1 2-4 0-2 4-6 4-3 4-6t4-6 4-6q2-6 8-8 3 0 6-4 4-4 6-4 3 0 4-2t6-2q6 1 6-2c1-2 2-2 14-2s13 0 14 2m-996 532q-1 2-4 2t-4 2l-4 2c-3 0-16 13-16 16l-2 4q-2 1-2 4t-2 4-2 4-2 4c-2 1-2 2-2 28s0 27 2 28q3 1 2 6-1 6 2 6l2 4c0 3 21 24 24 24l4 2q0 3 8 2c8-1 7 0 8 2 2 3 26 3 28 0q1-2 6-2 6 1 6-2l4-2c3 0 24-21 24-24l2-4q3 0 2-8c0-7 0-7-5-8q-10 1-11 8l-11 13c-11 11-11 11-15 11q-5 0-6 2c-2 3-22 3-24 0q-1-2-6-2c-4 0-4 0-13-9l-9-11-2-4q-2-1-2-6 1-6-2-6c-2-1-2-2-2-18s0-17 2-18q3-1 2-6-1-6 2-6 2-1 2-4t2-4l2-4c0-3 9-12 12-12l4-2c1-2 2-2 20-2s19 0 20 2l4 2c3 0 16 13 16 16q1 7 10 8c7 0 13-9 8-12l-2-4c0-3-21-24-24-24l-4-2c-1-2-2-2-26-2s-25 0-26 2m215 1q-3 3-3 7 1 5-2 6-2 1-2 4t-2 4-2 6q1 6-2 6t-2 6c1 6 0 5-2 6q-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4l-2 4c-4 3 2 8 8 8s14-8 14-14q0-5 2-6 3-1 2-6 0-5 5-9c5-5 5-5 33-5s28 0 31 3l3 5 2 4q2 1 2 4t2 4q3 1 2 6c0 7 8 14 15 14 5 0 5 0 5-8q0-8-2-8-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6t-2-6c1-6 0-5-2-6q-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6-2-1-2-4t-2-4-2-6q1-6-2-6l-2-4q0-2-5-7-11-9-20-2m14 28 3 5 2 4q3 1 2 6-1 6 2 6t2 6c-1 6 0 5 2 6q2 1 2 4t2 4q3 0 2 8v8h-21c-20 0-21 0-23-2l-3-2c-2 0-1-4 1-4q2-1 2-4t2-4q3-1 2-6-1-6 2-6 2-1 2-4t2-4q3-1 2-6-1-6 2-6t2-6q1-11 9-3m142-28c-5 5-5 134 0 138a10 10 0 0 0 14 0c3-3 3-3 3-25 0-30-1-28 24-28 18 0 19 0 20-2s2-2 10-2 9 0 10-2l4-2 11-9c9-9 9-9 9-27s0-19-2-20l-2-4c0-3-9-12-12-12l-4-2q0-2-8-2c-8 0-7 0-8-2s-2-2-34-2c-33 0-33 0-35 3m69 15q1 3 6 2 9 1 10 8l2 4c2 1 2 2 2 12s0 10-7 17-7 7-11 7q-5 0-6 2c-1 2-2 2-22 2-28 0-26 2-26-28s-2-28 28-28c22 0 23 0 24 2m127-15c-5 5-5 134 0 138q5 6 10 0c3-3 3-3 3-69s0-66-3-69q-6-6-10 0m100 0q-6 5 0 10c3 3 3 3 21 3 27 0 24-7 24 64 0 58 0 58 3 61a10 10 0 0 0 14 0c3-3 3-3 3-61 0-71-3-64 24-64 18 0 18 0 21-3q3-3 3-5t-3-5c-5-5-106-5-110 0m236 0-3 5-2 4q-2 1-2 6 1 6-2 6t-2 6c1 6 0 5-2 6q-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-2 1-2 4t-2 4-2 6q1 6-2 6-3 2 1 5c6 6 17 2 17-5l2-4q2-1 2-6-1-6 2-6l2-4q0-2 5-7c5-5 5-5 33-5s28 0 31 3l3 5 2 4q2 1 2 6-1 6 2 6 2 1 2 6 0 10 13 10 7 2 7-6 0-5-2-6t-2-6q0-6-2-6-2-1-2-4t-2-4q-3-1-2-6 1-6-2-6t-2-6c1-6 0-5-2-6q-2-1-2-4t-2-4q-3-1-2-6 1-6-2-6-2-1-2-4t-2-4q-3-1-2-6 1-6-2-6-2-1-2-4t-2-4q-3-1-2-6 1-6-2-6-2-1-2-4t-2-4q-3-1-2-6c0-11-18-19-25-11m14 28q3 3 3 7-1 5 2 6 2 1 2 4t2 4 2 6q-1 6 2 6t2 6c-1 6 0 5 2 6s2 2 2 6c-1 6-1 6-21 6s-21 0-23-2l-3-2c-2 0-1-4 1-4q2-1 2-6-1-5 2-6 2-1 2-4t2-4 2-6q-1-6 2-6t2-6c-1-6 0-5 2-6q2-1 2-4 1-8 9-1m142-28c-5 5-5 134 0 138s89 5 94 0q3-3 3-5t-3-5c-3-3-3-3-37-3s-34 0-37-3-3-3-3-61 0-58-3-61a10 10 0 0 0-14 0"


def logo_sprite():
    """Define o símbolo do logo uma única vez por página (fora da vista,
    logo após <body>); os três usos (cabeçalho, gaveta, rodapé) referenciam
    via <use>, evitando repetir ~27kB de path três vezes por página."""
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
            f'<symbol id="brand-mark" viewBox="{LOGO_MARK_VB}">'
            f'<path d="{LOGO_MARK_D}"/></symbol></svg>')


def brand_mark(cls=""):
    """Marca vetorizada da Acrópole Capital. Herda a cor do contexto via
    currentColor, então funciona igual no cabeçalho transparente, na gaveta
    e no rodapé escuro sem CSS extra por lugar."""
    extra = f" {cls}" if cls else ""
    return (f'<svg class="brand__mark{extra}" viewBox="{LOGO_MARK_VB}" '
            f'aria-hidden="true" focusable="false"><use href="#brand-mark"></use></svg>')


_LINKCARD_ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                    '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def linkcards(path, items, four=False):
    """
    Cartões de referência cruzada com selo, título, descrição curta e link
    "Saiba mais" — formato de vitrine de produtos relacionados. `items` é
    uma lista de (título, descrição, href, rótulo_do_link opcional).
    """
    # Em 2 colunas, um número ímpar de cartões deixa metade da última fileira
    # vazia — com 5 cartões o buraco é do tamanho de um cartão inteiro. Em 3
    # colunas a sobra cai para um terço da fileira e a grade fecha melhor.
    cls = "iconcards iconcards--4" if four else "iconcards"
    if not four and len(items) % 2 == 1 and len(items) > 3:
        cls += " iconcards--3"
    cards = []
    for it in items:
        title, desc, href = it[0], it[1], it[2]
        label = it[3] if len(it) > 3 else "Saiba mais"
        cards.append(f'''<a class="iconcard linkcard" href="{rel(path, href)}" data-reveal>
      <span class="iconcard__badge">{_LINKCARD_ARROW}</span>
      <h3>{title}</h3>
      <p>{desc}</p>
      <span class="linkcard__cta">{label} <span aria-hidden="true">&rarr;</span></span>
    </a>''')
    return f'<div class="{cls}">{"".join(cards)}</div>'


def benefits_cards(items, four=False):
    """
    Mesma fonte de dados do pointlist ("<strong>Título.</strong> Descrição."),
    renderizada como grade de iconcards — usada nas seções "Benefícios" das
    páginas de solução, no formato de cartão de produto.
    """
    parsed = []
    for raw in items:
        m = re.match(r"\s*<strong>(.*?)</strong>\s*(.*)", raw, re.S)
        if m:
            title, desc = m.group(1).rstrip("."), m.group(2)
        else:
            title, desc = "", raw
        parsed.append((title, desc))
    return iconcards(parsed, four=four)


def statrail(items, four=True):
    cls = "statrail statrail--4" if four else "statrail"
    cells = "".join(
        f'<div class="statrail__c"><span class="statrail__v">{v}</span>'
        f'<span class="statrail__l">{l}</span></div>' for v, l in items
    )
    return f'<div class="{cls}" data-reveal>{cells}</div>'


def cta_band(path, title, text, primary=("Solicitar uma análise", "contato.html"),
             secondary=("Entender o processo", "como-funciona.html"), tone="ink",
             primary_opens_modal=None):
    """
    `primary_opens_modal`: por padrão, o CTA principal abre o popup de
    captação rápida quando aponta para /contato (é o caso de todas as
    chamadas "Solicitar uma análise" hoje). Passe False para manter a
    navegação normal, ou True para forçar o popup mesmo apontando para
    outro destino.
    """
    sec = f'{btn(secondary[0], secondary[1], path, "btn--line")}' if secondary else ""
    if primary_opens_modal is None:
        primary_opens_modal = (primary[1] == "contato.html")
    primary_attrs = " data-lead-modal" if primary_opens_modal else ""
    return f"""<section class="band band--{tone}">
      <div class="shell">
        <div class="ctaband" data-reveal>
          <div>
            <h2>{title}</h2>
            <p class="lead">{text}</p>
          </div>
          <div class="btn-row">{btn(primary[0], primary[1], path, attrs=primary_attrs)}{sec}</div>
        </div>
      </div>
    </section>"""


def pagehead(path, trail, eyebrow, title, lead=None, meta=None, variant=0, image_slot=None):
    """Topo de página interna: migalhas, título e trilho de dados objetivos.
    `image_slot`: chave em content.site.IMAGES — usa foto real quando o
    cliente fornecer o arquivo, e a arte SVG padrão enquanto não fornecer."""
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    meta_html = ""
    if meta:
        cells = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
        meta_html = f'<dl class="pagehead__meta">{cells}</dl>'
    fallback = "pagehead-" + str(variant % 3)
    # Sempre visível na primeira dobra (é o topo da página): carrega prioritário,
    # nunca lazy — lazy aqui atrasaria o LCP à toa, já que o navegador teria que
    # notar a imagem entrando na viewport antes de sequer começar a baixá-la.
    # A foto do topo ocupa a largura toda no celular e pouco menos da
    # metade no desktop (ver .pagehead__grid no CSS) — é o que o `sizes`
    # abaixo diz ao navegador, para ele baixar a variante certa em vez da
    # maior sempre (ver gerar_imagens.py e README, item 119).
    art_html = (photo_or_art(path, image_slot, fallback, eager="auto",
                             sizes="(min-width: 56rem) 46vw, 100vw") if image_slot
                else art_img(path, fallback, eager=True))
    return f"""<section class="pagehead">
  <div class="pagehead__grid">
    <div class="pagehead__inner">
      {crumbs(trail, path)}
      <span class="tag" style="display:block;margin-top:1.5rem;color:var(--iris-on-dark)">{eyebrow}</span>
      <h1>{title}</h1>
      {lead_html}{meta_html}
    </div>
    <div class="pagehead__media" aria-hidden="true">{art_html}</div>
  </div>
</section>"""


def netband(path, tag, title, lead, points, cta=None):
    """Faixa da rede: globo interativo com as seis praças reais da empresa.
    No mobile, o globo compacto entra entre a etiqueta (\"Rede\") e o título,
    ou seja, acima do texto do título/lead — no desktop ele continua sendo
    só o fundo da faixa inteira (ver .netband__globe--wide), então essa
    ordem no HTML não afeta a versão larga."""
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    pts = pointlist(points)
    cta_html = f'<div class="mt-3">{tlink(cta[0], cta[1], path)}</div>' if cta else ""
    return f"""<section class="band band--ink band--top-rule netband">
  <div class="shell netband__inner">
    <div class="netband__text">
      <div class="sechead" data-reveal>
        <span class="tag sechead__tag">{tag}</span>
        <div class="netband__globe netband__globe--compact" aria-hidden="true">
          <canvas id="acr-globe-compact"></canvas>
        </div>
        <h2>{title}</h2>
        {lead_html}
      </div>
      {pts}
      {cta_html}
    </div>
  </div>
  <div class="netband__globe netband__globe--wide" aria-hidden="true">
    <canvas id="acr-globe-wide"></canvas>
  </div>
  <div class="netband__veil" aria-hidden="true"></div>
  <script src="{rel(path, 'assets/js/globe.js')}" defer></script>
</section>"""


def partners_strip(path, items):
    """Esteira contínua (marquee) com as instituições da rede, para dar
    concretude ao número. Puramente decorativa e não-interativa: a lista
    real fica acessível a leitores de tela num parágrafo oculto, e a faixa
    animada é ocultada deles (a duplicação do conteúdo, necessária para o
    loop sem costura, faria a lista ser lida duas vezes). Vazia enquanto
    PARTNERS estiver vazio — sem placeholder no lugar.

    Cada item é {"name": ...} (texto simples, categoria genérica) ou
    {"name", "logo", "w", "h"} (mostra a marca em
    assets/img/partners/<logo>.webp; w/h são as dimensões reais do arquivo,
    para reservar o espaço certo e não empurrar o layout ao carregar)."""
    if not items:
        return ""

    def cell(it):
        if it.get("logo"):
            src = rel(path, f'assets/img/partners/{it["logo"]}.webp')
            # Sem loading="lazy" de propósito: a esteira já começa a se mover
            # assim que a página carrega, então "carregar só quando entrar na
            # tela" não poupa nada aqui (o item ia precisar da imagem em
            # segundos, não minutos) e ainda tem um efeito colateral real —
            # em teste, o navegador adiava o carregamento de algumas logos
            # por 10+ segundos, e elas apareciam "do nada" no meio do giro,
            # em vez de já estarem lá. O peso total das 12 é ~176 KB, então
            # carregar tudo de uma vez não pesa a página.
            # fetchpriority="low" (não "lazy"): começa a baixar já, junto com
            # o resto da página, mas sem disputar banda com o que é crítico
            # para a primeira dobra (fonte, hero). É o ponto certo entre "não
            # atrasa a animação" e "não atrapalha o que importa mais".
            return (f'<img class="partners__logo" src="{src}" '
                     f'width="{it["w"]}" height="{it["h"]}" alt="{it["name"]}" '
                     f'decoding="async" fetchpriority="low">')
        return f'<span class="partners__name">{it["name"]}</span>'

    row = "".join(cell(it) for it in items)
    sr_list = ", ".join(it["name"] for it in items)
    return f"""<div class="partners" data-reveal>
      <p class="sr">Entre as instituições da nossa rede: {sr_list}.</p>
      <div class="partners__track" aria-hidden="true">
        <div class="partners__row">{row}</div>
        <div class="partners__row">{row}</div>
      </div>
    </div>"""


DIAGRAM_ALT = {
    "flux": "Diagrama do descasamento entre prazos de pagamento e de recebimento",
    "elevation": "Elevação de imóvel indicando a margem liberável sob garantia",
    "chassis": "Perfil de veículo sob a curva de depreciação do ativo",
    "matrix": "Matriz de comparação entre instituições financeiras",
    "layers": "Camadas de uma operação estruturada",
    "grid": "Liberação escalonada de recursos ao longo da obra",
    "plan": "Planta de implantação com fase de expansão",
}


def pullquote(text, cite=None):
    """Citação de destaque: quebra blocos longos e fixa a ideia central da página."""
    c = f"<cite>{cite}</cite>" if cite else ""
    return f'<div class="pullquote"><p>{text}</p>{c}</div>'


def inline_diagram(kind, cls=""):
    """
    Diagrama embutido como SVG de verdade no HTML (não um <img src="…svg">),
    para poder animar as próprias peças com CSS assim que o diagrama entra
    na tela — reaproveita o observador de scroll já usado no resto do
    site (ver site.js e a seção 21 do site.css), então cada bloco entra e
    anima uma vez só, sem custo depois disso.
    """
    svg = art.diagram(kind)
    extra = f" {cls}" if cls else ""
    return f'<div class="diagram diagram--{kind}{extra}" data-reveal>{svg}</div>'


def figure(kind, path, caption=None):
    cap = f'<div class="figure__cap">{caption}</div>' if caption else ""
    img = inline_diagram(kind, "figure__art")
    return f'<figure class="figure">{img}{cap}</figure>'




# ------------------------------------------------------------------ cabeçalho
def mega_solucoes(path):
    links = "".join(
        f'<a class="megapanel__link" href="{rel(path, "solucoes/" + s["slug"] + ".html")}">'
        f'<strong>{s["title"]}</strong><span>{s["menu"]}</span></a>'
        for s in SOLUTIONS
    )
    return f"""<div class="megapanel">
      <div class="megapanel__grid">{links}</div>
      <div class="megapanel__foot">
        <p class="xs muted" style="margin:0;max-width:34ch">Não achou o formato da sua operação? A maioria delas é desenhada, não escolhida de um catálogo.</p>
        <div class="btn-row" style="flex-wrap:wrap">
          {btn("Ver todas as soluções", "solucoes.html", path, "btn--line btn--sm")}
          {btn("Simular BNDES, FGI, Pronampe e Procred 360", "programas.html", path, "btn--line btn--sm")}
        </div>
      </div>
    </div>"""


def mega_programas(path):
    # Cada item leva direto para a página isolada do programa
    # (programas/<slug>.html), não mais para a âncora da página de visão
    # geral: pedido do cliente, para quem já sabe qual programa quer ir
    # direto ao assunto, sem passar pela página com todos os programas
    # lado a lado. A visão geral com o simulador completo continua existindo
    # e é o link do rodapé do painel, logo abaixo.
    links = "".join(
        f'<a class="megapanel__link" href="{rel(path, "programas/" + p["slug"] + ".html")}">'
        f'<strong>{p["title"]}</strong><span>{p["menu"]}</span></a>'
        for p in PUBLIC_PROGRAMS
    )
    return f"""<div class="megapanel">
      <div class="megapanel__grid">{links}</div>
      <div class="megapanel__foot">
        <p class="xs muted" style="margin:0;max-width:34ch">Programas e mecanismos de garantia comparados lado a lado, com simulador de valor, taxa e parcela.</p>
        <div class="btn-row" style="flex-wrap:wrap">
          {btn("Ver todos os programas", "programas.html", path, "btn--line btn--sm")}
        </div>
      </div>
    </div>"""


_MEGA_PANELS = {"solucoes": mega_solucoes, "programas": mega_programas}


def masthead(path, over, nav_key):
    items = []
    for n in NAV:
        current = (n["href"] == nav_key)
        mega_kind = n.get("mega")
        if mega_kind:
            panel = _MEGA_PANELS[mega_kind](path)
            items.append(f"""<div class="nav__item{' is-current' if current else ''}" data-mega>
              <button class="nav__link" aria-expanded="false" aria-haspopup="true">{n['label']}
                <svg class="nav__chev" viewBox="0 0 10 6" fill="none" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.2"/></svg>
              </button>{panel}</div>""")
        else:
            aria = ' aria-current="page"' if current else ""
            items.append(f'<div class="nav__item"><a class="nav__link" href="{rel(path, n["href"])}"{aria}>{n["label"]}</a></div>')

    # Sempre sólido (pedido do cliente): o cabeçalho é fixo e precisa ficar
    # legível o tempo todo, inclusive rolado por cima do conteúdo claro das
    # páginas — a variante transparente (`masthead--over`, pensada pra ficar
    # só sobre a arte escura do topo) ficava com o texto branco quase
    # invisível assim que passava a rolar sobre um fundo claro. `over` segue
    # recebido pelas páginas (ver `content/*.py`) mas não é mais usado aqui.
    cls = "masthead masthead--solid"
    return f"""<header class="{cls}">
  <div class="shell masthead__inner">
    <button class="burger" aria-expanded="false" aria-controls="drawer" aria-label="Abrir menu">
      <span class="burger__bars" aria-hidden="true"><i></i><i></i><i></i></span>
    </button>
    <a class="brand" href="{rel(path, 'index.html')}" aria-label="Acrópole Capital, página inicial">
      {brand_mark()}
    </a>
    <nav class="nav" aria-label="Navegação principal">
      {''.join(items)}
      <span class="nav__cta">{btn("Solicitar análise", "contato.html", path, "btn--line btn--sm", attrs=' data-lead-modal')}</span>
    </nav>
  </div>
</header>"""


def drawer(path):
    sols_sub = ('<a href="' + rel(path, 'solucoes.html') + '">Visão geral</a>' + "".join(
        f'<a href="{rel(path, "solucoes/" + s["slug"] + ".html")}">{s["title"]}</a>' for s in SOLUTIONS
    ))
    # Mesma mudança do painel do menu desktop (ver mega_programas): vai
    # direto para a página isolada do programa, não para a âncora.
    progs_sub = "".join(
        f'<a href="{rel(path, "programas/" + p["slug"] + ".html")}">{p["title"]}</a>' for p in PUBLIC_PROGRAMS
    )
    # Contagem no selo (o "7" fixo daqui saiu de sincronia com as 8 soluções
    # reais em algum momento — agora vem do tamanho de cada lista, pra não
    # desatualizar de novo se um item for adicionado ou removido).
    _drawer_subs = {"solucoes": (sols_sub, len(SOLUTIONS), "drawer-sol"),
                     "programas": (progs_sub, len(PUBLIC_PROGRAMS), "drawer-prog")}
    links = []
    for n in NAV:
        mega_kind = n.get("mega")
        if mega_kind:
            sub_html, count, sub_id = _drawer_subs[mega_kind]
            links.append(f"""<button class="drawer__link" data-drawer-toggle aria-expanded="false" aria-controls="{sub_id}">
              {n['label']}<span class="tag">{count}</span></button>
              <div class="drawer__sub" id="{sub_id}" data-open="false">{sub_html}</div>""")
        else:
            links.append(f'<a class="drawer__link" href="{rel(path, n["href"])}">{n["label"]}</a>')

    return f"""<div class="drawer" id="drawer" data-open="false" aria-hidden="true" inert>
  <div class="drawer__scrim" data-drawer-close></div>
  <div class="drawer__panel">
    <div class="shell">
      <div class="drawer__head">
        {brand_mark()}
        <span class="sr">Acrópole Capital</span>
        <button class="burger" data-drawer-close aria-expanded="true" aria-label="Fechar menu" style="margin-left:auto">
          <span class="burger__bars" aria-hidden="true"><i></i><i></i><i></i></span>
        </button>
      </div>
      <nav class="drawer__body" aria-label="Navegação principal, versão compacta">
        {''.join(links)}
        <div class="drawer__foot">
          {btn("Solicitar uma análise", "contato.html", path, attrs=' data-lead-modal')}
          <p class="drawer__meta">{drawer_meta()}</p>
        </div>
      </nav>
    </div>
  </div>
</div>"""


LINKEDIN_SVG = ('<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.5 1.5a1.5 1.5 0 '
                '100 3 1.5 1.5 0 000-3zM2.2 6h2.6v8H2.2V6zm4.4 0h2.5v1.1c.35-.66 1.2-1.35 2.47-1.35 2.64 0 '
                '3.13 1.74 3.13 4V14h-2.6V10.2c0-.9-.02-2.06-1.25-2.06-1.26 0-1.45.98-1.45 2v3.86H6.6V6z"/></svg>')
INSTAGRAM_SVG = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">'
                 '<rect x="2" y="2" width="12" height="12" rx="3.4"/><circle cx="8" cy="8" r="2.9"/>'
                 '<circle cx="11.8" cy="4.2" r=".8" fill="currentColor" stroke="none"/></svg>')
YOUTUBE_SVG = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">'
               '<rect x="1.4" y="3.6" width="13.2" height="8.8" rx="2.8"/>'
               '<path d="M6.6 6.4 10 8l-3.4 1.6V6.4Z" fill="currentColor" stroke="none"/></svg>')


def extra_contacts():
    """Endereço e horário só entram no rodapé quando existem."""
    out = []
    for v in (SITE["address"], SITE["hours"]):
        if not is_placeholder(v):
            out.append(f'<li><span class="xs" style="color:var(--slate-1)">{v}</span></li>')
    return "".join(out)


def rating_block():
    """
    Nota média que a Acrópole apurou a partir do retorno direto de clientes
    (cartas e mensagens de WhatsApp), não de uma plataforma pública de
    avaliações — por isso o rótulo é explícito sobre a origem, em vez de
    imitar o selo de um serviço de terceiros que não existe aqui.
    """
    star = ('<svg viewBox="0 0 16 16" aria-hidden="true">'
            '<path d="M8 1.2l2.1 4.4 4.8.6-3.5 3.3.9 4.8L8 11.9l-4.3 2.4.9-4.8L1.1 6.2l4.8-.6z"/></svg>')
    return f"""<div class="foot__rating" role="img" aria-label="Nota média 4,9 de 5 entre os clientes atendidos">
      <span class="foot__rating-stars" aria-hidden="true">{star * 5}</span>
      <strong class="foot__rating-score" aria-hidden="true">4,9</strong>
    </div>"""


def seal_block(path):
    """Selo RA1000 (Reclame Aqui). Só exibido como imagem estática, sem link,
    já que ainda não há um perfil RA configurado em SITE."""
    return f"""<div class="foot__seal">
      <img src="{rel(path, 'assets/img/ra1000.svg')}" width="79" height="40" loading="lazy" alt="Selo RA1000 do Reclame Aqui">
    </div>"""


def dev_credit_block(path):
    """'Site desenvolvido por' no rodapé: crédito de quem fez o site, com o
    logo como link. O clique abre o WhatsApp já com uma mensagem pronta
    (SITE['whatsapp_dev_href'], ver WHATSAPP_DEV_MSG em content/site.py),
    voltada a quem tem interesse em contratar um site parecido para a
    própria empresa — não é o mesmo link/mensagem usado para captar leads
    de capital de giro no resto do site.
    """
    if is_placeholder(SITE.get("whatsapp_dev_href")):
        return ""
    return f"""<div class="foot__devcredit">
      <span>Site desenvolvido por</span>
      <a href="{SITE['whatsapp_dev_href']}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp sobre desenvolvimento de sites">
        <img src="{rel(path, 'assets/img/dev-credit-logo.svg')}" width="21" height="22" loading="lazy" alt="">
      </a>
    </div>"""


def social_block():
    """Só publica o ícone quando existe URL real. Placeholder não vira link."""
    out = []
    for url, name, svg in ((SITE["linkedin"], "LinkedIn", LINKEDIN_SVG),
                           (SITE["instagram"], "Instagram", INSTAGRAM_SVG),
                           (SITE["youtube"], "YouTube", YOUTUBE_SVG)):
        if is_placeholder(url):
            continue
        out.append(f'<a href="{url}" aria-label="{name} da Acrópole Capital">{svg}</a>')
    if not out:
        return ('<p class="xs" style="margin-top:1.5rem;color:var(--graphite)">'
                'Perfis sociais: [definir URLs antes da publicação]</p>')
    return '<div class="foot__social">' + "".join(out) + "</div>"


def drawer_meta():
    parts = []
    if not is_placeholder(SITE["email"]):
        parts.append(mail_link())
    if not is_placeholder(SITE["phone_label"]):
        parts.append(clink(SITE["phone_label"], SITE["phone_href"]))
    if not is_placeholder(SITE["hours"]):
        parts.append(SITE["hours"])
    return "<br>".join(parts) if parts else "Contatos em atualização"


def footer(path):
    sol_links = "".join(
        f'<li><a href="{rel(path, "solucoes/" + s["slug"] + ".html")}">{s["title"]}</a></li>' for s in SOLUTIONS
    )
    inst = [("Sobre a Acrópole", "sobre.html"), ("Como funciona", "como-funciona.html"),
            ("Diagnóstico rápido", "diagnostico.html"),
            ("Calculadora de capital de giro", "calculadora-capital-de-giro.html"),
            ("Programas públicos de crédito", "programas.html"),
            # Landing de campanha do Pronampe 2026 (ver content/pronampe.py):
            # antes só era alcançável por um link dentro de um artigo do
            # blog — pedido do cliente, para aparecer também no rodapé.
            ("Pronampe 2026", "pronampe-2026.html"),
            ("Para empresas", "empresas.html"), ("Para investidores", "investidores.html"),
            ("Para o agronegócio", "agronegocio.html"),
            ("Conteúdos", "conteudos.html"), ("Governança", "governanca.html")]
    inst_links = "".join(f'<li><a href="{rel(path, h)}">{l}</a></li>' for l, h in inst)

    return f"""<footer class="foot">
  <div class="shell">
    <div class="foot__top">
      <div class="foot__brand">
        <a class="brand" href="{rel(path, 'index.html')}" style="color:var(--paper)" aria-label="Acrópole Capital, página inicial">
          {brand_mark()}
        </a>
        <p>{SITE['tagline']}</p>
        <p class="foot__disclaimer">{LEGAL_LINE}</p>
      </div>
      <div><h3>Soluções</h3><ul>{sol_links}</ul></div>
      <div><h3>Institucional</h3><ul>{inst_links}</ul></div>
      <div>
        <h3>Contato</h3>
        <ul>
          <li>{clink(SITE['whatsapp_label'], SITE['whatsapp_href'], pendente=PENDENTE['whatsapp_label'], attrs=' data-lead-modal')}</li>
          <li>{mail_link()}</li>
          {extra_contacts()}
        </ul>
        {social_block()}
        {rating_block()}
        <div class="foot__seal-row">
          {seal_block(path)}
          {dev_credit_block(path)}
        </div>
      </div>
    </div>
    <div class="foot__legal">
      <p class="foot__fine">© <span data-year>2026</span> Acrópole Capital. Todos os direitos reservados. CNPJ {SITE['cnpj']}.</p>
      <nav aria-label="Links legais">
        <a href="{rel(path, 'politica-de-privacidade.html')}">Política de Privacidade</a>
        <a href="{rel(path, 'termos-de-uso.html')}">Termos de Uso</a>
        <a href="{rel(path, 'avisos-legais.html')}">Avisos legais</a>
      </nav>
    </div>
  </div>
</footer>
<a class="rail" href="{rel(path, 'contato.html') if is_placeholder(SITE['whatsapp_href']) else SITE['whatsapp_href']}" data-show="false"{'' if is_placeholder(SITE['whatsapp_href']) else ' data-lead-modal'} aria-label="Falar com um especialista">
  <picture>
    <source type="image/avif" srcset="{rel(path, 'assets/img/rail/foto-lucas.avif')}">
    <source type="image/webp" srcset="{rel(path, 'assets/img/rail/foto-lucas.webp')}">
    <img src="{rel(path, 'assets/img/rail/foto-lucas.png')}" width="208" height="208" decoding="async" loading="lazy" alt="">
  </picture>
</a>"""


# ------------------------------------------------------------ popup de captação
def _lm_field(id_, name, label, kind="text", placeholder="", hint=None, mask=None,
              validate=None, required=True, err="Preencha este campo.", full=False):
    described = " ".join(x for x in [f"{id_}-hint" if hint else None, f"{id_}-err"] if x)
    attrs = f'type="{kind}" id="{id_}" name="{name}" aria-describedby="{described}"'
    if placeholder:
        attrs += f' placeholder="{placeholder}"'
    if mask:
        attrs += f' data-mask="{mask}"'
    if validate:
        attrs += f' data-validate="{validate}"'
    if required:
        attrs += " required"
    if kind == "tel":
        attrs += ' inputmode="numeric"'
    hint_html = f'<span class="hint" id="{id_}-hint">{hint}</span>' if hint else ""
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{id_}">{label}</label>
      <input {attrs}>
      {hint_html}
      <span class="field__err" id="{id_}-err">{err}</span>
    </div>"""


def _lm_select(id_, name, label, options, hint=None, required=False, full=False):
    opts = "".join(f'<option value="{o}">{o}</option>' for o in options)
    hint_html = f'<span class="hint" id="{id_}-hint">{hint}</span>' if hint else ""
    req = " required" if required else ""
    described = " ".join(x for x in [f"{id_}-hint" if hint else None, f"{id_}-err"] if x)
    aria = f' aria-describedby="{described}"'
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{id_}">{label}</label>
      <select id="{id_}" name="{name}"{req}{aria}>
        <option value="">Selecione</option>{opts}
      </select>
      {hint_html}
      <span class="field__err" id="{id_}-err">Selecione uma opção para continuar.</span>
    </div>"""


def cookie_bar(path):
    """
    Aviso de cookies (pedido do cliente): uma caixinha discreta no canto
    inferior direito, mostrada uma vez na primeira visita, com um botão só
    ("Aceitar") — sem gerenciamento granular de categorias.

    Atualização (ver README, item sobre webhook + tracking_params): o
    site passou a gravar um cookie próprio de atribuição
    (`app_attribution`, 30 dias — origem de campanha/UTM, não analytics
    de terceiro) e a enviar de verdade os formulários a um webhook (ver
    `config.js`). O aviso genérico abaixo, apoiado na Política de
    Privacidade (que já cobria "cookies e ferramentas de análise" de
    forma abrangente antes disso existir de fato), continua válido —
    mas se a Acrópole também ligar analytics/pixel de terceiro de
    verdade no futuro, vale revisitar isso para um modelo de
    consentimento por categoria. Por ora, o pedido era só o aviso com
    um OK, pequeno e discreto (não uma barra ocupando a linha inteira —
    pedido explícito, ver item 165 do README), e é isso que existe.

    A escolha fica em localStorage (site.js, `cookieconsent:v1`), então a
    caixinha não aparece de novo nas próximas visitas depois que a pessoa
    aceitar. Sem JS (localStorage indisponível ou bloqueado), ela nem
    chega a aparecer — silenciosamente, para nunca cobrir conteúdo em
    quem tem JS desligado.
    """
    return f"""<div class="cookiebar" id="cookiebar" data-show="false" role="region" aria-label="Aviso de cookies">
  <p>Usamos cookies para melhorar sua experiência. Ao continuar, você concorda com nossa <a href="{rel(path, 'politica-de-privacidade.html')}">Política de Privacidade</a>.</p>
  <div class="cookiebar__actions">
    <button type="button" class="btn btn--line btn--sm" data-cookie-accept>Aceitar</button>
  </div>
</div>"""


def lead_modal(path, lead_context=None):
    """
    Popup de captação rápida. Os CTAs de "Solicitar uma análise" e os links
    diretos de WhatsApp (cabeçalho, gaveta, rodapé, trilho flutuante,
    faixas de chamada e a página de contato) abrem este popup em vez de
    navegar direto — o JS intercepta o clique (ver `[data-lead-modal]` em
    site.js). Pede só o essencial para o especialista entender o caso antes
    de ligar. Ao enviar, não redireciona para lugar nenhum: mostra
    agradecimento no próprio popup e a pessoa fecha e continua navegando.

    Reaproveita a mesma engrenagem do formulário de /contato — máscara
    (`data-mask`), validação (`data-validate`, `.field[data-invalid]`) e
    envio (`form[data-endpoint-form]`, que respeita `ACROPOLE_CONFIG.endpoint`
    e cai em modo demonstração quando ele está vazio). Ao enviar com sucesso,
    `data-whatsapp-redirect` (ver site.js) leva a pessoa para o WhatsApp com
    uma mensagem pronta, alguns instantes depois de mostrar a confirmação no
    próprio popup — nada de lógica nova em JS além de abrir/fechar o popup e
    desse redirecionamento.

    `lead_context`: dict opcional (ex.: {"category": "Capital de giro",
    "topic": "necessidade-de-capital-de-giro"}) que a página de origem passa
    via `page["lead_context"]`. Vira campo oculto no formulário, além do
    `payload.page` que o site.js já anexa a toda submissão (endereço da
    página). Existe para o CRM não depender de reconstruir a categoria a
    partir da URL: a origem do lead (artigo e categoria) já chega pronta.
    Nenhuma integração real é feita aqui — só o campo, pronto para ser lido
    do lado do CRM.
    """
    hidden_context = "".join(
        f'<input type="hidden" name="lead_{k}" value="{esc(str(v))}">'
        for k, v in (lead_context or {}).items()
    )
    return f"""<div class="leadmodal" id="lead-modal" data-open="false" aria-hidden="true">
  <div class="leadmodal__overlay" data-lead-close></div>
  <div class="leadmodal__dialog" role="dialog" aria-modal="true" aria-labelledby="lead-modal-title">
    <button type="button" class="leadmodal__close" data-lead-close aria-label="Fechar">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13"/></svg>
    </button>
    <div class="leadmodal__body">
      <h2 id="lead-modal-title" class="leadmodal__title">O capital que vai destravar o próximo passo da sua empresa.</h2>
      <p class="muted small mb-2" style="max-width:44ch">100% alinhado com o crescimento do seu negócio.</p>

      <form class="form" data-endpoint-form data-whatsapp-redirect="{SITE['whatsapp_lead_href']}" novalidate>
        {hidden_context}
        <div class="fgrid fgrid--2">
          {_lm_field("lm-nome", "nome", "Nome completo", err="Informe seu nome completo.")}
          {_lm_field("lm-telefone", "telefone", "Telefone ou WhatsApp", kind="tel",
                     placeholder="(00) 00000-0000", mask="phone", validate="phone",
                     err="Informe um número com DDD.")}
          {_lm_field("lm-email", "email", "E-mail", kind="email", placeholder="nome@empresa.com.br",
                     validate="email", err="Informe um e-mail válido.")}
          {_lm_field("lm-empresa", "empresa", "Nome da empresa", err="Informe o nome da empresa.")}
          {_lm_select("lm-cargo", "cargo", "Cargo", CARGOS, required=True)}
          {_lm_select("lm-porte", "porte", "Porte da empresa", PORTES, required=True)}
          {_lm_select("lm-faturamento", "faturamento", "Qual o faturamento anual da sua empresa?",
                     FATURAMENTOS, required=True, full=True)}
        </div>

        <div class="hp" aria-hidden="true">
          <label for="lm-company">Não preencha este campo</label>
          <input type="text" id="lm-company" name="company_website" tabindex="-1" autocomplete="off">
        </div>

        <input type="hidden" name="tracking_params" value="">

        <label class="consent mt-2">
          <input type="checkbox" name="consentimento" required>
          <span>Autorizo o contato da Acrópole Capital para tratar desta solicitação, conforme a <a href="{rel(path, 'politica-de-privacidade.html')}">Política de Privacidade</a>. O envio não representa solicitação formal de crédito nem aprovação.</span>
          <span class="consent__err">Marque a caixa acima pra continuar.</span>
        </label>

        <div class="formfoot">
          <div class="btn-row">
            <button type="submit" class="btn" data-step-submit>
              <span class="spinner" aria-hidden="true"></span>Enviar
            </button>
          </div>
        </div>

        <div class="formstate formstate--ok" role="status">
          <span class="formstate__icon" aria-hidden="true">{_ICON_CHECK_CIRCLE}</span>
          <div>
            <strong>Recebemos suas informações.</strong> Você será direcionado ao WhatsApp em instantes para continuar a conversa com um consultor.
            <div class="mt-2 leadmodal__okactions">
              <a class="tlink" href="{SITE['whatsapp_lead_href']}" target="_blank" rel="noopener">Ir para o WhatsApp agora</a>
              <span class="leadmodal__okdot" aria-hidden="true">·</span>
              <button type="button" class="tlink" data-lead-close>Fechar e continuar navegando</button>
            </div>
          </div>
        </div>
        <div class="formstate formstate--err" role="alert">
          <span class="formstate__icon" aria-hidden="true">{_ICON_ALERT_CIRCLE}</span>
          <div><strong>O envio não foi concluído.</strong> Tente novamente em alguns instantes, ou fale direto pelo WhatsApp no rodapé desta página.</div>
        </div>
      </form>
    </div>
  </div>
</div>"""


# ------------------------------------------------------------------ documento
def font_head(path):
    """Fontes locais, as 2 pré-carregadas.

    São exatamente 2 arquivos (Inter variável + Manrope 700, ver
    fonts.css), e os 2 são usados acima da dobra em toda página: o corpo do
    texto na Inter e o h1 na Manrope. Pré-carregar os dois foi a mudança
    que mais moveu o ponteiro na auditoria de performance (README, item
    119): sem o preload, o navegador só descobre a fonte depois de baixar e
    interpretar o fonts.css, e o texto pinta na fonte do sistema para
    trocar depois — o que empurrava o LCP em quase um segundo no
    Lighthouse.
    """
    pre = "".join(
        f'<link rel="preload" as="font" type="font/woff2" crossorigin '
        f'href="{rel(path, "assets/fonts/" + f)}.woff2">'
        for f in ("inter-var", "manrope-700")
    )
    # O @font-face vai INLINE, não como arquivo: fonts.css tem ~1 KB, e como
    # arquivo custava uma ida e volta inteira à rede bem no caminho crítico
    # — o navegador só sabe qual fonte aplicar depois que ele chega, então o
    # texto ficava esperando por 1 KB. Inline, a regra já está no HTML e as
    # fontes (pré-carregadas acima) são aplicadas assim que chegam. Medido:
    # o LCP da página de Conteúdos caiu de 2,0s para 1,5s só com isso
    # (README, item 119). O arquivo continua existindo em static/ e em
    # dist/ — é ele que o pacote navegável e esta função leem.
    css = _font_css_min().replace("../fonts/", rel(path, "assets/fonts/"))
    return pre + f"<style>{css}</style>"


@functools.lru_cache(maxsize=8)
def _read_static(rel_path):
    """Lê um arquivo de static/ uma única vez por build (a mesma folha de
    fontes é embutida em 58 páginas)."""
    with open(os.path.join(ROOT, "static", *rel_path.split("/")), encoding="utf-8") as f:
        return f.read()


@functools.lru_cache(maxsize=1)
def _font_css_min():
    """fonts.css sem comentários. Ele é dos arquivos mais comentados do
    projeto (a explicação de por que são 2 fontes, e não 10), e esse texto
    todo iria embutido em cada uma das 58 páginas. O arquivo em static/ e em
    dist/ continua comentado — só a cópia embutida é enxugada."""
    css = _read_static("assets/css/fonts.css")
    return rcssmin.cssmin(css) if HAVE_MINIFIERS else css


def head_common(page, path, url, title, desc, schema_html, stylesheet, early_script=""):
    """Cabeçalho comum às duas formas de página (site e campanha isolada).

    O <head> é idêntico nas duas — mesmos metadados, mesmo compartilhamento,
    mesmos ícones, mesmas fontes locais: o que muda é só a folha de estilo
    (o site inteiro usa site.css; a landing de campanha usa a sua própria,
    ver document()).
    """
    # Página que não deve ser indexada (hoje só o 404): sem canonical —
    # apontar o canonical de uma página de erro para uma URL que não
    # existe de verdade e não está no sitemap é pior que não ter
    # canonical nenhum — e robots=noindex, já que ela pode ser servida
    # sob qualquer caminho inválido, não é conteúdo que deva competir por
    # posição de busca.
    noindex = page.get("noindex", False)
    canonical_tag = "" if noindex else f'<link rel="canonical" href="{url}">\n'
    robots_tag = ('<meta name="robots" content="noindex, follow">' if noindex
                  else '<meta name="robots" content="index, follow, max-image-preview:large">')
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{early_script}<title>{title}</title>
<meta name="description" content="{desc}">
{canonical_tag}{robots_tag}
<meta name="theme-color" content="{page.get('theme_color', '#030b12')}">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="Acrópole Capital">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['domain']}/assets/social/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Acrópole Capital: assessoria e estruturação de crédito">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE['domain']}/assets/social/og-image.jpg">
<link rel="icon" href="{rel(path, 'assets/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{rel(path, 'assets/icons/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="icon" href="{rel(path, 'assets/icons/favicon-16.png')}" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="{rel(path, 'assets/icons/apple-touch-icon.png')}">
<link rel="manifest" href="{rel(path, 'site.webmanifest')}">
{font_head(path)}
<link rel="stylesheet" href="{rel(path, stylesheet)}">
{schema_html}"""


def document(page):
    path = page["path"]
    url = SITE["domain"] + clean_url(path)
    desc = esc(page["desc"])
    title = esc(page["title"])
    schema = page.get("schema") or []
    schema_html = "".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{head_common(page, path, url, title, desc, schema_html, 'assets/css/site.css',
             early_script=f'<script>{REVEAL_DETECT_JS}</script>' + chr(10))}
</head>
<body>
{logo_sprite()}
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
{masthead(path, page.get("over", False), page.get("nav_key"))}
{drawer(path)}
<main id="conteudo">
{page["body"]}
</main>
{footer(path)}
{lead_modal(path, page.get("lead_context"))}
{cookie_bar(path)}
<script src="{rel(path, 'assets/js/config.js')}" defer></script>
<script src="{rel(path, 'assets/js/site.js')}" defer></script>
</body>
</html>"""


# ------------------------------------------------------------------ schema
def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FinancialService",
        "name": "Acrópole Capital",
        "url": SITE["domain"],
        "description": SITE["tagline"],
        "areaServed": "BR",
        "taxID": SITE["cnpj"],
        "knowsAbout": [s["title"] for s in SOLUTIONS],
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label,
             "item": SITE["domain"] + (clean_url(href) if href else "")}
            for i, (label, href) in enumerate(items)
        ],
    }


def faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer",
                                "text": " ".join(a) if isinstance(a, list) else a}}
            for q, a in items
        ],
    }


# ------------------------------------------------------------------ escrita
def write(page):
    out = os.path.join(DIST, page["path"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(document(page))


def minify_js(js):
    """
    Minifica um bloco JS. Com o binário `terser` disponível (npm install -g
    terser), faz *mangling* de verdade: renomeia variável e função locais
    para identificador curto (a, b, c...) e remove código morto — é isso
    que transforma `function acrGiroInit()` em algo como `function n(){`.
    Sem terser, cai pro rjsmin (sempre presente se HAVE_MINIFIERS): só tira
    espaço e comentário, sem renomear nada. Qualquer falha do terser (binário
    quebrado, JS que ele não consiga parsear) também cai pro rjsmin em vez de
    quebrar o build — minificação nunca pode ser motivo de build vermelho.

    --mangle sem --mangle-props: só nomes de variável/função somem, nunca
    nome de propriedade de objeto (`window.ACROPOLE_CONFIG.endpoint`, os
    `data-*` lidos via dataset, etc.) — mangling de propriedade exigiria
    mapear cada acesso por string (`obj['endpoint']`) no projeto inteiro pra
    não quebrar nada, risco alto para um site que não guarda segredo nenhum
    atrás dessas chaves.
    """
    if TERSER_BIN:
        try:
            r = subprocess.run(
                [TERSER_BIN, "--compress", "--mangle", "--toplevel"],
                input=js, capture_output=True, text=True, timeout=30,
            )
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout
        except (OSError, subprocess.SubprocessError):
            pass
    return rjsmin.jsmin(js) if HAVE_MINIFIERS else js


def minify_assets(dist):
    """
    Minifica CSS e JS só na cópia de saída (dist/) — os fontes em static/
    continuam legíveis e comentados para edição. Passo opcional: sem
    rjsmin/rcssmin instalados (pip install rjsmin rcssmin), o build segue
    normalmente com os arquivos como estão, só um pouco mais pesados.

    Cobre 3 lugares, não só o site.css/site.js externos: config.js (ficava de
    fora antes, indo pro ar com comentário e tudo) e todo <script> inline que
    o build injeta por página (calculadora de giro, questionário do
    diagnóstico, globo, kanban) — esses últimos eram publicados como
    texto-fonte puro, legível e comentado, dentro do próprio HTML. Precisa
    rodar antes de harden_csp(): o hash SHA-256 da CSP tem que bater com o
    byte final publicado, não com a fonte não minificada.
    """
    if not HAVE_MINIFIERS:
        print("Aviso: rjsmin/rcssmin não instalados — CSS/JS não foram minificados "
              "(pip install rjsmin rcssmin para ativar).")
        return
    print(("Minificando com terser (mangling de identificador ativo)."
           if TERSER_BIN else
           "Aviso: terser não encontrado no PATH — JS minificado sem mangling de "
           "identificador (npm install -g terser para ativar).")
    )
    for css_name in ("site.css",):
        css_path = os.path.join(dist, "assets", "css", css_name)
        if not os.path.exists(css_path):
            continue
        css = open(css_path, encoding="utf-8").read()
        css = rcssmin.cssmin(css)
        if CSSO_BIN:
            try:
                r = subprocess.run([CSSO_BIN], input=css, capture_output=True,
                                    text=True, timeout=30)
                if r.returncode == 0 and r.stdout.strip():
                    css = r.stdout
            except (OSError, subprocess.SubprocessError):
                pass
        open(css_path, "w", encoding="utf-8").write(css)

    for name in ("site.js", "config.js", "globe.js"):
        js_path = os.path.join(dist, "assets", "js", name)
        if os.path.exists(js_path):
            js = open(js_path, encoding="utf-8").read()
            open(js_path, "w", encoding="utf-8").write(minify_js(js))

    for root, _, names in os.walk(dist):
        for n in names:
            if not n.endswith(".html"):
                continue
            path = os.path.join(root, n)
            raw = open(path, encoding="utf-8").read()

            def _shrink(m):
                return m.group(0)[:m.start(1) - m.start(0)] + minify_js(m.group(1)) + "</script>"

            patched = INLINE_SCRIPT_RE.sub(_shrink, raw)
            if patched != raw:
                open(path, "w", encoding="utf-8").write(patched)


INLINE_SCRIPT_RE = re.compile(
    r'<script(?![^>]*\bsrc=)(?![^>]*type="application/ld\+json")[^>]*>([\s\S]*?)</script>',
    re.IGNORECASE,
)


def harden_csp(dist):
    """
    A CSP publicada (script-src 'self') bloquearia, no navegador, os poucos
    blocos <script> que o site injeta inline (o script de revelação no
    <head>, o globo da rede, o simulador de programas e o questionário do
    diagnóstico) — eles não têm origem 'self' nem 'unsafe-inline' liberado.
    Em vez de enfraquecer a política com 'unsafe-inline' (que passaria a
    aceitar QUALQUER script injetado, inclusive por um ataque de XSS),
    cada bloco inline realmente publicado tem seu hash SHA-256 calculado
    aqui e adicionado à allowlist: só o conteúdo exato gerado pelo build
    roda, e nada mais. <script type="application/ld+json"> não entra nessa
    varredura porque não é executável — CSP script-src não se aplica a ele.
    """
    hashes = set()
    for root, _, names in os.walk(dist):
        for n in names:
            if not n.endswith(".html"):
                continue
            raw = open(os.path.join(root, n), encoding="utf-8").read()
            for m in INLINE_SCRIPT_RE.finditer(raw):
                digest = hashlib.sha256(m.group(1).encode("utf-8")).digest()
                hashes.add("'sha256-" + base64.b64encode(digest).decode("ascii") + "'")
    if not hashes:
        return
    allow = " ".join(sorted(hashes))

    def patch_script_src(csp):
        return re.sub(r"script-src 'self'", "script-src 'self' " + allow, csp)

    # Cada `if os.path.exists` abaixo, se o arquivo existir mas o padrão não
    # bater (_headers reformatado, vercel.json sem esse bloco), silenciosamente
    # não fazia nada: o build "passava" normal e publicava uma CSP sem os
    # hashes, quebrando todo script inline do site em produção sem nenhum
    # aviso aqui. Cada ramo agora levanta se o arquivo existe mas o hash não
    # foi aplicado, em vez de deixar essa falha só aparecer no navegador do
    # visitante.
    headers_path = os.path.join(dist, "_headers")
    if os.path.exists(headers_path):
        text = open(headers_path, encoding="utf-8").read()
        text, n = re.subn(
            r"(Content-Security-Policy: .*)$", lambda m: patch_script_src(m.group(1)),
            text, count=1, flags=re.MULTILINE,
        )
        if n == 0:
            raise RuntimeError(
                f"harden_csp: nenhuma linha 'Content-Security-Policy:' encontrada em {headers_path} "
                "— a CSP publicada ficaria sem os hashes dos scripts inline."
            )
        open(headers_path, "w", encoding="utf-8").write(text)

    vercel_path = os.path.join(dist, "vercel.json")
    if os.path.exists(vercel_path):
        conf = json.load(open(vercel_path, encoding="utf-8"))
        patched = False
        for block in conf.get("headers", []):
            for h in block.get("headers", []):
                if h.get("key") == "Content-Security-Policy":
                    h["value"] = patch_script_src(h["value"])
                    patched = True
        if not patched:
            raise RuntimeError(
                f"harden_csp: nenhum header 'Content-Security-Policy' encontrado em {vercel_path} "
                "— a CSP publicada ficaria sem os hashes dos scripts inline."
            )
        with open(vercel_path, "w", encoding="utf-8") as f:
            json.dump(conf, f, indent=2, ensure_ascii=False)
            f.write("\n")


def write_htaccess(dist):
    """
    Gera dist/.htaccess a partir do vercel.json já finalizado (depois de
    harden_csp, pra levar os hashes de script inline junto), pra hospedagem
    Apache/LiteSpeed (ex.: Hostinger compartilhada) ter a mesma paridade de
    headers de segurança e cache que a Vercel já tem — sem esse arquivo, a
    CSP, HSTS e as regras de cache simplesmente não existiriam num host
    Apache, silenciosamente, sem nenhum aviso no navegador além da ausência.

    Só lê o vercel.json como fonte única de verdade (nunca redigita a CSP
    aqui) — assim os dois hosts nunca podem divergir por esquecimento.
    """
    vercel_path = os.path.join(dist, "vercel.json")
    if not os.path.exists(vercel_path):
        raise RuntimeError("write_htaccess: vercel.json não encontrado — rode depois de harden_csp().")
    conf = json.load(open(vercel_path, encoding="utf-8"))

    main_headers = None
    for block in conf.get("headers", []):
        if block.get("source") == "/(.*)":
            main_headers = block["headers"]
            break
    if not main_headers:
        raise RuntimeError("write_htaccess: bloco de headers globais ('/(.*)') não encontrado em vercel.json.")

    lines = [
        "# Gerado automaticamente por build.py (write_htaccess) a partir de vercel.json.",
        "# Não editar à mão — rode `python3 build.py` de novo depois de mudar vercel.json.",
        "",
        "# Nunca listar o conteúdo de uma pasta sem index.",
        "Options -Indexes",
        "",
        "# Nega acesso via navegador a qualquer arquivo de config local com segredo",
        "# (ex.: api/config.local.php, api/db.local.php) — defesa em profundidade,",
        "# mesmo que o PHP em si já não vaze o conteúdo se for executado normalmente.",
        '<FilesMatch "(^|\\.)env$|\\.local\\.php$|\\.log$">',
        "  <IfModule mod_authz_core.c>",
        "    Require all denied",
        "  </IfModule>",
        "  <IfModule !mod_authz_core.c>",
        "    Order allow,deny",
        "    Deny from all",
        "  </IfModule>",
        "</FilesMatch>",
        "",
        "<IfModule mod_headers.c>",
    ]
    for h in main_headers:
        value = h["value"].replace('"', '\\"')
        lines.append(f'  Header always set "{h["key"]}" "{value}"')
    lines += [
        "</IfModule>",
        "",
        "ErrorDocument 404 /404.html",
        "",
        "# HTTPS forçado (a maioria dos hosts já força por padrão, mas sem custo garantir aqui também).",
        "<IfModule mod_rewrite.c>",
        "  RewriteEngine On",
        "  RewriteCond %{HTTPS} off",
        "  RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]",
        "",
        "  # URL limpa (ex.: /contato também serve contato.html) — os links do",
        "  # próprio site já incluem .html, isso é só um bônus pra quem digita",
        "  # a URL sem extensão direto no navegador.",
        "  RewriteCond %{REQUEST_FILENAME} !-f",
        "  RewriteCond %{REQUEST_FILENAME} !-d",
        "  RewriteCond %{REQUEST_FILENAME}\\.html -f",
        "  RewriteRule ^(.*)$ $1.html [L]",
        "</IfModule>",
        "",
        "<IfModule mod_headers.c>",
        '  <FilesMatch "\\.(css|js)$">',
        '    Header set Cache-Control "public, max-age=3600, must-revalidate"',
        "  </FilesMatch>",
        '  <FilesMatch "\\.(woff2?|ttf)$">',
        '    Header set Cache-Control "public, max-age=31536000, immutable"',
        "  </FilesMatch>",
        '  <FilesMatch "\\.(avif|webp|png|jpe?g|gif|svg|ico)$">',
        '    Header set Cache-Control "public, max-age=604800, must-revalidate"',
        "  </FilesMatch>",
        "</IfModule>",
        "",
    ]
    with open(os.path.join(dist, ".htaccess"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def cache_bust(dist):
    """
    Acrescenta `?v=<hash>` à URL de cada folha de estilo/script externo
    referenciado no HTML, calculado a partir do conteúdo final (já
    minificado, ver minify_assets — por isso roda depois) de cada arquivo.

    Bug relatado pela cliente (README, item 178-bis): print de tela
    mostrando a caixa de consentimento marcada, com o aviso de erro
    "Marque a caixa acima pra continuar." ainda visível E desalinhado —
    grudado embaixo da caixa, flush à esquerda, em vez de alinhado com o
    texto de consentimento ao lado. Investigando, o HTML dela já tinha o
    `<span class="consent__err">` do item 176, mas o CSS ainda não conhecia
    a regra `grid-column: 2` daquele span (adicionada no mesmo commit) —
    ou seja, o navegador dela estava rodando HTML novo com CSS antigo ao
    mesmo tempo. Sem essa regra, o posicionamento automático do CSS Grid
    empurra o item pra próxima linha da primeira coluna, exatamente embaixo
    da caixa: reproduz o print exato.

    Causa raiz: `assets/(css|js)/*` é publicado com
    `Cache-Control: max-age=3600` (ver vercel.json) — depois de um deploy,
    tanto o navegador de quem já visitou quanto a borda da Vercel podem
    continuar servindo a cópia antiga de site.css por até 1h enquanto o
    HTML novo já está no ar. Versionar a URL pelo hash do conteúdo elimina
    essa janela: como o endereço muda toda vez que o conteúdo muda, a
    versão errada nunca fica em cache sob o endereço novo — sem precisar
    de refresh forçado nem de esperar o cache expirar.
    """
    targets = {}
    for rel_path in ("assets/css/site.css", "assets/js/site.js",
                      "assets/js/config.js", "assets/js/globe.js"):
        full = os.path.join(dist, *rel_path.split("/"))
        if os.path.exists(full):
            with open(full, "rb") as f:
                targets[rel_path] = hashlib.sha256(f.read()).hexdigest()[:10]
    if not targets:
        return
    patterns = [
        (re.compile(r'((?:href|src)="[^"]*' + re.escape(rel_path) + r')(")'), h)
        for rel_path, h in targets.items()
    ]
    for root, _, names in os.walk(dist):
        for n in names:
            if not n.endswith(".html"):
                continue
            path = os.path.join(root, n)
            raw = open(path, encoding="utf-8").read()
            patched = raw
            for pattern, h in patterns:
                patched = pattern.sub(lambda m, h=h: f"{m.group(1)}?v={h}{m.group(2)}", patched)
            if patched != raw:
                open(path, "w", encoding="utf-8").write(patched)


def emit_globe_js(dist):
    """
    Escreve o JS do globo como arquivo próprio (assets/js/globe.js).

    Ele mora em content/globe.py (é código gerado junto do conteúdo, não um
    asset escrito à mão), mas ir inline no HTML custava caro: são ~90 KB —
    com as fronteiras dos países dentro — em cima dos 150 KB do resto da
    home, tudo no caminho crítico, para um elemento decorativo. Como
    arquivo externo com defer, o HTML da home cai para menos da metade, o
    navegador começa a pintar antes e o globo chega depois, sem disputar
    com o conteúdo (ver README, item 119).
    """
    from content.globe import GLOBE_JS
    out = os.path.join(dist, "assets", "js", "globe.js")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(GLOBE_JS)


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "static"), DIST, dirs_exist_ok=True)
    emit_art(DIST)
    emit_globe_js(DIST)

    from content import home, institucional, solucoes, conteudos, contato, diagnostico, governanca, legal, programas, pronampe
    pages = []
    for mod in (home, institucional, solucoes, conteudos, contato, diagnostico, governanca, legal, programas, pronampe):
        pages.extend(mod.pages())

    for p in pages:
        write(p)

    # sitemap + robots
    urls = "".join(
        f"<url><loc>{SITE['domain']}{clean_url(p['path'])}</loc>"
        f"<changefreq>{'weekly' if p['path'] in ('index.html', 'conteudos.html') else 'monthly'}</changefreq>"
        f"<priority>{'1.0' if p['path'] == 'index.html' else '0.7'}</priority></url>"
        for p in pages if p["path"] != "404.html"
    )
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + urls + "</urlset>")
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")

    # security.txt (RFC 9116): canal formal pra quem encontrar uma
    # vulnerabilidade reportar antes de publicar — prática padrão de
    # divulgação responsável, sem ela um pesquisador não tem pra onde
    # escrever a não ser abrir o achado em público. "Expires" é obrigatório
    # no RFC (evita que o arquivo fique desatualizado pra sempre): 1 ano a
    # partir do build, então cada rebuild renova a data sozinho.
    expires = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)) \
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    security_txt = (
        f"Contact: mailto:{SITE['email']}\n"
        f"Expires: {expires}\n"
        f"Canonical: {SITE['domain']}/.well-known/security.txt\n"
        "Preferred-Languages: pt-BR, en\n"
    )
    wellknown_dir = os.path.join(DIST, ".well-known")
    os.makedirs(wellknown_dir, exist_ok=True)
    with open(os.path.join(wellknown_dir, "security.txt"), "w", encoding="utf-8") as f:
        f.write(security_txt)

    minify_assets(DIST)
    cache_bust(DIST)
    harden_csp(DIST)
    write_htaccess(DIST)

    print(f"{len(pages)} páginas geradas em {DIST}")
    return pages


if __name__ == "__main__":
    build()
