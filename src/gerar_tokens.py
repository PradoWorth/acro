# -*- coding: utf-8 -*-
"""
Gera o pacote de tokens em formato dev a partir do :root de site.css.

Etapa 10.1 do processo do Studio Responsivo. A fonte da verdade continua
sendo o CSS do site — este script LÊ de lá e converte, em vez de manter uma
segunda lista à mão que inevitavelmente descolaria da primeira. Rode de novo
depois de mexer nos tokens e os cinco formatos saem atualizados juntos.

    python3 gerar_tokens.py [destino]        # padrão: ../tokens

Saída (estrutura pedida pela skill):
    tokens/primitive/   valores crus (cores, tamanhos, tempos)
    tokens/semantic/    o que cada valor significa em uso
    tokens/components/  o que é específico de um componente
Cada camada em CSS, SCSS, JSON (Style Dictionary), TS e config do Tailwind.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(RAIZ, "static", "assets", "css", "site.css")
DESTINO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(RAIZ), "tokens")

# Como cada token é classificado. A ordem importa: o primeiro padrão que
# casar decide. Primitivo é o valor cru; semântico é o papel que ele cumpre;
# de componente é o que só existe dentro de uma peça.
CLASSES = [
    ("components", re.compile(r"^--(cta-|shadow-button|r-button|r-card|r-input|r-tag|band$)")),
    ("semantic",   re.compile(r"^--(bg|fg|ink|paper|slate|accent|rule|surface|brand|danger|ok|"
                              r"z-|dur|ease|stroke|t-|track-|sp-|shell|gut|shadow)")),
    ("primitive",  re.compile(r".")),
]

GRUPOS = [
    ("color",      re.compile(r"^--(petrol|iris|soft-iris|cobalt|studio-slate|obsidian|white|cloud|"
                              r"mist|graphite|iron|noir|accent|ink|paper|slate|surface|bg$|fg$|"
                              r"rule|danger|ok$|brass|cta-)")),
    ("typography", re.compile(r"^--(t-|track-|sans$)")),
    ("space",      re.compile(r"^--(sp-|gut$|shell$|band$)")),
    ("radius",     re.compile(r"^--r-")),
    ("elevation",  re.compile(r"^--shadow")),
    ("motion",     re.compile(r"^--(dur|ease)")),
    ("zindex",     re.compile(r"^--z-")),
    ("stroke",     re.compile(r"^--stroke")),
    ("other",      re.compile(r".")),
]


def primeiro(pares, nome):
    for rotulo, padrao in pares:
        if padrao.search(nome):
            return rotulo
    return pares[-1][0]


def ler_root():
    """Extrai os pares do bloco :root, ignorando comentários."""
    css = open(CSS, encoding="utf-8").read()
    m = re.search(r":root\s*\{(.*?)\n\}", css, re.S)
    if not m:
        raise SystemExit("bloco :root não encontrado em site.css")
    corpo = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
    tokens = []
    for linha in corpo.split(";"):
        linha = linha.strip()
        mm = re.match(r"^(--[a-z0-9-]+)\s*:\s*(.+)$", linha, re.S)
        if mm:
            tokens.append((mm.group(1), " ".join(mm.group(2).split())))
    return tokens


def camel(nome):
    partes = nome.lstrip("-").split("-")
    return partes[0] + "".join(p.capitalize() for p in partes[1:])


def escrever(caminho, conteudo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho


def main():
    tokens = ler_root()
    por_camada = {"primitive": [], "semantic": [], "components": []}
    for nome, valor in tokens:
        por_camada[primeiro(CLASSES, nome)].append((nome, valor))

    escritos = []
    cabecalho = ("/* Gerado por src/gerar_tokens.py a partir de site.css.\n"
                 "   Não edite à mão: a fonte da verdade é o :root do site. */\n")

    for camada, itens in por_camada.items():
        if not itens:
            continue
        # CSS
        linhas = [f"  {n}: {v};" for n, v in itens]
        escritos.append(escrever(os.path.join(DESTINO, camada, f"{camada}.css"),
                                 cabecalho + ":root {\n" + "\n".join(linhas) + "\n}\n"))
        # SCSS
        scss = [f"${n.lstrip('-')}: {v};" for n, v in itens]
        escritos.append(escrever(os.path.join(DESTINO, camada, f"_{camada}.scss"),
                                 cabecalho.replace("/*", "//").replace("*/", "")
                                 + "\n".join(scss) + "\n"))
        # JSON no formato Style Dictionary, agrupado por tipo
        sd = {}
        for n, v in itens:
            g = primeiro(GRUPOS, n)
            sd.setdefault(g, {})[n.lstrip("-")] = {"value": v}
        escritos.append(escrever(os.path.join(DESTINO, camada, f"{camada}.tokens.json"),
                                 json.dumps(sd, ensure_ascii=False, indent=2) + "\n"))
        # TypeScript
        ts = [f"  {camel(n)}: '{v}'," for n, v in itens]
        escritos.append(escrever(os.path.join(DESTINO, camada, f"{camada}.ts"),
                                 cabecalho + f"export const {camada} = {{\n"
                                 + "\n".join(ts) + "\n} as const;\n\n"
                                 + f"export type {camada.capitalize()}Token = keyof typeof {camada};\n"))

    # Tailwind: um arquivo só, apontando para as CSS Variables (assim o tema
    # continua trocável em runtime em vez de congelar o valor no build).
    todos = [t for itens in por_camada.values() for t in itens]
    def secao(padrao, corta):
        out = {}
        for n, _ in todos:
            if re.match(padrao, n):
                chave = re.sub(corta, "", n.lstrip("-"))
                out[chave] = f"var({n})"
        return out
    tw = {
        "theme": {
            "extend": {
                "colors": secao(r"^--(bg|fg|ink|paper|slate|accent|rule|surface|brass|iris|cobalt|"
                                r"petrol|obsidian|cloud|mist|graphite|iron|danger|ok)", r"^"),
                "spacing": secao(r"^--sp-", r"^sp-"),
                "borderRadius": secao(r"^--r-", r"^r-"),
                "fontSize": secao(r"^--t-", r"^t-"),
                "letterSpacing": secao(r"^--track-", r"^track-"),
                "zIndex": secao(r"^--z-", r"^z-"),
                "transitionDuration": secao(r"^--dur", r"^dur-?"),
                "transitionTimingFunction": secao(r"^--ease", r"^ease-?"),
                "borderWidth": secao(r"^--stroke-", r"^stroke-"),
                "boxShadow": secao(r"^--shadow-", r"^shadow-"),
                "maxWidth": {"shell": "var(--shell)"},
            }
        }
    }
    escritos.append(escrever(os.path.join(DESTINO, "tailwind.tokens.js"),
                             "// Gerado por src/gerar_tokens.py a partir de site.css.\n"
                             "// Aponta para as CSS Variables de propósito: o tema segue\n"
                             "// trocável em runtime, em vez de congelar o valor no build.\n"
                             "module.exports = " + json.dumps(tw, ensure_ascii=False, indent=2) + ";\n"))

    print(f"{len(tokens)} tokens lidos de site.css")
    for camada, itens in por_camada.items():
        print(f"  {camada:<11} {len(itens):>3} tokens")
    print(f"\n{len(escritos)} arquivos em {DESTINO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
