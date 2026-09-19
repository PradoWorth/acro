import os
from PIL import Image

SRC = "/tmp/work/site/acropole-capital/_novas_fotos_raw_lote4"
DST = "/tmp/work/site/acropole-capital/src/static/assets/img/conteudos"

MAIN_W, MAIN_H = 720, 480   # 3:2, mesmo padrão dos artigos já existentes
THUMB = 216                  # quadrado, para os cards de "relacionados"

jobs = [
    ("artigo-como-conseguir-credito-para-a-empresa.jpg", "como-conseguir-credito-para-a-empresa"),
    ("artigo-como-calcular-necessidade-de-capital-de-giro.jpg", "como-calcular-necessidade-de-capital-de-giro"),
    ("artigo-documentos-para-solicitar-credito-empresarial.jpg", "documentos-para-solicitar-credito-empresarial"),
    ("artigo-pronampe-quem-pode-solicitar.png", "pronampe-quem-pode-solicitar"),
    ("artigo-procred-360-publico-e-documentos.png", "procred-360-publico-e-documentos"),
    ("artigo-garantia-para-credito-empresarial.jpg", "garantia-para-credito-empresarial"),
    ("artigo-bndes-para-empresas-como-funciona.webp", "bndes-para-empresas-como-funciona"),
    ("artigo-fgi-tradicional-x-fgi-peac.jpg", "fgi-tradicional-x-fgi-peac"),
    ("artigo-capital-de-giro-pronampe-procred-360-ou-bndes.png", "capital-de-giro-pronampe-procred-360-ou-bndes"),
    ("artigo-pedido-de-credito-negado-o-que-fazer.jpg", "pedido-de-credito-negado-o-que-fazer"),
    ("artigo-como-comparar-credito-empresarial-pelo-cet.jpg", "como-comparar-credito-empresarial-pelo-cet"),
    ("artigo-linhas-bndes-capital-de-giro-finame-cartao.png", "linhas-bndes-capital-de-giro-finame-cartao"),
]


def crop_to_ratio(im, target_ratio):
    w, h = im.size
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        new_w = round(h * target_ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    else:
        new_h = round(w / target_ratio)
        top = (h - new_h) // 2
        return im.crop((0, top, w, top + new_h))


for src_name, slug in jobs:
    src_path = os.path.join(SRC, src_name)
    im = Image.open(src_path).convert("RGB")

    main = crop_to_ratio(im, MAIN_W / MAIN_H).resize((MAIN_W, MAIN_H), Image.LANCZOS)
    main_path = os.path.join(DST, slug + ".jpg")
    main.save(main_path, "JPEG", quality=85, optimize=True)

    thumb = crop_to_ratio(im, 1.0).resize((THUMB, THUMB), Image.LANCZOS)
    thumb_path = os.path.join(DST, slug + "-thumb.jpg")
    thumb.save(thumb_path, "JPEG", quality=85, optimize=True)

    print(slug, os.path.getsize(main_path), "+", os.path.getsize(thumb_path), "bytes")
