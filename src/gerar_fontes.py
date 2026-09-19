# -*- coding: utf-8 -*-
"""
Gera as duas fontes auto-hospedadas do site a partir dos pacotes originais
(Fontsource, SIL Open Font License), reduzidas aos caracteres que o site
realmente usa.

Por que existe (ver README, item 119 — auditoria de performance):

  Antes, o site servia 5 arquivos estáticos (Inter 400/500/600/700 +
  Manrope 700 = 108 KB) e o navegador precisava dos 5 antes de pintar o
  texto no peso final. Fonte é o maior peso do caminho crítico de uma
  página estática como esta, e era o que segurava o LCP: o texto pintava
  na fonte do sistema e trocava quando a Inter chegava.

  Agora são 2 arquivos (47 KB no total):
    - Inter VARIÁVEL (um arquivo com o eixo de peso 100-900, cobrindo os
      4 pesos que o site usa),
    - Manrope 700 estática (a única que o site usa dessa família — a
      variável dela seria maior que a estática de um peso só).

  Os dois são reduzidos (subset) ao repertório de caracteres do site:
  ASCII, Latin-1 completo (todo o português, espanhol e francês), mais a
  pontuação tipográfica usada (travessão, aspas curvas, reticências,
  seta, visto, euro). Nada que o site escreve hoje — nem o que ele
  provavelmente escreverá — fica de fora.

Como rodar (só é preciso quando quiser regerar as fontes):

    npm pack @fontsource-variable/inter @fontsource/manrope
    tar xzf fontsource-variable-inter-*.tgz && mv package inter-var
    tar xzf fontsource-manrope-*.tgz && mv package manrope
    pip install fonttools brotli
    python3 gerar_fontes.py inter-var/files/inter-latin-wght-normal.woff2 \\
                            manrope/files/manrope-latin-700-normal.woff2

O resultado vai para static/assets/fonts/ e é referenciado por
static/assets/css/fonts.css.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ROOT, "static", "assets", "fonts")

# Repertório mantido no subset. Latin-1 inteiro (U+00A0-00FF) cobre todo o
# português; o resto é a pontuação tipográfica que o site usa de fato.
UNICODES = ",".join([
    "U+0020-007E",   # ASCII imprimível
    "U+00A0-00FF",   # Latin-1: acentos, ç, º, ª, ©, ×, °
    "U+2013-2014",   # – —
    "U+2018-201A",   # ' ' ‚
    "U+201C-201E",   # " " „
    "U+2022",        # •
    "U+2026",        # …
    "U+20AC",        # €
    "U+2122",        # ™
    "U+2190-2193",   # ← ↑ → ↓
    "U+2212",        # −
    "U+2713",        # ✓
])

FEATURES = "kern,liga,calt,ccmp,locl,mark,mkmk"


def subset(src, out_name):
    out = os.path.join(DEST, out_name)
    subprocess.run(
        ["pyftsubset", src, f"--unicodes={UNICODES}", "--flavor=woff2",
         f"--layout-features={FEATURES}", "--drop-tables+=DSIG",
         f"--output-file={out}"],
        check=True,
    )
    print(f"{os.path.basename(src)}: {os.path.getsize(src)/1024:.1f} KB -> "
          f"{out_name} {os.path.getsize(out)/1024:.1f} KB")
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit("uso: gerar_fontes.py <inter-variavel.woff2> <manrope-700.woff2>")
    os.makedirs(DEST, exist_ok=True)
    subset(sys.argv[1], "inter-var.woff2")
    subset(sys.argv[2], "manrope-700.woff2")


if __name__ == "__main__":
    main()
