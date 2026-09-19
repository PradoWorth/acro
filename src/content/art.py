# -*- coding: utf-8 -*-
"""
Biblioteca visual da Acrópole Capital.

Nada aqui é banco de imagens. São composições arquitetônicas em camadas, com
perspectiva atmosférica (planos mais distantes ficam mais apagados), luz
direcional, grão e sobreposição de desenho técnico. Os diagramas das soluções
continuam carregando informação real sobre cada operação.
"""

L = "rgba(255,255,255,.09)"
L2 = "rgba(255,255,255,.18)"
L3 = "rgba(255,255,255,.42)"
BR = "rgba(138,206,196,.72)"
BR2 = "rgba(20,157,136,.45)"
TX = "rgba(255,255,255,.42)"


def _grain(ident, opacity=".055", freq=".9"):
    """Grão fino: tira o aspecto chapado e dá materialidade de impresso."""
    return f"""<filter id="{ident}" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="4" seed="7" result="n"/>
    <feColorMatrix in="n" type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope="{opacity}"/></feComponentTransfer>
  </filter>"""


def _windows(x, y, cols, rows, cw, ch, gap, fill, lit=(), lit_fill=None):
    out = []
    for r in range(rows):
        for c in range(cols):
            f = lit_fill if (r, c) in lit and lit_fill else fill
            out.append(f'<rect x="{x + c * (cw + gap)}" y="{y + r * (ch + gap)}" '
                       f'width="{cw}" height="{ch}" fill="{f}"/>')
    return "".join(out)


def _tower(x, base, w, h, tone, win_tone, lit_tone=None, cols=4, rows=9, setback=0):
    """Torre com recuo opcional no topo e janelas, algumas acesas."""
    top = base - h
    body = f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{tone}"/>'
    if setback:
        body += (f'<rect x="{x + setback}" y="{top - 46}" width="{w - setback * 2}" '
                 f'height="46" fill="{tone}"/>')
        body += (f'<line x1="{x + w // 2}" y1="{top - 46}" x2="{x + w // 2}" '
                 f'y2="{top - 78}" stroke="{tone}" stroke-width="2"/>')
    cw = max(4, (w - (cols + 1) * 7) // cols)
    lit = {(1, 1), (3, 0), (4, 2), (6, 1), (7, 3), (2, 3)} if lit_tone else ()
    body += _windows(x + 8, top + 16, cols, rows, cw, 9, 7, win_tone, lit, lit_tone)
    return body


# ---------------------------------------------------------------------- hero
def hero():
    """Skyline em três planos, fachada em primeiro plano e desenho técnico sobreposto."""
    far = ""
    for x, w, h, c, r in ((60, 92, 300, 3, 8), (176, 74, 380, 3, 10), (268, 108, 250, 4, 6),
                          (396, 86, 420, 3, 11), (500, 120, 330, 4, 8), (640, 78, 470, 3, 12),
                          (738, 100, 360, 4, 9), (860, 88, 300, 3, 8), (966, 130, 410, 5, 10),
                          (1116, 84, 340, 3, 9), (1218, 110, 270, 4, 7), (1348, 96, 390, 4, 10),
                          (1462, 118, 320, 4, 8)):
        far += _tower(x, 760, w, h, "rgba(163,186,190,.085)", "rgba(12,14,16,.16)", None, c, r)

    mid = ""
    for x, w, h, c, r, sb in ((30, 130, 400, 5, 11, 0), (196, 108, 520, 4, 14, 18),
                              (330, 150, 350, 6, 9, 0), (516, 118, 470, 4, 12, 22),
                              (668, 160, 300, 6, 8, 0), (864, 124, 540, 5, 14, 20),
                              (1024, 142, 380, 5, 10, 0), (1204, 112, 460, 4, 12, 18),
                              (1352, 168, 330, 6, 9, 0)):
        mid += _tower(x, 800, w, h, "rgba(120,146,152,.14)", "rgba(12,14,16,.26)",
                      "rgba(138,206,196,.20)", c, r, sb)

    flutes = "".join(
        f'<line x1="{1088 + i * 11}" y1="352" x2="{1088 + i * 11}" y2="812" '
        f'stroke="rgba(255,255,255,.055)" stroke-width="1"/>' for i in range(44))
    piers = "".join(
        f'<rect x="{1080 + i * 84}" y="330" width="26" height="482" fill="rgba(255,255,255,.075)"/>'
        for i in range(6))
    ticks = "".join(
        f'<line x1="{72 + i * 38}" y1="866" x2="{72 + i * 38}" '
        f'y2="{874 if i % 5 else 884}" stroke="{L2}" stroke-width="1"/>' for i in range(40))

    return f"""<svg width="1600" height="1000" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="acr-sky" x1="0" y1="0" x2=".35" y2="1">
      <stop offset="0" stop-color="#030b12"/>
      <stop offset=".46" stop-color="#030b12"/>
      <stop offset="1" stop-color="#02080c"/>
    </linearGradient>
    <radialGradient id="acr-glow" cx=".74" cy=".16" r=".62">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".62"/>
      <stop offset=".45" stop-color="#093e3e" stop-opacity=".28"/>
      <stop offset="1" stop-color="#030b12" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="acr-haze" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#030b12" stop-opacity=".92"/>
      <stop offset=".55" stop-color="#030b12" stop-opacity=".18"/>
      <stop offset="1" stop-color="#030b12" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="acr-floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#083436" stop-opacity=".85"/>
      <stop offset="1" stop-color="#02080c" stop-opacity="1"/>
    </linearGradient>
    <linearGradient id="acr-veil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#02080c" stop-opacity=".96"/>
      <stop offset=".42" stop-color="#02080c" stop-opacity=".72"/>
      <stop offset=".78" stop-color="#02080c" stop-opacity=".08"/>
      <stop offset="1" stop-color="#02080c" stop-opacity="0"/>
    </linearGradient>
    {_grain("acr-grain", ".07")}
  </defs>

  <rect width="1600" height="1000" fill="url(#acr-sky)"/>
  <rect width="1600" height="1000" fill="url(#acr-glow)"/>

  <g>{far}</g>
  <rect x="0" y="420" width="1600" height="380" fill="url(#acr-haze)" opacity=".55"/>
  <g>{mid}</g>

  <g>
    <rect x="1064" y="330" width="536" height="482" fill="rgba(255,255,255,.035)"/>
    {flutes}{piers}
    <rect x="1064" y="300" width="536" height="30" fill="rgba(255,255,255,.10)"/>
    <rect x="1064" y="292" width="536" height="6" fill="rgba(138,206,196,.24)"/>
    <line x1="1064" y1="812" x2="1600" y2="812" stroke="rgba(255,255,255,.22)" stroke-width="1"/>
  </g>

  <rect x="0" y="800" width="1600" height="200" fill="url(#acr-floor)"/>
  <g opacity=".16" transform="translate(0,1624) scale(1,-1)">
    <rect x="1064" y="330" width="536" height="140" fill="rgba(255,255,255,.05)"/>
  </g>

  <g>
    <line x1="0" y1="118" x2="1600" y2="118" stroke="{L2}" stroke-width="1"/>
    <line x1="0" y1="866" x2="1600" y2="866" stroke="{L2}" stroke-width="1"/>
    {ticks}
    <path d="M1064 292 Q 1332 168 1600 292" fill="none" stroke="{BR}" stroke-width="1"/>
    <circle cx="1332" cy="230" r="3.5" fill="none" stroke="{BR}" stroke-width="1"/>
    <line x1="1332" y1="118" x2="1332" y2="866" stroke="{BR2}" stroke-width="1" stroke-dasharray="2 10"/>
    <line x1="1040" y1="330" x2="1040" y2="812" stroke="{BR2}" stroke-width="1"/>
    <path d="M1030 330 h20 M1030 812 h20" stroke="{BR2}" stroke-width="1"/>
  </g>

  <rect width="1600" height="1000" fill="url(#acr-veil)"/>
  <rect width="1600" height="1000" filter="url(#acr-grain)" opacity=".5"/>
</svg>"""


# ------------------------------------------------------------------ pagehead
def pagehead(variant=0):
    """Topo interno: mesma linguagem do hero, em registro mais baixo."""
    v = variant % 3

    if v == 0:
        # colunata em perspectiva, sobre silhueta urbana
        sky = ""
        for x, w, h, c, r in ((700, 96, 300, 3, 8), (812, 124, 400, 4, 10), (952, 88, 250, 3, 6),
                              (1056, 132, 360, 4, 9), (1204, 100, 290, 3, 7), (1320, 138, 430, 4, 11),
                              (1474, 108, 320, 4, 8)):
            sky += _tower(x, 456, w, h, "rgba(163,186,190,.085)", "rgba(12,14,16,.20)",
                          "rgba(138,206,196,.20)", c, r)
        cols = "".join(
            f'<rect x="{960 + i * 106}" y="{132 + i * 6}" width="36" height="{324 - i * 6}" '
            f'fill="rgba(255,255,255,{.15 - i * .014:.3f})"/>' for i in range(7))
        art = (sky + '<rect x="936" y="104" width="740" height="28" fill="rgba(255,255,255,.17)"/>'
               '<rect x="936" y="96" width="740" height="5" fill="rgba(138,206,196,.38)"/>' + cols)
        accent = (f'<path d="M936 96 Q 1306 26 1676 96" fill="none" stroke="{BR}" stroke-width="1"/>'
                  f'<circle cx="1306" cy="61" r="3" fill="none" stroke="{BR}" stroke-width="1"/>')

    elif v == 1:
        # skyline denso
        art = ""
        for x, w, h, c, r in ((640, 104, 300, 4, 8), (760, 136, 420, 5, 11), (912, 92, 250, 3, 6),
                              (1020, 124, 380, 4, 10), (1160, 106, 290, 4, 7), (1282, 148, 450, 5, 12),
                              (1446, 116, 330, 4, 8)):
            art += _tower(x, 456, w, h, "rgba(255,255,255,.105)", "rgba(12,14,16,.26)",
                          "rgba(138,206,196,.22)", c, r)
        accent = (f'<path d="M640 150 Q 1150 46 1660 150" fill="none" stroke="{BR}" stroke-width="1"/>'
                  f'<line x1="1150" y1="80" x2="1150" y2="456" stroke="{BR2}" stroke-width="1" stroke-dasharray="2 10"/>')

    else:
        # malha cadastral e implantação
        grid_l = "".join(f'<line x1="{i * 88}" y1="0" x2="{i * 88}" y2="520" stroke="{L}" stroke-width="1"/>'
                         for i in range(19))
        grid_l += "".join(f'<line x1="0" y1="{i * 88}" x2="1600" y2="{i * 88}" stroke="{L}" stroke-width="1"/>'
                          for i in range(7))
        art = (grid_l
               + '<rect x="960" y="118" width="480" height="290" fill="rgba(255,255,255,.045)" '
                 'stroke="rgba(255,255,255,.18)" stroke-width="1"/>'
               + '<rect x="1004" y="160" width="270" height="206" fill="url(#ph-plot2)" '
                 'stroke="rgba(255,255,255,.14)" stroke-width="1"/>'
               + '<rect x="1300" y="160" width="96" height="206" fill="none" '
                 f'stroke="{BR2}" stroke-width="1" stroke-dasharray="5 5"/>')
        accent = (f'<circle cx="1200" cy="262" r="176" fill="none" stroke="{BR2}" stroke-width="1"/>'
                  f'<line x1="960" y1="430" x2="1440" y2="430" stroke="{BR}" stroke-width="1"/>'
                  f'<path d="M960 424 v12 M1440 424 v12" stroke="{BR}" stroke-width="1"/>')

    ticks = "".join(
        f'<line x1="{60 + i * 40}" y1="470" x2="{60 + i * 40}" '
        f'y2="{476 if i % 5 else 484}" stroke="{L2}" stroke-width="1"/>' for i in range(38))

    return f"""<svg width="1600" height="520" viewBox="0 0 1600 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ph-sky{v}" x1="0" y1="0" x2=".3" y2="1">
      <stop offset="0" stop-color="#030b12"/><stop offset=".6" stop-color="#030b12"/>
      <stop offset="1" stop-color="#02080c"/>
    </linearGradient>
    <radialGradient id="ph-glow{v}" cx=".78" cy=".05" r=".78">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".62"/>
      <stop offset=".5" stop-color="#093e3e" stop-opacity=".24"/>
      <stop offset="1" stop-color="#030b12" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ph-plot{v}" x1="0" y1="0" x2=".8" y2="1">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".42"/>
      <stop offset="1" stop-color="#093e3e" stop-opacity=".12"/>
    </linearGradient>
    <linearGradient id="ph-horizon{v}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d5e57" stop-opacity="0"/>
      <stop offset="1" stop-color="#0d5e57" stop-opacity=".26"/>
    </linearGradient>
    <linearGradient id="ph-floor{v}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#083436" stop-opacity=".8"/>
      <stop offset="1" stop-color="#02080c"/>
    </linearGradient>
    <linearGradient id="ph-veil{v}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#02080c" stop-opacity=".97"/>
      <stop offset=".44" stop-color="#02080c" stop-opacity=".8"/>
      <stop offset=".8" stop-color="#02080c" stop-opacity=".1"/>
      <stop offset="1" stop-color="#02080c" stop-opacity="0"/>
    </linearGradient>
    {_grain("ph-grain" + str(v), ".06")}
  </defs>
  <rect width="1600" height="520" fill="url(#ph-sky{v})"/>
  <rect width="1600" height="520" fill="url(#ph-glow{v})"/>
  {art}
  <rect x="0" y="392" width="1600" height="64" fill="url(#ph-horizon{v})"/>
  <rect x="0" y="456" width="1600" height="64" fill="url(#ph-floor{v})"/>
  <line x1="0" y1="456" x2="1600" y2="456" stroke="{L2}" stroke-width="1"/>
  {ticks}{accent}
  <rect width="1600" height="520" fill="url(#ph-veil{v})"/>
  <rect width="1600" height="520" filter="url(#ph-grain{v})" opacity=".45"/>
</svg>"""


# ----------------------------------------------------------- placa de fundo
def _plate(ident):
    return f"""<defs>
    <linearGradient id="pl{ident}" x1="0" y1="0" x2=".7" y2="1">
      <stop offset="0" stop-color="#030e17"/>
      <stop offset=".55" stop-color="#030b12"/>
      <stop offset="1" stop-color="#030b12"/>
    </linearGradient>
    <radialGradient id="pg{ident}" cx=".82" cy=".12" r=".8">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".34"/>
      <stop offset="1" stop-color="#030b12" stop-opacity="0"/>
    </radialGradient>
    {_grain("gr" + ident, ".05", "1.1")}
  </defs>
  <rect width="520" height="360" fill="url(#pl{ident})"/>
  <rect width="520" height="360" fill="url(#pg{ident})"/>"""


def _frame(body, label, ident):
    return f"""<svg viewBox="0 0 520 360" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">
  {_plate(ident)}
  {body}
  <rect width="520" height="360" filter="url(#gr{ident})" opacity=".55"/>
  <path d="M46 20 H28 Q20 20 20 28 V46 M474 340 H492 Q500 340 500 332 V314"
        stroke="{BR2}" stroke-width="1" fill="none"/>
</svg>"""


# ---------------------------------------------------------------- diagramas
def flux():
    pay = "".join(f'<rect x="{56 + i * 62}" y="116" width="34" height="22" rx="2" fill="{L3}"/>' for i in range(6))
    rec = "".join(f'<rect x="{104 + i * 62}" y="226" width="34" height="22" rx="2" fill="url(#fx-br)"/>' for i in range(6))
    # Faixa cheia (não um traço fino) ligando o rodapé de cada barra de
    # pagamento ao topo da barra de recebimento correspondente — a mesma
    # largura da barra nas duas pontas, só que inclinada, para ler como um
    # fluxo contínuo em vez de três retângulos soltos e desalinhados.
    gap = "".join(
        f'<polygon points="{56 + i * 62},138 {90 + i * 62},138 '
        f'{138 + i * 62},226 {104 + i * 62},226" fill="url(#fx-gap)"/>'
        for i in range(6)
    )
    # Setas discretas nos dois grupos de barra: para deixar óbvio, sem
    # precisar ler o texto primeiro, que um bloco é dinheiro saindo (seta
    # para baixo) e o outro é dinheiro entrando (seta para cima).
    pay_arrows = "".join(
        f'<path class="fx-arrow-pay" style="animation-delay:{i * .12:.2f}s" '
        f'd="M{73 + i * 62} 98 L{73 + i * 62} 112 M{69 + i * 62} 106 '
        f'L{73 + i * 62} 112 L{77 + i * 62} 106" stroke="{TX}" '
        f'stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        for i in range(6)
    )
    rec_arrows = "".join(
        f'<path class="fx-arrow-rec" style="animation-delay:{.5 + i * .12:.2f}s" '
        f'd="M{121 + i * 62} 266 L{121 + i * 62} 252 M{117 + i * 62} 258 '
        f'L{121 + i * 62} 252 L{125 + i * 62} 258" stroke="#8acec4" '
        f'stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        for i in range(6)
    )
    # Chave de medida na quarta coluna: dá um número concreto (o mesmo do
    # texto ao lado, 35 dias) ao espaço entre pagar e receber, que sem
    # rótulo é só uma faixa colorida — o que faz o descasamento saltar aos
    # olhos é o número, não a forma.
    bx = 400
    bracket = f"""
    <line class="diagram-march" x1="{bx}" y1="138" x2="{bx}" y2="226" stroke="#8acec4" stroke-width="1" stroke-dasharray="2 4"/>
    <line x1="{bx - 5}" y1="138" x2="{bx + 5}" y2="138" stroke="#8acec4" stroke-width="1"/>
    <line x1="{bx - 5}" y1="226" x2="{bx + 5}" y2="226" stroke="#8acec4" stroke-width="1"/>
    <text x="{bx + 11}" y="178" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="600">35</text>
    <text x="{bx + 11}" y="192" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="9" letter-spacing=".5">dias</text>"""
    return _frame(f"""
    <defs>
      <linearGradient id="fx-gap" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#0d5e57" stop-opacity=".95"/>
        <stop offset="1" stop-color="#093e3e" stop-opacity=".55"/>
      </linearGradient>
      <linearGradient id="fx-br" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#8acec4"/><stop offset="1" stop-color="#317ae2"/>
      </linearGradient>
    </defs>
    <line x1="40" y1="86" x2="480" y2="86" stroke="{L}" stroke-width="1"/>
    <line x1="40" y1="272" x2="480" y2="272" stroke="{L}" stroke-width="1"/>
    <text x="40" y="70" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Pagamentos a fornecedores</text>
    <text x="40" y="300" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Recebimentos de clientes</text>
    {gap}{pay}{rec}{pay_arrows}{rec_arrows}{bracket}
    <text x="40" y="332" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Necessidade de capital de giro</text>
    """, "Descasamento entre prazos de pagamento e de recebimento", "fx")


def elevation():
    win = ""
    for r in range(5):
        for c in range(4):
            is_lit = (r, c) in {(1, 1), (3, 2)}
            lit = "rgba(138,206,196,.22)" if is_lit else "rgba(255,255,255,.05)"
            cls = ' class="diagram-anim el-window"' if is_lit else ""
            delay = f' style="animation-delay:{(r + c) * .18:.2f}s"' if is_lit else ""
            win += (f'<rect{cls}{delay} x="{150 + c * 56}" y="{104 + r * 42}" width="34" height="26" rx="2" '
                    f'fill="{lit}" stroke="{L2}" stroke-width="1"/>')
    return _frame(f"""
    <defs><linearGradient id="el-f" x1="0" y1="0" x2=".6" y2="1">
      <stop offset="0" stop-color="rgba(255,255,255,.09)"/><stop offset="1" stop-color="rgba(255,255,255,.02)"/>
    </linearGradient></defs>
    <clipPath id="el-clip"><rect x="128" y="80" width="264" height="230" rx="8"/></clipPath>
    <rect x="128" y="80" width="264" height="230" rx="8" fill="url(#el-f)" stroke="{L3}" stroke-width="1"/>
    <path d="M112 80 L260 32 L408 80 Z" fill="rgba(255,255,255,.055)" stroke="{L3}" stroke-width="1"/>
    {win}
    <rect x="128" y="218" width="264" height="92" fill="rgba(29,90,102,.30)" clip-path="url(#el-clip)"/>
    <line class="diagram-march" x1="60" y1="218" x2="460" y2="218" stroke="#8acec4" stroke-width="1" stroke-dasharray="4 5"/>
    <line x1="40" y1="310" x2="480" y2="310" stroke="{L2}" stroke-width="1"/>
    <text x="60" y="208" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Margem liberável (LTV)</text>
    <text x="60" y="336" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Posse e uso permanecem com o proprietário</text>
    """, "Elevação de imóvel indicando a margem liberável sob garantia", "el")


def chassis():
    # Perfil de sedã em silhueta única (capô, para-brisa, teto, vigia e porta-malas
    # em uma curva contínua), com as rodas encaixadas no para-lama — o desenho que
    # o cliente confirmou como referência definitiva.
    rocker_y, wheel_r = 264, 28
    wheel_cy = 288 - wheel_r
    fw, rw = 172, 360
    body = (f"M92,{rocker_y} "
            f"C96,{rocker_y-8} 100,{rocker_y-18} 106,{rocker_y-28} "
            f"C114,{rocker_y-42} 126,{rocker_y-50} 140,{rocker_y-52} "
            f"L{fw+34},{rocker_y-52} "
            f"C{fw+50},{rocker_y-72} {fw+72},{rocker_y-86} {fw+96},{rocker_y-90} "
            f"L{rw-58},{rocker_y-90} "
            f"C{rw-32},{rocker_y-87} {rw-14},{rocker_y-76} {rw-4},{rocker_y-54} "
            f"L{rw+38},{rocker_y-54} "
            f"C{rw+52},{rocker_y-54} {rw+63},{rocker_y-48} {rw+69},{rocker_y-38} "
            f"C{rw+75},{rocker_y-28} {rw+78},{rocker_y-14} {rw+80},{rocker_y} "
            f"Z")
    windshield = f"M{fw+34},{rocker_y-52} L{fw+58},{rocker_y-72}"
    rear_window = f"M{rw-4},{rocker_y-54} L{rw-20},{rocker_y-78}"
    return _frame(f"""
    <defs><linearGradient id="ch-c" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8acec4"/><stop offset="1" stop-color="#317ae2" stop-opacity=".5"/>
    </linearGradient></defs>
    <path d="{body}" fill="rgba(255,255,255,.06)" stroke="{L3}" stroke-width="1.2"/>
    <path d="{windshield}" stroke="{L2}" stroke-width="1"/>
    <path d="{rear_window}" stroke="{L2}" stroke-width="1"/>
    <circle cx="{fw}" cy="{wheel_cy}" r="{wheel_r}" fill="rgba(12,14,16,.85)" stroke="{L3}" stroke-width="1.2"/>
    <circle cx="{fw}" cy="{wheel_cy}" r="{round(wheel_r*0.4)}" fill="none" stroke="{L2}" stroke-width="1"/>
    <circle cx="{rw}" cy="{wheel_cy}" r="{wheel_r}" fill="rgba(12,14,16,.85)" stroke="{L3}" stroke-width="1.2"/>
    <circle cx="{rw}" cy="{wheel_cy}" r="{round(wheel_r*0.4)}" fill="none" stroke="{L2}" stroke-width="1"/>
    <line x1="40" y1="288" x2="480" y2="288" stroke="{L2}" stroke-width="1"/>
    <path class="diagram-draw" pathLength="1" d="M60 96 C 160 118, 300 152, 462 178" fill="none" stroke="url(#ch-c)" stroke-width="1.5"/>
    <text x="60" y="84" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Curva de depreciação do bem</text>
    <text x="60" y="322" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">O prazo do contrato precisa caber sob a curva</text>
    """, "Perfil de veículo sob a curva de depreciação do ativo", "ch")


def matrix():
    cells = ""
    for r in range(5):
        for c in range(7):
            sel = c == 4
            cls = ' class="diagram-anim mx-dot"' if sel else ""
            delay = f' style="animation-delay:{r * .16:.2f}s"' if sel else ""
            cells += (f'<circle{cls}{delay} cx="{92 + c * 56}" cy="{116 + r * 40}" r="{4 if sel else 2.5}" '
                      f'fill="{"#8acec4" if sel else L2}"/>')
    return _frame(f"""
    <defs><linearGradient id="mx-c" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".6"/><stop offset="1" stop-color="#093e3e" stop-opacity=".25"/>
    </linearGradient></defs>
    <clipPath id="mx-clip"><rect x="64" y="88" width="392" height="216" rx="8"/></clipPath>
    <rect x="64" y="88" width="392" height="216" rx="8" fill="rgba(255,255,255,.02)" stroke="{L}" stroke-width="1"/>
    <rect x="288" y="88" width="56" height="216" fill="url(#mx-c)" clip-path="url(#mx-clip)"/>
    <line x1="288" y1="88" x2="288" y2="304" stroke="{BR2}" stroke-width="1"/>
    <line x1="344" y1="88" x2="344" y2="304" stroke="{BR2}" stroke-width="1"/>
    {cells}
    <text x="64" y="76" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Instituições comparadas</text>
    <text x="64" y="334" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Escolha por CET, não por taxa de vitrine</text>
    """, "Matriz de comparação entre instituições financeiras", "mx")


def layers():
    rows = [(94, 392, "Sênior com garantia real"), (134, 312, "Complementar"),
            (174, 232, "Ponte / cronograma"), (214, 152, "Recursos próprios")]
    body = ""
    for i, (y, w, label) in enumerate(rows):
        fill = "url(#ly-s)" if i == 0 else ("rgba(29,90,102,.20)" if i == 1 else "rgba(255,255,255,.03)")
        body += (f'<rect class="diagram-grow-x" style="animation-delay:{i * .1:.2f}s" '
                 f'x="64" y="{y}" width="{w}" height="30" rx="4" fill="{fill}" stroke="{L2}" stroke-width="1"/>')
        if i >= 2:
            body += (f'<text x="{64 + w + 12}" y="{y + 20}" fill="{TX}" font-family="Inter, system-ui, sans-serif" '
                     f'font-size="10" letter-spacing="1">{label}</text>')
    return _frame(f"""
    <defs><linearGradient id="ly-s" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".8"/><stop offset="1" stop-color="#093e3e" stop-opacity=".4"/>
    </linearGradient></defs>
    {body}
    <line x1="64" y1="286" x2="456" y2="286" stroke="{L2}" stroke-width="1"/>
    <line x1="456" y1="94" x2="456" y2="286" stroke="#8acec4" stroke-width="1"/>
    <path d="M450 94 h12 M450 286 h12" stroke="#8acec4" stroke-width="1"/>
    <text x="64" y="76" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Composição da operação</text>
    <text x="64" y="326" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Fontes combinadas, uma só formalização</text>
    """, "Camadas de uma operação estruturada", "ly")


def grid():
    steps = ""
    for i in range(6):
        f = "url(#gd-a)" if i < 4 else "rgba(255,255,255,.07)"
        steps += (f'<rect class="diagram-grow-y" style="animation-delay:{i * .1:.2f}s" '
                  f'x="{72 + i * 56}" y="{264 - i * 32}" width="46" '
                  f'height="{16 + i * 32}" rx="3" fill="{f}" stroke="{L2}" stroke-width="1"/>')
    return _frame(f"""
    <defs><linearGradient id="gd-a" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".75"/><stop offset="1" stop-color="#093e3e" stop-opacity=".3"/>
    </linearGradient></defs>
    {steps}
    <line x1="56" y1="280" x2="464" y2="280" stroke="{L2}" stroke-width="1"/>
    <line x1="408" y1="70" x2="408" y2="280" stroke="#8acec4" stroke-width="1" stroke-dasharray="4 5"/>
    <text x="72" y="62" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Liberação acompanha o avanço da obra</text>
    <text x="222" y="308" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Amortização inicia após a conclusão</text>
    """, "Liberação escalonada de recursos ao longo da obra", "gd")


def plan():
    hatch = "".join(f'<line x1="{124 + i * 14}" y1="112" x2="{96 + i * 14}" y2="252" '
                    f'stroke="{L}" stroke-width="1"/>' for i in range(16))
    return _frame(f"""
    <defs><linearGradient id="pn-b" x1="0" y1="0" x2=".8" y2="1">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".38"/><stop offset="1" stop-color="#093e3e" stop-opacity=".12"/>
    </linearGradient></defs>
    <rect x="64" y="80" width="392" height="200" rx="8" fill="rgba(255,255,255,.02)" stroke="{L3}" stroke-width="1"/>
    <rect x="96" y="112" width="232" height="140" rx="4" fill="url(#pn-b)" stroke="{L2}" stroke-width="1"/>
    {hatch}
    <rect class="diagram-march" x="352" y="112" width="80" height="140" rx="4" fill="none" stroke="{BR2}" stroke-width="1" stroke-dasharray="4 4"/>
    <line x1="64" y1="300" x2="456" y2="300" stroke="#8acec4" stroke-width="1"/>
    <path d="M64 294 v12 M456 294 v12" stroke="#8acec4" stroke-width="1"/>
    <text x="64" y="68" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Terreno</text>
    <text x="352" y="270" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="10" letter-spacing="1">Fase 2</text>
    <text x="64" y="330" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Aquisição e obra em uma única estrutura</text>
    """, "Planta de implantação com fase de expansão", "pn")


def securitize():
    # Carteira de recebíveis (as barras à esquerda) convergindo para um único
    # título emitido (o bloco maior à direita) — o mesmo lastro, e cada barra
    # "some" dentro da estrutura do título em vez de ficar solta, para ler
    # como conversão, não como uma lista ao lado de uma caixa qualquer.
    #
    # Animação própria (ver site.css, ".diagram--securitize"), no mesmo
    # padrão das outras 7: as barras crescem a partir da esquerda em
    # sequência (mesmo mecanismo de "layers"), os traços de convergência se
    # desenham até o título (mesmo mecanismo de "chassis"), o bloco do
    # título pulsa suavemente uma vez revelado, e a seta de saída avança
    # em marcha contínua, como o próprio recurso saindo em direção ao
    # cedente.
    n = 5
    bars = ""
    # Base do bloco de barras calculada para centralizar o grupo (5 barras,
    # 22px de altura, 34px de passo — 158px de altura total) no mesmo eixo
    # vertical do bloco "Título emitido" ao lado (y 140-260, centro 200):
    # 200 - 158/2 = 121. Antes a base era um número fixo (90) que não
    # acompanhava esse cálculo — as barras ficavam ~31px acima do centro
    # do bloco, lendo como desalinhado ("torto") em vez de convergindo
    # simetricamente para ele.
    group_h = (n - 1) * 34 + 22
    base_y = 200 - group_h // 2
    for i in range(n):
        y = base_y + i * 34
        bars += (f'<rect class="diagram-grow-x" style="animation-delay:{i * .1:.2f}s" '
                 f'x="56" y="{y}" width="128" height="22" rx="3" '
                 f'fill="rgba(255,255,255,.05)" stroke="{L2}" stroke-width="1"/>')
        bars += (f'<path class="diagram-draw" pathLength="1" style="animation-delay:{i * .1 + .2:.2f}s" '
                 f'd="M184 {y + 11} C 240 {y + 11}, 270 200, 300 200" '
                 f'fill="none" stroke="{L2}" stroke-width="1"/>')
    return _frame(f"""
    <defs><linearGradient id="sc-t" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d5e57" stop-opacity=".85"/><stop offset="1" stop-color="#093e3e" stop-opacity=".4"/>
    </linearGradient></defs>
    {bars}
    <rect class="sc-block" x="300" y="140" width="120" height="120" rx="6" fill="url(#sc-t)" stroke="{BR2}" stroke-width="1"/>
    <line class="diagram-march" x1="428" y1="200" x2="468" y2="200" stroke="#8acec4" stroke-width="1" stroke-dasharray="4 4"/>
    <path class="sc-arrow" d="M460 194 L468 200 L460 206" stroke="#8acec4" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="56" y="{base_y - 14}" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Carteira de recebíveis</text>
    <text x="300" y="130" fill="{TX}" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Título emitido</text>
    <text x="300" y="334" fill="#8acec4" font-family="Inter, system-ui, sans-serif" font-size="11" letter-spacing="1">Liquidez antecipada ao cedente</text>
    """, "Carteira de recebíveis convertida em título de mercado de capitais", "sc")


DIAGRAMS = {"flux": flux, "elevation": elevation, "chassis": chassis,
            "matrix": matrix, "layers": layers, "grid": grid, "plan": plan,
            "securitize": securitize}


def diagram(kind):
    return DIAGRAMS[kind]()

