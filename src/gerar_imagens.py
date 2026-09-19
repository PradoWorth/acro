# -*- coding: utf-8 -*-
"""
Gera as variantes de cada foto do site a partir do arquivo original (.jpg):
uma versão reduzida para telas pequenas e a versão cheia, cada uma em AVIF e
WebP, com o .jpg original como último recurso. Isso inclui as miniaturas
quadradas de artigo (`-thumb.jpg`, 216×216): pequenas, mas sem variantes de
largura intermediária (já são a única versão exibida — ver o loop de
`WIDTHS` em `variants()`, que pula 800/1100 quando maiores que a própria
imagem).

Por que (ver README, item 119 — auditoria de performance):

  As fotos de topo de página têm 1400px de largura. No celular, a caixa em
  que elas aparecem tem ~412px de CSS; mesmo numa tela de 2,6x, isso dá
  ~1080px. Servir 1400px para todo mundo significa mandar ~64 KB quando
  ~28 KB entregam a mesma nitidez — e essa foto costuma ser justamente o
  maior elemento da primeira dobra (o LCP da página).

  Com srcset + sizes (ver raster_img, em build.py), o navegador escolhe:
  telas pequenas baixam a variante de 800px, telas grandes a de 1400px.

Como rodar (só quando entrar ou mudar alguma foto):

    python3 gerar_imagens.py

Precisa de avifenc e cwebp no PATH (pacotes libavif-bin e webp) e do
Pillow. Sem eles, o script avisa e não gera nada — o site continua
funcionando com o que já existe em static/assets/img/.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "static", "assets", "img")

# Larguras intermediárias geradas além da original. 800px cobre a caixa
# do celular a ~2x e o desktop a 1x; 1100px cobre o celular comum
# (412 CSS x 2,6) sem mandar os 1400px inteiros. O navegador escolhe pelo
# srcset/sizes (ver raster_img, em build.py).
WIDTHS = (800, 1100)

# Qualidade: AVIF 50 e WebP 72 ficaram, nas fotos deste site, visualmente
# indistinguíveis do original em tela cheia (PSNR ~35 dB), com metade do
# peso do que estava publicado antes.
AVIF_Q = "50"
WEBP_Q = "72"

# Exceções pontuais (ver README, item 154 — auditoria de compressão): fotos
# com muito mais detalhe de alta frequência que a média do site (foto aérea
# de skyline cheia de janelas e telhados; corredor de armazém cheio de
# caixas e plástico-bolha) pesam bem mais que as demais na mesma qualidade
# 50/72, porque têm muito mais entropia por pixel — não porque estejam
# "sem comprimir". Nesses dois casos, comparação lado a lado (recorte 3x)
# não mostrou diferença perceptível até AVIF 35-38; usamos 38 com folga.
# Chave = nome do arquivo (sem caminho), valor = (avif_q, webp_q).
QUALITY_OVERRIDES = {
    "solucoes-pagehead.jpg": ("32", WEBP_Q),
    "solucao-capital-de-giro.jpg": ("38", WEBP_Q),
}

# Fotos que não entram: os logotipos dos parceiros (WebP de poucos KB, sem
# .jpg de origem) e os ícones da mão do kanban (PNG com transparência, sem
# .jpg de origem — ver README, item 154, para como esses dois grupos foram
# comprimidos à parte).
SKIP_DIRS = {"partners", "kanban", "lp"}


def need(tool):
    if shutil.which(tool):
        return True
    print(f"Aviso: {tool} não encontrado no PATH — nada foi gerado.")
    return False


def variants(src):
    """Gera <nome>-800.{avif,webp} e <nome>.{avif,webp} a partir do .jpg."""
    from PIL import Image

    avif_q, webp_q = QUALITY_OVERRIDES.get(os.path.basename(src), (AVIF_Q, WEBP_Q))
    base, _ = os.path.splitext(src)
    im = Image.open(src)
    w, _h = im.size
    tmp = base + "-tmp.png"
    made = []

    for width, suffix in [(x, f"-{x}") for x in WIDTHS] + [(w, "")]:
        if width >= w and suffix:
            continue
        resized = im if width == w else im.resize(
            (width, round(im.size[1] * width / w)), Image.LANCZOS)
        resized.convert("RGB").save(tmp)
        for ext, cmd in (
            ("avif", ["avifenc", "-q", avif_q, "-s", "6", tmp, base + suffix + ".avif"]),
            ("webp", ["cwebp", "-q", webp_q, "-quiet", tmp, "-o", base + suffix + ".webp"]),
        ):
            subprocess.run(cmd, check=True, capture_output=True)
            made.append((base + suffix + "." + ext, os.path.getsize(base + suffix + "." + ext)))
    os.remove(tmp)
    return made


def main():
    if not (need("avifenc") and need("cwebp")):
        sys.exit(1)
    total_before = total_after = 0
    for root, dirs, names in os.walk(IMG):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in sorted(names):
            if not n.endswith(".jpg"):
                continue
            src = os.path.join(root, n)
            before = sum(os.path.getsize(os.path.join(root, f))
                          for f in os.listdir(root)
                          if f.startswith(os.path.splitext(n)[0]) and f.endswith((".avif", ".webp")))
            made = variants(src)
            after = sum(size for _, size in made)
            total_before += before
            total_after += after
            rel = os.path.relpath(src, IMG)
            print(f"{rel}: {before/1024:.0f} KB -> {after/1024:.0f} KB em {len(made)} variantes")
    print(f"\ntotal das variantes: {total_before/1024:.0f} KB -> {total_after/1024:.0f} KB")


if __name__ == "__main__":
    main()
