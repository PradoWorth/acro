# -*- coding: utf-8 -*-
"""
Diagnóstico rápido: ferramenta interativa client-side.

Importante por design: não pede valor de faturamento nem devolve taxa, prazo
ou valor liberável. Isso não é uma calculadora de crédito — é um roteador
qualitativo entre as 8 estruturas, com a mesma cautela do resto do site.
Nenhum dado do visitante é enviado a lugar nenhum; tudo roda no navegador.
"""
from content.site import SOLUTIONS
import build as B


QUESTIONS_JS = r"""
const ACR_SOL = __SOL_JSON__;

function acrRecommend(a) {
  // a = { perfil, necessidade, garantia, porte, obra }
  const out = [];
  const add = (slug, why) => { if (!out.find(o => o.slug === slug)) out.push({ slug, why }); };

  if (a.necessidade === 'nao_sei') {
    return { empty: true };
  }

  if (a.necessidade === 'liquidez') {
    if (a.garantia === 'veiculo') add('auto-equity', 'Você tem um veículo disponível e quer liquidez rápida: é o cenário em que essa estrutura costuma caber, desde que o prazo do contrato seja curto o suficiente para a depreciação do bem.');
    if (a.garantia === 'imovel') add('home-equity', 'Com imóvel disponível, o home equity costuma trazer custo bem menor que crédito sem garantia, ao custo de comprometer o bem como lastro.');
    if (a.garantia === 'recebiveis' && a.perfil === 'pj') { add('capital-de-giro', 'Recebíveis ou faturamento consistente sustentam uma linha de giro sem precisar de garantia real.'); add('mercado-de-capitais', 'Se a carteira de recebíveis for recorrente e relevante, antecipá-la de forma estruturada costuma custar menos do que o desconto avulso.'); }
    if (!out.length) add('como-funciona', 'Sem um ativo claro para lastrear a operação, o primeiro passo é uma conversa de diagnóstico para mapear o que está disponível.');
  }

  if (a.necessidade === 'reduzir_custo') {
    if (a.garantia === 'imovel') add('home-equity', 'Substituir dívida cara por uma estrutura com garantia imobiliária costuma ser a alavanca mais forte de redução de custo, quando o saldo e o prazo fazem sentido.');
    else add('credito-pj', 'Sem garantia real disponível, o caminho costuma ser comparar instituições e mecanismos públicos de garantia para reduzir o custo do passivo atual.');
  }

  if (a.necessidade === 'crescer') {
    if (a.perfil === 'pj' && a.porte === 'grande') add('estruturacao-de-credito', 'Operações a partir de R$ 500 mil costumam exigir desenho sob medida, combinando mais de uma fonte e mais de uma garantia.');
    else { add('capital-de-giro', 'Para sustentar crescimento sem apertar o caixa, o ponto de partida é dimensionar a necessidade real de giro.'); add('credito-pj', 'Vale comparar instituições e verificar enquadramento em programas como Pronampe ou PEAC FGI.'); }
  }

  if (a.necessidade === 'imovel') {
    if (a.obra === 'sim') add('aquisicao-e-construcao', 'Como envolve construção, terreno e obra tendem a ser tratados como uma operação só, com liberação por etapa.');
    else add('financiamento', 'Para adquirir um imóvel pronto preservando caixa, financiamento costuma ser o ponto de partida.');
  }

  if (!out.length) add('solucoes', 'Nenhuma combinação óbvia surgiu das respostas. Vale uma conversa para mapear o cenário com mais detalhe.');
  return { empty: false, items: out.slice(0, 2) };
}

function acrDiagInit() {
  const form = document.querySelector('[data-diag-form]');
  if (!form) return;
  const reducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const scrollBehavior = reducedMotion ? 'auto' : 'smooth';
  const result = document.querySelector('[data-diag-result]');
  const empty = document.querySelector('[data-diag-empty]');
  const list = document.querySelector('[data-diag-list]');
  const portoField = document.querySelector('[data-field-porte]');
  const obraField = document.querySelector('[data-field-obra]');

  function sync() {
    const perfil = form.querySelector('input[name="perfil"]:checked');
    const necessidade = form.querySelector('input[name="necessidade"]:checked');
    portoField.hidden = !(perfil && perfil.value === 'pj' && necessidade && necessidade.value === 'crescer');
    obraField.hidden = !(necessidade && necessidade.value === 'imovel');
  }
  form.addEventListener('change', sync);
  sync();

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const fd = new FormData(form);
    const a = {
      perfil: fd.get('perfil') || '', necessidade: fd.get('necessidade') || '',
      garantia: fd.get('garantia') || '', porte: fd.get('porte') || '',
      obra: fd.get('obra') || '',
    };
    if (!a.necessidade) {
      const f = form.querySelector('.field');
      if (f) { f.setAttribute('data-invalid', 'true'); f.scrollIntoView({ block: 'center', behavior: scrollBehavior }); }
      return;
    }
    const rec = acrRecommend(a);
    result.hidden = false;
    result.scrollIntoView({ block: 'center', behavior: scrollBehavior });
    if (rec.empty) {
      empty.hidden = false; list.hidden = true; return;
    }
    empty.hidden = true; list.hidden = false;
    list.innerHTML = rec.items.map(function (it) {
      const sol = ACR_SOL[it.slug];
      const href = sol ? sol.href : 'solucoes.html';
      const title = sol ? sol.title : 'Ver o processo';
      return '<div class="callout lift" style="margin-bottom:1rem">' +
        '<span class="tag">Direção sugerida</span>' +
        '<h3 style="margin-top:.5rem">' + title + '</h3>' +
        '<p class="small muted">' + it.why + '</p>' +
        '<div class="mt-2"><a class="tlink" href="' + href + '">Ver esta estrutura</a></div>' +
        '</div>';
    }).join('');
  });

  const reset = document.querySelector('[data-diag-reset]');
  if (reset) reset.addEventListener('click', function () {
    form.reset(); result.hidden = true; sync();
    form.scrollIntoView({ block: 'start', behavior: scrollBehavior });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', acrDiagInit);
} else {
  acrDiagInit();
}
"""


def _radio_row(name, legend, options, hint=None):
    """options: list of (value, label)"""
    items = "".join(
        f'<label class="choice"><input type="radio" name="{name}" value="{v}"><span>{l}</span></label>'
        for v, l in options
    )
    hint_html = f'<p class="hint" style="margin:.5rem 0 0">{hint}</p>' if hint else ""
    return f"""<div class="field field--full">
      <span class="fieldset-legend">{legend}</span>
      <div class="choicegrid" role="radiogroup" aria-label="{legend}">{items}</div>
      {hint_html}
    </div>"""


def pages():
    path = "diagnostico.html"
    trail = [("Início", "index.html"), ("Diagnóstico rápido", None)]

    sol_json = {
        s["slug"]: {"title": s["title"], "href": B.rel(path, "solucoes/" + s["slug"] + ".html")}
        for s in SOLUTIONS
    }
    sol_json["solucoes"] = {"title": "Ver todas as soluções", "href": B.rel(path, "solucoes.html")}
    sol_json["como-funciona"] = {"title": "Entender o processo", "href": B.rel(path, "como-funciona.html")}
    import json
    script = QUESTIONS_JS.replace("__SOL_JSON__", json.dumps(sol_json, ensure_ascii=False))

    body = B.pagehead(
        path, trail, "Diagnóstico rápido",
        "4 perguntas. Uma direção, não uma proposta.",
        "Esta ferramenta não substitui a análise: ela aponta qual das 8 estruturas costuma "
        "caber no seu cenário, para você chegar à conversa já sabendo por onde começar. "
        "Nenhuma resposta sai do seu navegador, nada é enviado ou registrado.",
        meta=[("O que isto não é", "Simulação de valor, taxa ou prazo"),
              ("O que isto é", "Direcionamento entre as 8 estruturas"),
              ("Dados enviados", "Nenhum. Processamento local")],
        variant=1, image_slot="diagnostico")

    body += f"""<section class="band">
  <div class="shell shell--tight">
    <form data-diag-form novalidate>
      <div class="fgrid">
        {_radio_row("perfil", "Perfil", [("pf", "Pessoa física"), ("pj", "Pessoa jurídica")])}
        {_radio_row("necessidade", "Qual é a necessidade principal?", [
            ("liquidez", "Liquidez rápida"),
            ("reduzir_custo", "Reduzir o custo de uma dívida atual"),
            ("crescer", "Crescer o negócio ou o giro"),
            ("imovel", "Comprar ou construir um imóvel"),
            ("nao_sei", "Ainda não sei"),
        ])}
        {_radio_row("garantia", "Qual ativo está disponível como possível garantia?", [
            ("imovel", "Imóvel"), ("veiculo", "Veículo"),
            ("recebiveis", "Recebíveis ou faturamento"), ("nenhum", "Nenhum no momento"),
        ])}
        <div data-field-porte hidden>
          {_radio_row("porte", "Porte aproximado da operação", [
              ("pequeno", "Abaixo de R$ 500 mil"), ("grande", "A partir de R$ 500 mil"),
          ], "Usado apenas para indicar se o caso tende a pedir uma estrutura sob medida.")}
        </div>
        <div data-field-obra hidden>
          {_radio_row("obra", "Envolve construir, e não só comprar pronto?", [
              ("sim", "Sim, envolve obra"), ("nao", "Não, é aquisição pronta"),
          ])}
        </div>
      </div>
      <div class="formfoot" style="border-top:0;padding-top:0;margin-top:1.5rem">
        <button type="submit" class="btn">Ver direção sugerida</button>
        <p class="xs muted" style="margin:0;max-width:32ch">Resultado qualitativo. Não é uma pré-aprovação nem uma simulação de valores.</p>
      </div>
    </form>

    <div data-diag-result hidden role="status" aria-live="polite" class="mt-4" style="border-top:1px solid var(--rule);padding-top:2rem">
      {B.sechead("Resultado", "A partir do que você respondeu")}
      <div data-diag-list class="mt-3"></div>
      <p data-diag-empty hidden class="muted">Sem uma resposta clara na necessidade principal, o caminho mais direto é uma conversa de diagnóstico.</p>
      <div class="callout callout--fill mt-3">
        <p class="small muted" style="margin:0">Isto é um direcionamento entre estruturas, calculado no seu navegador a partir de regras gerais. Não considera seu perfil de crédito, não consulta nenhum bureau e não substitui a análise de um especialista. Toda condição real depende de análise da instituição financeira responsável.</p>
        <div class="btn-row mt-3">
          {B.btn("Solicitar uma análise completa", "contato.html", path)}
          <button type="button" class="btn btn--line" data-diag-reset>Refazer</button>
        </div>
      </div>
    </div>
  </div>
</section>"""

    body += B.cta_band(
        path, "Prefere conversar direto?",
        "O diagnóstico rápido é opcional. Se o seu caso já está claro, vá direto para a análise.",
        secondary=("Ver as 8 estruturas", "solucoes.html"), tone="ink")

    body += f'<script>{script}</script>'

    return [{
        "path": path, "nav_key": None, "over": True,
        "title": "Diagnóstico rápido de crédito | Acrópole Capital",
        "desc": ("Ferramenta interativa que direciona entre as 8 estruturas de crédito da Acrópole "
                 "Capital a partir do seu cenário. Sem envio de dados, sem simulação de valores."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail)],
    }]
