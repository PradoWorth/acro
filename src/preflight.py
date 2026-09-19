# -*- coding: utf-8 -*-
"""
Trava de publicação.

Roda depois do build e recusa a publicação enquanto faltar dado obrigatório ou
sobrar placeholder no HTML gerado. A intenção é simples: tornar impossível
subir o site com "[Nome do responsável]" ou um WhatsApp que não existe.

    python3 preflight.py        -> código 0 se pode publicar, 1 se não pode
"""
import os
import re
import sys
from datetime import date as _date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content.site import CONTATO, SITE  # noqa: E402
from content.programas import SELIC_REF, SELIC_REF_DATA, SELIC_REF_MES  # noqa: E402

# Quantos meses a referência de Selic pode ter antes de virar aviso. O Copom
# se reúne a cada ~45 dias, então em quatro meses já se passaram duas ou três
# reuniões: a conta ilustrativa do simulador começa a descolar da realidade.
# Não bloqueia a publicação — o número está declarado com data e com a
# ressalva de que é pós-fixado —, mas deixa de envelhecer em silêncio.
SELIC_MESES_ATE_AVISAR = 4

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT) if os.path.basename(ROOT) == "src" else ROOT
DIST = os.path.join(BASE, "dist")

# Sem estes o site não deve ir ao ar: são os caminhos por onde o lead chega.
OBRIGATORIOS = {
    "whatsapp": "Número de WhatsApp comercial (só dígitos, com país e DDD)",
    "email": "E-mail comercial",
}

# Recomendados: não travam a publicação, mas enfraquecem a percepção de solidez.
RECOMENDADOS = {
    "endereco": "Endereço comercial",
    "horario": "Horário de atendimento",
    "linkedin": "URL do LinkedIn",
    "instagram": "URL do Instagram",
}

# Placeholders de conteúdo que ainda vivem nos textos das páginas.
PADROES_TEXTO = [
    (r"\[Nome do responsável\]", "Nomes da equipe na página /sobre"),
    (r"\[Formação, trajetória[^\]]*\]", "Biografias da equipe na página /sobre"),
    (r"\[Cargo[^\]]*\]", "Cargos da equipe na página /sobre"),
    (r"\[data de publicação\]", "Data nos documentos legais"),
    (r"\[Cidade/UF\]", "Foro nos Termos de Uso"),
    (r"\[definir URLs[^\]]*\]", "Perfis sociais no rodapé"),
]


def cor(txt, c):
    return f"\033[{c}m{txt}\033[0m" if sys.stdout.isatty() else txt


def main():
    bloqueios, avisos = [], []

    for chave, descricao in OBRIGATORIOS.items():
        if not CONTATO.get(chave):
            bloqueios.append(f"CONTATO['{chave}'] não preenchido — {descricao}")

    for chave, descricao in RECOMENDADOS.items():
        if not CONTATO.get(chave):
            avisos.append(f"CONTATO['{chave}'] não preenchido — {descricao}")

    # Dado de mercado volátil: avisa antes de a página começar a mentir sozinha.
    try:
        ano_ref, mes_ref = (int(x) for x in SELIC_REF_MES.split("-"))
        hoje = _date.today()
        meses = (hoje.year - ano_ref) * 12 + (hoje.month - mes_ref)
        if meses >= SELIC_MESES_ATE_AVISAR:
            avisos.append(
                f"Selic de referência do simulador ({str(SELIC_REF).replace('.', ',')}% "
                f"de {SELIC_REF_DATA}) está com {meses} meses — confirme a taxa vigente "
                f"e atualize SELIC_REF e SELIC_REF_MES em content/programas.py"
            )
    except Exception as e:  # formato inesperado é problema de manutenção, não silêncio
        avisos.append(f"SELIC_REF_MES não pôde ser lido ({e}) — esperado 'AAAA-MM'")

    # Varredura do HTML gerado
    if os.path.isdir(DIST):
        achados = {}
        for root, _, names in os.walk(DIST):
            for n in names:
                if not n.endswith(".html"):
                    continue
                raw = open(os.path.join(root, n), encoding="utf-8").read()
                rel = os.path.relpath(os.path.join(root, n), DIST)
                for pad, desc in PADROES_TEXTO:
                    if re.search(pad, raw):
                        achados.setdefault(desc, set()).add(rel)
                # qualquer [colchete] restante que não seja de código
                for m in re.finditer(r"\[[A-ZÀ-Ú][^\]\n]{3,60}\]", raw):
                    achados.setdefault(f"Placeholder solto: {m.group(0)}", set()).add(rel)
        for desc, arquivos in sorted(achados.items()):
            lista = ", ".join(sorted(arquivos)[:3])
            extra = f" (+{len(arquivos) - 3})" if len(arquivos) > 3 else ""
            bloqueios.append(f"{desc} — em {lista}{extra}")
    else:
        bloqueios.append("dist/ não encontrado. Rode build.py antes.")

    print()
    if bloqueios:
        print(cor(f"NÃO PUBLICAR — {len(bloqueios)} pendência(s) obrigatória(s):", "1;31"))
        for b in bloqueios:
            print("  ×", b)
    else:
        print(cor("Pendências obrigatórias: nenhuma.", "1;32"))

    if avisos:
        print(cor(f"\nRecomendado antes de divulgar ({len(avisos)}):", "1;33"))
        for a in avisos:
            print("  !", a)

    print("\nPreencha em content/site.py, no bloco CONTATO, e rode:")
    print("  python3 build.py && python3 preflight.py\n")
    return 1 if bloqueios else 0


if __name__ == "__main__":
    sys.exit(main())
