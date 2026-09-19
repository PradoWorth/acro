# -*- coding: utf-8 -*-
"""
Programas públicos de crédito e garantia (BNDES, PEAC FGI, Pronampe e
Procred 360): página de referência sobre os mecanismos que ampliam o
enquadramento de empresas elegíveis, com um simulador educativo logo no início da página.

O simulador roda inteiramente no navegador — nenhum dado é enviado a lugar
nenhum — e usa as regras gerais publicadas de cada programa (teto de valor,
fórmula de taxa, prazo máximo). Ele existe para dar uma ordem de grandeza,
não uma proposta: o resultado é sempre rotulado como estimativa, e o texto
deixa claro que a condição final depende da análise da instituição
financeira responsável, do enquadramento real da empresa e da variação da
Selic ao longo do contrato.
"""
import json
import build as B
from content.conteudos import ARTICLES

# Referência de Selic usada só para ilustrar a conta do simulador — as taxas
# de Pronampe e Procred 360 são pós-fixadas (Selic + spread), então o
# resultado muda conforme o Copom se reúne. Ver nota de rodapé do simulador.
#
# É o único dado de mercado volátil que alimenta um número que o visitante vê
# numa página de conversão. Por isso mora aqui, e só aqui: o simulador, a nota
# de rodapé e o aviso do fim da página derivam todos destas constantes, então
# valor e data não têm como divergir. A data fica em AAAA-MM, legível por
# máquina, para o preflight.py conseguir avisar quando envelhecer — dado
# volátil que ninguém percebe envelhecendo é exatamente o que se quer evitar.
# O rótulo em português é derivado, nunca escrito à mão em outro lugar.
SELIC_REF = 14.00
SELIC_REF_MES = "2026-09"

_MESES_PT = ("janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")


def _mes_por_extenso(aaaa_mm):
    """Converte 'AAAA-MM' no rótulo em português usado nos textos.

    Quebra o build de propósito se o formato estiver errado, em vez de gerar
    o site com uma data estranha na página: o erro aparece na hora de montar,
    não depois de publicado. A mensagem diz o que consertar, porque um
    ValueError cru de desempacotamento não diria nada a quem só editou a
    constante para atualizar a Selic.
    """
    partes = aaaa_mm.split("-")
    erro = (f"SELIC_REF_MES={aaaa_mm!r} inválido em content/programas.py. "
            f"Use 'AAAA-MM', por exemplo '2026-09'.")
    if len(partes) != 2:
        raise ValueError(erro)
    try:
        ano, mes = int(partes[0]), int(partes[1])
    except ValueError:
        raise ValueError(erro) from None
    if not 1 <= mes <= 12:
        raise ValueError(erro + f" Mês {mes} não existe.")
    return f"{_MESES_PT[mes - 1]} de {ano}"


SELIC_REF_DATA = _mes_por_extenso(SELIC_REF_MES)

PROGRAMS = [
    {
        "slug": "bndes",
        "nome": "BNDES",
        "kicker": "Banco Nacional de Desenvolvimento",
        "resumo": "Não é uma linha única, e sim o banco de fomento por trás de várias linhas de repasse: Finame (máquinas e equipamentos), Finem (projetos de investimento maiores) e Cartão BNDES (compras a fornecedores cadastrados), entre outras.",
        "rows": [
            ("Para quem", "Empresas de todos os portes, com linhas específicas para micro e pequenas"),
            ("Como chega até a empresa", "De forma indireta, por bancos e financeiras credenciados; o BNDES raramente contrata direto com quem não é grande empresa"),
            ("O que financia", "Máquinas, equipamentos, obras, projetos de expansão e, pelo Cartão BNDES, insumos e serviços"),
            ("Taxa", "Composta por três fatores (custo do BNDES, spread do BNDES e spread do agente financeiro), por isso varia bastante conforme o banco repassador"),
            ("Prazo", "Varia por linha, de alguns anos até prazos longos em projetos de investimento"),
        ],
        "nota": "Por depender do banco repassador escolhido, o BNDES fica de fora do simulador abaixo: a taxa final só se conhece cotando com o agente financeiro.",
        "artigo": ("Ver o guia completo do BNDES para empresas", "bndes-para-empresas-como-funciona"),
        "artigo2": ("Ver a diferença entre Finame, Finem e Cartão BNDES", "linhas-bndes-capital-de-giro-finame-cartao"),
    },
    {
        "slug": "peac-fgi",
        "nome": "PEAC FGI",
        "kicker": "Fundo Garantidor para Investimentos",
        "resumo": "Não é uma linha de crédito: é um fundo que garante parte da operação junto ao banco, reduzindo o risco de quem empresta e, com isso, facilitando a aprovação de empresas sem garantia real suficiente.",
        "rows": [
            ("Para quem", "Micro, pequenas e médias empresas, cooperativas e associações com faturamento anual de até R$ 300 milhões"),
            ("Cobertura do fundo", "De 10% a 80% do risco da operação, a critério do banco; o restante continua sob responsabilidade da instituição financeira"),
            ("Valor", "De R$ 1 mil a R$ 10 milhões por CNPJ, por instituição financeira"),
            ("Taxa", "Negociada com o banco, com teto médio regulatório de 1,75% ao mês"),
            ("Prazo", "Até 96 meses, com carência de 12 a 36 meses"),
        ],
        "nota": None,
        "artigo": ("Ver a diferença entre FGI Tradicional e FGI PEAC", "fgi-tradicional-x-fgi-peac"),
    },
    {
        "slug": "pronampe",
        "nome": "Pronampe",
        "kicker": "Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte",
        "resumo": "Linha de capital de giro do governo federal, com garantia do FGO (Fundo Garantidor de Operações), pensada para reduzir a exigência de garantia real de negócios menores.",
        "rows": [
            ("Para quem", "MEI, microempresas e empresas de pequeno porte com faturamento anual de até R$ 4,8 milhões"),
            ("Valor máximo", "Até 50% do faturamento anual, com teto de R$ 500 mil por CNPJ"),
            ("Taxa", "Selic vigente + 6% ao ano, sem tarifa de crédito ou seguro embutidos"),
            ("Prazo", "Até 96 meses, com carência de até 24 meses"),
            ("Garantia", "Em regra, nenhuma garantia real: o FGO cobre parte do risco junto ao banco"),
        ],
        "nota": None,
        "artigo": ("Ver o guia completo do Pronampe", "pronampe-quem-pode-solicitar"),
        "artigo2": ("Como funciona o compartilhamento de faturamento no e-CAC", "como-funciona-o-compartilhamento-de-faturamento-no-e-cac"),
    },
    {
        "slug": "procred-360",
        "nome": "Procred 360",
        "kicker": "Lei nº 14.995/2024",
        "resumo": "Linha mais recente, focada em microempresas e MEI, com uma das taxas mais baixas entre os programas públicos e concessão apoiada em dados de faturamento já declarados à Receita Federal.",
        "rows": [
            ("Para quem", "MEI e microempresas com faturamento anual de até R$ 360 mil"),
            ("Valor máximo", "Até 30% do faturamento anual declarado (até 50% com o selo Mulher Empreendedora), teto de R$ 150 mil"),
            ("Taxa", "5% ao ano + Selic diária"),
            ("Prazo", "Até 60 meses, com carência inicial"),
            ("Garantia", "FGO (Fundo Garantidor de Operações), com aval do governo federal"),
        ],
        "nota": None,
        "artigo": ("Ver o guia completo do Procred 360", "procred-360-publico-e-documentos"),
    },
]

PROGRAM_BY_SLUG = {p["slug"]: p for p in PROGRAMS}
ARTICLES_BY_SLUG = {a["slug"]: a for a in ARTICLES}

# Segunda linha da tabela de cada programa (além de "Para quem", "Taxa" e
# "Prazo", já usados no trilho de 3 fatos do topo — ver _meta_rows): as 2
# linhas restantes de cada programa, reaproveitadas como destaque no painel
# de imagem complementar (ver PROGRAM_HIGHLIGHTS em program_page), em vez de
# escrever um resumo novo sem lastro na própria tabela.
_HIGHLIGHT_LABELS = {
    "bndes": ("Como chega até a empresa", "O que financia"),
    "peac-fgi": ("Cobertura do fundo", "Valor"),
    "pronampe": ("Valor máximo", "Garantia"),
    "procred-360": ("Valor máximo", "Garantia"),
}

# Artigo que compara os 4 programas lado a lado: relevante para as páginas
# isoladas de todos eles, não só de um — por isso fica junto, fora do
# "artigo"/"artigo2" específico de cada PROGRAMS[i].
_ARTIGO_COMPARATIVO = "capital-de-giro-pronampe-procred-360-ou-bndes"

# Regras usadas pelo simulador (só os 3 programas com fórmula pública e
# objetiva de valor/taxa — o BNDES varia por agente financeiro demais para
# caber num cálculo genérico, ver PROGRAMS[0]["nota"]).
SIM_RULES = {
    "pronampe": {"label": "Pronampe", "pct_faturamento": 0.50, "teto": 500000,
                 "spread_aa": 6.0, "prazo_max": 96, "carencia": "até 24 meses"},
    "procred-360": {"label": "Procred 360", "pct_faturamento": 0.30, "teto": 150000,
                     "spread_aa": 5.0, "prazo_max": 60, "carencia": "prazo inicial, conforme contrato"},
    "peac-fgi": {"label": "PEAC FGI", "pct_faturamento": None, "teto": 10000000,
                 "taxa_am_direta": 1.75, "prazo_max": 96, "carencia": "de 12 a 36 meses"},
}

SIM_JS = r"""
const ACR_SIM_RULES = __RULES_JSON__;
const ACR_SELIC = __SELIC__;

function acrSimOnlyDigits(v) { return (v || '').replace(/\D+/g, ''); }
function acrSimBRL(n) {
  return 'R$ ' + Math.round(n).toLocaleString('pt-BR');
}
function acrSimPct(n, casas) {
  return n.toLocaleString('pt-BR', { minimumFractionDigits: casas, maximumFractionDigits: casas }) + '%';
}

function acrSimInit() {
  const form = document.querySelector('[data-sim-form]');
  if (!form) return;
  const reducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const result = document.querySelector('[data-sim-result]');
  const placeholder = document.querySelector('[data-sim-placeholder]');
  const progSel = form.querySelector('[name="programa"]');
  const prazoSel = form.querySelector('[name="prazo"]');

  function fillPrazoOptions() {
    const rule = ACR_SIM_RULES[progSel.value];
    if (!rule) return;
    const opts = [];
    for (let n = 12; n <= rule.prazo_max; n += 12) opts.push(n);
    if (opts[opts.length - 1] !== rule.prazo_max) opts.push(rule.prazo_max);
    prazoSel.innerHTML = opts.map(function (n) {
      return '<option value="' + n + '"' + (n === rule.prazo_max ? ' selected' : '') + '>' + n + ' meses</option>';
    }).join('');
    // Reescrever innerHTML não dispara 'change' no <select> — mas é esse
    // evento que o select customizado (site.js) escuta para redesenhar seu
    // botão/lista visíveis (.cs-trigger/.cs-menu). Sem isto, o <select>
    // real fica com as opções certas, porém o widget visível continua
    // mostrando o conteúdo antigo (ou vazio, na primeira carga da página).
    prazoSel.dispatchEvent(new Event('change'));
  }

  progSel.addEventListener('change', fillPrazoOptions);
  fillPrazoOptions();

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const rule = ACR_SIM_RULES[progSel.value];
    if (!rule) return;

    const faturamento = Number(acrSimOnlyDigits(form.querySelector('[name="faturamento"]').value || '0'));
    const desejado = Number(acrSimOnlyDigits(form.querySelector('[name="valor"]').value || '0'));
    const n = Number(prazoSel.value || rule.prazo_max);

    let elegivel = rule.teto;
    let elegivelPorFaturamento = false;
    if (rule.pct_faturamento) {
      const porFaturamento = faturamento * rule.pct_faturamento;
      if (porFaturamento < rule.teto) { elegivel = porFaturamento; elegivelPorFaturamento = true; }
    }
    const valorAprovado = desejado > 0 ? Math.min(desejado, elegivel) : elegivel;

    let taxaAA, taxaAM;
    if (rule.taxa_am_direta) {
      taxaAM = rule.taxa_am_direta;
      taxaAA = (Math.pow(1 + taxaAM / 100, 12) - 1) * 100;
    } else {
      taxaAA = ACR_SELIC + rule.spread_aa;
      taxaAM = (Math.pow(1 + taxaAA / 100, 1 / 12) - 1) * 100;
    }

    const i = taxaAM / 100;
    const pmt = valorAprovado > 0 ? (valorAprovado * i) / (1 - Math.pow(1 + i, -n)) : 0;
    const custoTotal = pmt * n;

    result.querySelector('[data-sim-elegivel]').textContent = acrSimBRL(valorAprovado);
    result.querySelector('[data-sim-taxa-aa]').textContent = acrSimPct(taxaAA, 1) + ' ao ano';
    result.querySelector('[data-sim-taxa-am]').textContent = acrSimPct(taxaAM, 2) + ' ao mês';
    result.querySelector('[data-sim-prazo]').textContent = n + ' meses';
    result.querySelector('[data-sim-parcela]').textContent = acrSimBRL(pmt) + ' / mês';
    result.querySelector('[data-sim-total]').textContent = acrSimBRL(custoTotal);
    result.querySelector('[data-sim-carencia]').textContent = rule.carencia;

    const warnEl = result.querySelector('[data-sim-warn]');
    if (elegivel <= 0) {
      warnEl.textContent = 'Informe o faturamento anual para calcular o valor elegível.';
      warnEl.hidden = false;
    } else if (desejado > 0 && desejado > elegivel) {
      const motivo = elegivelPorFaturamento
        ? 'limitado a ' + acrSimPct(rule.pct_faturamento * 100, 0) + ' do faturamento anual informado'
        : 'o teto do programa por CNPJ';
      warnEl.textContent = 'O valor solicitado (' + acrSimBRL(desejado) + ') está acima do que o ' + rule.label +
        ' permite neste cenário: ' + motivo + '. A estimativa abaixo já usa o valor máximo elegível de ' +
        acrSimBRL(elegivel) + ', não o valor solicitado.';
      warnEl.hidden = false;
    } else {
      warnEl.hidden = true;
    }

    if (placeholder) placeholder.hidden = true;
    result.hidden = false;
    // Lado a lado no desktop, o resultado já fica visível sem rolar; em
    // telas estreitas as colunas empilham, então vale levar o usuário até
    // ele depois de calcular.
    if (window.matchMedia('(max-width: 899px)').matches) {
      result.scrollIntoView({ block: 'start', behavior: reducedMotion ? 'auto' : 'smooth' });
    }
  });

  const currencyFields = form.querySelectorAll('[data-mask="currency"]');
  currencyFields.forEach(function (input) {
    input.addEventListener('input', function () {
      // Descarta um sufixo de centavos (",50"/".50") antes de raspar os
      // dígitos: sem isso, digitar "1.000,50" virava R$ 100.050 (os
      // centavos entravam como dígitos inteiros a mais) — o simulador só
      // trabalha com reais inteiros, então os centavos digitados por
      // hábito são descartados, não somados ao valor.
      const d = acrSimOnlyDigits(input.value.replace(/[.,]\d{1,2}$/, '')).slice(0, 12);
      input.value = d ? 'R$ ' + Number(d).toLocaleString('pt-BR') : '';
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', acrSimInit);
} else {
  acrSimInit();
}
"""


# Landing de campanha dedicada (ver content/pronampe.py) — hoje só o
# Pronampe tem uma; os outros 3 programas não têm campanha própria, então
# não aparecem aqui. slug -> (título do link, href, texto de apoio).
CAMPAIGN_LINKS = {
    "pronampe": (
        "Simular e solicitar pelo Pronampe 2026",
        "pronampe-2026.html",
        "Veja as condições disponíveis para sua empresa e envie sua solicitação diretamente "
        "para nossa equipe.",
    ),
}

# Item 138: os mesmos 3 pontos concretos que já abrem a landing da
# campanha (ver .pronampe-checks em content/pronampe.py) — reaproveitados
# aqui, não reescritos, para o callout desta página prometer exatamente o
# que a página de destino cumpre.
CAMPAIGN_HIGHLIGHTS = {
    "pronampe": ["Até R$ 500 mil disponíveis", "96 meses para amortização", "Carência de até 24 meses"],
}

_CC_ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
                   'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                   '<circle cx="12" cy="12" r="9.6"/><path d="M8 12.3l2.6 2.6L16.2 9"/></svg>')
_CC_ICON_ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                   'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                   '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def _campaign_callout(path, slug):
    """Card de destaque para a landing de campanha do programa, quando
    existir (ver CAMPAIGN_LINKS) — pedido do cliente, para que a campanha
    publicada deixe de ser alcançável só por um link dentro de um artigo do
    blog e passe a aparecer nas próprias páginas do programa.

    Item 138: card genérico (`callout callout--fill`, cinza, sem nenhum
    dado concreto) trocado por uma versão própria, mais chamativa e com
    informação real que dá vontade de clicar — pedido do cliente. Selo em
    destaque em vez do rótulo cinza de sechead, os 3 pontos concretos de
    CAMPAIGN_HIGHLIGHTS (mesmo texto da landing, não inventado aqui) e um
    botão com seta. Sai do componente `.callout` genérico (compartilhado
    com o resto do site) para o próprio `.campaigncallout` (ver site.css),
    porque o ajuste é só para este card, não para todo `.callout--fill`
    do site."""
    info = CAMPAIGN_LINKS.get(slug)
    if not info:
        return ""
    title, href, text = info
    checks = CAMPAIGN_HIGHLIGHTS.get(slug, [])
    checks_html = "".join(f"<li>{_CC_ICON_CHECK}<span>{h}</span></li>" for h in checks)
    checks_block = f'<ul class="campaigncallout__checks">{checks_html}</ul>' if checks_html else ""
    return f"""<div class="campaigncallout mt-3">
      <span class="campaigncallout__tag">Campanha ativa</span>
      <h2>{title}</h2>
      <p>{text}</p>
      {checks_block}
      <div class="mt-2">{B.btn(f"Ver condições e solicitar {_CC_ICON_ARROW}", href, path)}</div>
    </div>"""


def _program_section(path, i, p):
    rows_html = B.deflist(p["rows"], split=True)
    nota_html = f'<p class="notice mt-3">{p["nota"]}</p>' if p["nota"] else ""
    artigo_html = (f'<div class="mt-3">{B.tlink(p["artigo"][0], "conteudos/" + p["artigo"][1] + ".html", path)}</div>'
                   if p.get("artigo") else "")
    artigo2_html = (f'<div class="mt-1">{B.tlink(p["artigo2"][0], "conteudos/" + p["artigo2"][1] + ".html", path)}</div>'
                    if p.get("artigo2") else "")
    # Além desta seção-resumo (com âncora, para quem já sabe qual programa
    # quer), cada um também tem uma página isolada própria (ver
    # program_page()), com espaço para imagem e conteúdo específicos — pedido
    # do cliente. As duas convivem: esta seção continua exatamente como era.
    pagina_html = f'<div class="mt-1">{B.tlink("Ver a página completa do " + p["nome"], "programas/" + p["slug"] + ".html", path)}</div>'
    campanha_html = _campaign_callout(path, p["slug"])
    band_cls = "band band--top-rule" if i % 2 else "band band--stone band--top-rule"
    # id âncora (ex.: #pronampe) — permite que outras páginas do site linkem
    # direto para o programa específico, em vez de só para o topo da página.
    return f"""<section class="{band_cls}" id="{p['slug']}">
  <div class="shell">
    {B.sechead(str(i + 1), p["nome"], p["resumo"], note=p["kicker"])}
    <div class="stack-2">
      {rows_html}
      {nota_html}
      {artigo_html}
      {artigo2_html}
      {pagina_html}
      {campanha_html}
    </div>
  </div>
</section>"""


# Perguntas frequentes de fundo de funil sobre os programas — os termos de
# busca "quem pode solicitar", "requisitos" e "garante aprovação" aparecem
# de forma recorrente na pesquisa de SEO do site. Cada resposta reafirma o
# mesmo limite: os programas mudam o enquadramento ou o risco da operação,
# nunca a decisão final, que é sempre da instituição financeira.
FAQ_PROGRAMS = [
    ("Quem pode solicitar o Pronampe?",
     "MEI, microempresas e empresas de pequeno porte com faturamento anual de até R$ 4,8 milhões. "
     "Dentro desse universo, cada instituição financeira ainda aplica sua própria análise de crédito "
     "antes de liberar a operação."),
    ("Qual a diferença entre Pronampe e Procred 360?",
     "O Pronampe atende um público mais amplo (até R$ 4,8 milhões de faturamento anual, teto de R$ 500 "
     "mil por CNPJ). O Procred 360 é mais recente e mais estreito: só MEI e microempresas com faturamento "
     "de até R$ 360 mil, com teto de R$ 150 mil e uma das taxas mais baixas entre os programas públicos. "
     "Na prática, o Procred 360 nasceu para atender quem não se encaixava bem no Pronampe."),
    ("O PEAC FGI garante a aprovação do crédito?",
     "Não. O PEAC FGI é um fundo garantidor: ele cobre entre 10% e 80% do risco da operação junto ao "
     "banco, o que facilita a análise de empresas sem garantia real suficiente, mas a decisão final, a "
     "taxa e o prazo continuam sendo definidos pela instituição financeira."),
    ("Como funciona o BNDES para empresas?",
     "O BNDES não é uma linha única. É o banco de fomento por trás de várias linhas de repasse, como "
     "Finame, Finem e Cartão BNDES. Na maior parte dos casos, o acesso é indireto, por bancos e "
     "financeiras credenciados, e a taxa final varia conforme o agente financeiro escolhido."),
    ("Esses programas garantem a aprovação do crédito?",
     "Não. Pronampe, Procred 360, PEAC FGI e as linhas do BNDES reduzem a exigência de garantia real ou "
     "ampliam o conjunto de instituições dispostas a analisar a operação, mas a aprovação, a taxa e o "
     "prazo finais sempre dependem da análise de crédito do banco ou da cooperativa responsável."),
]


_SIM_PROGRAM_LABELS = {"pronampe": "Pronampe", "procred-360": "Procred 360", "peac-fgi": "PEAC FGI"}


def _simulator_section(path, slugs=None):
    """
    Bloco do simulador (formulário + resultado + script). `slugs` restringe
    as opções do seletor de programa — usado nas páginas isoladas de
    Pronampe, Procred 360 e PEAC FGI, cada uma trazendo o simulador já
    travado no próprio programa (sem o BNDES, que não entra aqui: ver a nota
    em PROGRAMS[0], a taxa depende do agente financeiro escolhido, não tem
    fórmula pública única). Sem `slugs`, mostra as 3 opções — é o caso da
    página de visão geral (hub).
    """
    slugs = slugs or list(_SIM_PROGRAM_LABELS.keys())
    options = "".join(f'<option value="{slug}">{_SIM_PROGRAM_LABELS[slug]}</option>' for slug in slugs)
    intro = ("Informe o faturamento anual e o valor desejado. O resultado aparece "
             "ao lado, sem sair do formulário: dá para simular quantas vezes quiser. "
             "A conta roda aqui no navegador, e nenhum dado é enviado."
             if len(slugs) == 1 else
             "Escolha um programa, informe o faturamento anual e o valor desejado. O resultado "
             "aparece ao lado, sem sair do formulário: dá para simular quantas vezes quiser. A "
             "conta roda aqui no navegador, e nenhum dado é enviado.")
    programa_field = (f'<input type="hidden" id="sim-programa" name="programa" value="{slugs[0]}">'
                       if len(slugs) == 1 else
                       f"""<div class="field">
              <label for="sim-programa">Programa</label>
              <select id="sim-programa" name="programa" required>{options}</select>
            </div>""")

    sim_rules = {slug: SIM_RULES[slug] for slug in slugs}
    sim_json = json.dumps(sim_rules, ensure_ascii=False)
    script = SIM_JS.replace("__RULES_JSON__", sim_json).replace("__SELIC__", str(SELIC_REF))

    return f"""<section class="band">
  <div class="shell">
  <div class="toolcard">
    {B.sechead("Simulador", "Estimativa rápida de valor, taxa e parcela", intro)}
    <div class="cols cols--1-1 mt-3">
      <div>
        <form data-sim-form novalidate>
          <div class="fgrid fgrid--2">
            {programa_field}
            <div class="field">
              <label for="sim-prazo">Prazo desejado</label>
              <select id="sim-prazo" name="prazo" required></select>
            </div>
            <div class="field">
              <label for="sim-faturamento">Faturamento anual da empresa</label>
              <input type="text" inputmode="numeric" id="sim-faturamento" name="faturamento" data-mask="currency" placeholder="R$ 0" required>
            </div>
            <div class="field">
              <label for="sim-valor">Valor que você gostaria de captar</label>
              <input type="text" inputmode="numeric" id="sim-valor" name="valor" data-mask="currency" placeholder="R$ 0 (opcional, deixe em branco para ver o teto)">
            </div>
          </div>
          <div class="formfoot formfoot--wide" style="border-top:0;padding-top:0;margin-top:1.5rem">
            <button type="submit" class="btn">Calcular estimativa</button>
          </div>
        </form>
      </div>

      <div class="callout">
        <div data-sim-placeholder>
          <span class="tag">Resultado</span>
          <p class="small muted mt-2" style="margin-bottom:0">Preencha os dados ao lado e clique em "Calcular estimativa" para ver aqui o valor, a taxa e a parcela estimados.</p>
        </div>
        <div data-sim-result hidden role="status" aria-live="polite">
          {B.sechead("Resultado", "Estimativa para o cenário informado")}
          <p data-sim-warn hidden class="notice mt-2">Informe o faturamento anual para calcular o valor elegível.</p>
          <div class="deflist mt-2">
            <div class="deflist__row"><dt>Valor estimado elegível</dt><dd data-sim-elegivel class="figures"></dd></div>
            <div class="deflist__row"><dt>Taxa estimada</dt><dd><span data-sim-taxa-aa class="figures"></span> (<span data-sim-taxa-am class="figures"></span>)</dd></div>
            <div class="deflist__row"><dt>Prazo simulado</dt><dd data-sim-prazo class="figures"></dd></div>
            <div class="deflist__row"><dt>Carência típica</dt><dd data-sim-carencia></dd></div>
            <div class="deflist__row"><dt>Parcela estimada</dt><dd data-sim-parcela class="figures"></dd></div>
            <div class="deflist__row"><dt>Custo total estimado do período</dt><dd data-sim-total class="figures"></dd></div>
          </div>
          <p class="xs muted mt-3">Cálculo ilustrativo, com a fórmula pública de cada programa e uma Selic de referência de {SELIC_REF_DATA} ({B.esc(str(SELIC_REF).replace('.', ','))}% ao ano): a Selic muda a cada reunião do Copom, e Pronampe e Procred 360 têm taxa pós-fixada, então a parcela real varia ao longo do contrato. Não considera seu perfil de crédito, não consulta bureau e não é uma simulação da instituição financeira. O valor, a taxa e a aprovação finais dependem da análise do banco ou da cooperativa responsável.</p>
          <div class="mt-3">
            {B.btn("Verificar enquadramento com um especialista", "contato.html", path, variant="btn--block", attrs=' data-lead-modal')}
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</section>
<script>{script}</script>"""


def _meta_rows(rows, labels):
    """Extrai, na ordem pedida, as linhas de `rows` cujo rótulo começa com
    algum dos prefixos em `labels` — usado para montar o trilho de 3 fatos do
    topo de cada página (pagehead), reaproveitando os mesmos dados da tabela
    "Como funciona", nunca um resumo escrito à parte."""
    out = []
    for label in labels:
        for k, v in rows:
            if k.startswith(label):
                out.append((k, v))
                break
    return out


def program_page(slug):
    p = PROGRAM_BY_SLUG[slug]
    path = f"programas/{slug}.html"
    trail = [("Início", "index.html"), ("Programas de crédito", "programas.html"), (p["nome"], None)]

    meta = _meta_rows(p["rows"], ("Para quem", "Taxa", "Prazo"))
    body = B.pagehead(path, trail, p["kicker"], p["nome"], p["resumo"], meta,
                       variant=PROGRAMS.index(p), image_slot="programa-" + slug)

    campanha_html = _campaign_callout(path, slug)
    if campanha_html:
        # Fica logo no topo, antes de qualquer conteúdo informativo: para
        # quem já sabe que quer o Pronampe e só quer simular e enviar os
        # dados, é a ação mais direta da página, pedido do cliente.
        # Item 140: padding-block trocado de "band" (64-80px) para
        # "band--tight" (24px) em cima e embaixo, a pedido do cliente, que
        # achou o respiro em volta deste card grande demais.
        body += f'<section class="band band--tight"><div class="shell shell--tight">{campanha_html}</div></section>'

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Como funciona", p["nome"])}
    <div class="stack-2">
      {B.deflist(p["rows"], split=True)}
      {f'<p class="notice mt-3">{p["nota"]}</p>' if p["nota"] else ""}
    </div>
  </div>
</section>"""

    # Painel com a segunda imagem da página (complementar à do topo) e 2
    # destaques — as 2 linhas da própria tabela acima que não entraram no
    # trilho de fatos do pagehead (ver _HIGHLIGHT_LABELS), não um resumo
    # novo: mesma fonte de dados, outro formato de leitura.
    rows_by_label = dict(p["rows"])
    hl_labels = _HIGHLIGHT_LABELS[slug]
    bullets = [f"<strong>{label}:</strong> {rows_by_label[label]}" for label in hl_labels]
    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.media_aside(path, "programa-" + slug + "-2", "pagehead-" + str((PROGRAMS.index(p) + 1) % 3),
                   p["kicker"], "Como o " + p["nome"] + " funciona na prática", p["resumo"], bullets,
                   cta=("Falar com um especialista", "contato.html"))}
  </div>
</section>"""

    if slug in SIM_RULES:
        body += _simulator_section(path, [slug])

    # Conteúdos relacionados (com imagem, quando o artigo tiver uma própria)
    # — os 1 ou 2 artigos específicos do programa, mais o comparativo entre
    # os 4 programas, que serve às 4 páginas igualmente. Fica perto do fim,
    # antes do rodapé, como pedido: é o espaço reservado para quem quiser
    # ler mais sobre o assunto antes de sair da página.
    rel_slugs = [s for s in (p.get("artigo", (None, None))[1], p.get("artigo2", (None, None))[1], _ARTIGO_COMPARATIVO) if s]
    seen = set()
    rel_articles = []
    for s in rel_slugs:
        if s in seen or s not in ARTICLES_BY_SLUG:
            continue
        seen.add(s)
        rel_articles.append(ARTICLES_BY_SLUG[s])
    if rel_articles:
        rows_html = "".join(
            B.artrow(path, "conteudos/" + a["slug"] + ".html", a.get("image"), a["category"],
                     a["title"], a["excerpt"], foot=a["date_label"])
            for a in rel_articles
        )
        body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Para saber mais", "Conteúdos sobre " + p["nome"] + ".")}
    <div class="artlist">{rows_html}</div>
  </div>
</section>"""

    faq = [item for item in FAQ_PROGRAMS if p["nome"].split()[0].lower() in item[0].lower()
           or (slug == "pronampe" and "pronampe" in item[0].lower())
           or (slug == "procred-360" and "procred 360" in item[0].lower())]
    # Fecha sempre com a pergunta geral ("esses programas garantem a
    # aprovação?"), presente em todas as páginas de programa — mesmo limite
    # institucional repetido em todo lugar que fala de crédito facilitado.
    geral = FAQ_PROGRAMS[-1]
    if geral not in faq:
        faq.append(geral)
    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Sobre " + p["nome"] + ".")}
    {B.accordion(faq, "faq-" + slug)}
    <p class="notice mt-3">Regras, taxas, tetos e prazos seguem a legislação e as normas do programa, com verificação em {SELIC_REF_DATA}. Nenhuma informação desta página constitui oferta, simulação vinculante ou promessa de aprovação.</p>
  </div>
</section>"""

    others = [x for x in PROGRAMS if x["slug"] != slug]
    rel_rows = [(o["nome"], o["kicker"], "programas/" + o["slug"] + ".html", "Ver a página") for o in others]
    body += f"""<section class="band band--stone band--snug">
  <div class="shell">
    {B.sechead("Outros programas", "Frequentemente avaliados em conjunto.")}
    {B.linkcards(path, rel_rows)}
    <div class="mt-3">{B.tlink("Ver todos, lado a lado, na página de programas", "programas.html", path)}</div>
  </div>
</section>"""

    body += B.cta_band(
        path, f"Não sabe se a empresa se enquadra no {p['nome']}?",
        "Verificamos o enquadramento como parte da estruturação, sem custo e sem compromisso.",
        secondary=("Ver as 8 estruturas de crédito", "solucoes.html"), tone="petrol")

    # Título de SEO mais curto que o kicker de exibição da página, só para
    # caber no limite de exibição do Google (~60 caracteres) junto do sufixo
    # institucional — o kicker completo (ex.: "Lei nº 14.995/2024") continua
    # aparecendo normalmente no topo da página (pagehead), só não no <title>.
    seo_kicker = {
        "bndes": "Banco Nacional de Desenvolvimento",
        "peac-fgi": "Fundo Garantidor de Investimentos",
        "pronampe": "Capital de giro com aval do FGO",
        "procred-360": "Crédito para microempresas",
    }[slug]

    return {
        "path": path, "nav_key": None, "over": True,
        "title": f"{p['nome']}: {seo_kicker} | Acrópole Capital",
        "desc": B.fit_desc(p["resumo"], f"Como funciona o {p['nome']}, na estruturação de crédito da Acrópole Capital."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(faq)],
    }


def pages():
    path = "programas.html"
    trail = [("Início", "index.html"), ("Programas de crédito", None)]

    body = B.pagehead(
        path, trail, "Programas públicos", "Programas e mecanismos de garantia que usamos na estruturação",
        "Parte do trabalho de estruturação é verificar se a operação se enquadra em algum "
        "programa público de crédito ou garantia. Quando cabe, isso costuma reduzir a "
        "exigência de garantia real ou baixar o custo final. Veja como funcionam os principais.",
        meta=[("Simulador", "Logo abaixo, sem sair desta página"),
              ("Natureza", "Programas de terceiros, não produtos da Acrópole Capital"),
              ("Enquadramento", "Depende do porte e do faturamento da empresa")],
        variant=0, image_slot="programas")

    # --------------------------------------------------------- simulador
    # Fica logo após o cabeçalho, e não ao final da página: é a ferramenta
    # que mais gera ação nesta página, então precisa da maior visibilidade.
    body += _simulator_section(path)

    for i, p in enumerate(PROGRAMS):
        body += _program_section(path, i, p)

    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Sobre Pronampe, Procred 360, PEAC FGI e BNDES.")}
    {B.accordion(FAQ_PROGRAMS, "faq-programas")}
    <p class="notice mt-3">Regras, taxas, tetos e prazos seguem a legislação e as normas de cada programa, com verificação em {SELIC_REF_DATA}. Nenhuma informação desta página constitui oferta, simulação vinculante ou promessa de aprovação.</p>
  </div>
</section>"""

    body += B.cta_band(
        path, "Não sabe em qual desses sua empresa se enquadra?",
        "Verificamos o enquadramento como parte da estruturação, sem custo e sem compromisso.",
        secondary=("Ver as 8 estruturas de crédito", "solucoes.html"), tone="petrol")

    hub_page = {
        "path": path, "nav_key": None, "over": True,
        "title": "Pronampe, Procred 360, BNDES e PEAC FGI | Acrópole Capital",
        "desc": ("Como funcionam Pronampe, Procred 360, BNDES e PEAC FGI: quem pode solicitar, valor, "
                 "taxa e prazo de cada programa, com simulador rápido de estimativa."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(FAQ_PROGRAMS)],
    }
    return [hub_page] + [program_page(p["slug"]) for p in PROGRAMS]
