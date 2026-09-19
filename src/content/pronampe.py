# -*- coding: utf-8 -*-
"""
Landing page da campanha Pronampe 2026.

Origem: o cliente entregou a campanha como um projeto React (Vite/Tailwind),
com layout e copy próprios. Esta página é a campanha dele publicada NO
MODELO DO SITE — decisão dele, depois de ver as duas versões lado a lado
(ver README, item 120):

  - o texto é o da campanha, palavra por palavra (título, dores, exemplos
    por segmento, condições, requisitos, etapas e perguntas frequentes);
  - a apresentação é a do site: mesmo cabeçalho, gaveta, rodapé, tipografia,
    cores, componentes e formulário de captação de verdade (com máscara,
    validação, envio ao endpoint e redirecionamento para o WhatsApp).

Só o arranjo de campanha (topo escuro com o formulário ao lado, cartões de
dor, faixa de condições) é local a esta página, isolado por escopo CSS em
`.pronampe` — o resto vem do site.css como em qualquer outra página.

Item 121 (ver README): a versão do item 120 ainda trazia uma paleta própria
da campanha (azul-marinho, laranja, verde isolados em `--p-navy`/`--p-blue`/
`--p-orange`/`--p-green`) por cima do modelo do site — nenhuma dessas cores
existe no sistema visual (`static/assets/css/site.css`), que usa só verde
institucional (`--iris`/`--accent-ink`), azul de destaque (`--cobalt`) e
preto-azulado (`--obsidian`) para fundo escuro. O cliente pediu para
descartar essa paleta própria e usar só as cores e os componentes reais do
site (o mesmo `--cta-grad` dos botões, o mesmo `--obsidian` das faixas
escuras, o mesmo par `--accent-wash`/`--accent-ink` dos selos de ícone que
aparece em toda página de produto). O arranjo de campanha (topo com foto e
formulário ao lado, cartões de dor, faixa de condições escura) continua —
só a cor local em cima dele foi removida.

Duas informações que ESTA versão acrescenta ao texto do arquivo original,
ambas sinalizadas ao cliente (ver README, item 120): o teto de faturamento
anual do Pronampe (R$ 4,8 milhões), sem o qual uma empresa maior pode se
candidatar achando que se enquadra, e a nota de que os valores por segmento
são exemplos de aplicação, não valores liberados a um cliente específico.
"""
from content.site import SITE, PENDENTE
import build as B


# ---------------------------------------------------------------- formulário
def _field(id_, name, label, kind="text", placeholder="", mask=None, validate=None,
           required=True, err="Preencha este campo.", full=False):
    attrs = f'type="{kind}" id="{id_}" name="{name}" aria-describedby="{id_}-err"'
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
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{id_}">{label}</label>
      <input {attrs}>
      <span class="field__err" id="{id_}-err">{err}</span>
    </div>"""


def _select(id_, name, label, options, full=False):
    opts = "".join(f'<option value="{v}">{l}</option>' for v, l in options)
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{id_}">{label}</label>
      <select id="{id_}" name="{name}" required aria-describedby="{id_}-err">
        <option value="">Selecione o faturamento...</option>{opts}
      </select>
      <span class="field__err" id="{id_}-err">Selecione uma opção para continuar.</span>
    </div>"""


REVENUE_OPTIONS = [
    ("abaixo-60k", "Abaixo de R$ 60.000/mês"),
    ("60k-200k", "De R$ 60.000 a R$ 200.000/mês"),
    ("200k-400k", "De R$ 200.000 a R$ 400.000/mês"),
    ("acima-400k", "Acima de R$ 400.000/mês"),
]


def lead_form(path):
    return f"""<h2 class="pronampe-form__title">Simule seu limite</h2>
    <form class="form" data-endpoint-form data-whatsapp-redirect="{SITE['whatsapp_lead_href']}" novalidate>
      <input type="hidden" name="lead_campaign" value="pronampe-2026">
      <div class="fgrid fgrid--2" style="gap:1rem">
        {_field("pn-nome", "nome", "Nome completo", placeholder="Ex: João Silva", err="Informe seu nome completo.")}
        {_field("pn-telefone", "telefone", "Telefone / WhatsApp", kind="tel", placeholder="(00) 00000-0000", mask="phone", validate="phone", err="Informe um número com DDD.")}
        {_field("pn-cnpj", "cnpj", "CNPJ da empresa", placeholder="00.000.000/0000-00", mask="doc", validate="doc", err="Informe um CNPJ válido.", full=True)}
        {_select("pn-faturamento", "faturamento_mensal", "Faturamento médio mensal", REVENUE_OPTIONS, full=True)}
      </div>

      <div class="pronampe-notice">
        {_ICON_CLOCK}
        <p>Um consultor entra em contato via WhatsApp <strong>em até 2 minutos</strong>.</p>
      </div>

      <div class="hp" aria-hidden="true">
        <label for="pn-company">Não preencha este campo</label>
        <input type="text" id="pn-company" name="company_website" tabindex="-1" autocomplete="off">
      </div>

      <label class="consent mt-2">
        <input type="checkbox" name="consentimento" required>
        <span>Confirmo que a empresa e os sócios <strong>não possuem restrições</strong> ativas no SPC/Serasa, e autorizo o contato da Acrópole Capital para tratar desta solicitação conforme a <a href="{B.rel(path, 'politica-de-privacidade.html')}">Política de Privacidade</a>. O envio não representa solicitação formal de crédito nem aprovação.</span>
      </label>

      <div class="formfoot" style="margin-top:1.25rem">
        <div class="btn-row" style="width:100%">
          <button type="submit" class="btn btn--block" data-step-submit>
            <span class="spinner" aria-hidden="true"></span>Verificar meu limite agora
          </button>
        </div>
      </div>

      {B.form_status("ok", f"<strong>Análise solicitada.</strong> Fique de olho no seu WhatsApp: um especialista entra em contato em até 2 minutos. Se a página não abrir sozinha, <a href='{SITE['whatsapp_lead_href']}' target='_blank' rel='noopener'>toque aqui</a>.")}
      {B.form_status("err", f"<strong>O envio não foi concluído.</strong> Tente novamente em alguns instantes ou fale direto pelo WhatsApp no rodapé desta página.")}

      <div class="pronampe-safe">{_ICON_SHIELD}<span>Ambiente seguro. Dados protegidos pela LGPD.</span></div>
    </form>"""


_ICON_CLOCK = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">'
               '<circle cx="8" cy="8" r="6.4"/><path d="M8 4.6V8l2.6 1.6"/></svg>')
_ICON_SHIELD = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">'
                '<path d="M8 1.6 2.8 3.4v4.2c0 4 2.3 6.3 5.2 7.6 2.9-1.3 5.2-3.6 5.2-7.6V3.4L8 1.6Z"/>'
                '<path d="M5.6 8.2l1.7 1.7 3.1-3.4"/></svg>')
# Item 140: mesmo tratamento do item 139 (fidelidade ao lucide-react),
# estendido ao resto dos ícones da página — o check do hero e os 4+4+3
# das faixas "custo invisível" / "condições" / "requisitos". Mesma
# convenção: viewBox 24x24, stroke-width 2, round/round, do próprio pacote.
_ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>')

ICON_ALERT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>')
ICON_TREND_DOWN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                    '<path d="M16 17h6v-6"/><path d="m22 17-8.5-8.5-5 5L2 7"/></svg>')
ICON_WALLET = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/>'
               '<path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>')
ICON_SHIELD_ALERT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                      '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
                      '<path d="M12 8v4"/><path d="M12 16h.01"/></svg>')

# Item 139: ícones copiados fielmente do pacote lucide-react (Store,
# Stethoscope, Factory — v0.546.0), que é o que o material original da
# campanha (lp-pronampe-codigo-fonte.zip) usa nos 3 cartões de segmento.
# Mantidos no viewBox 24x24 e traço 2/round do próprio lucide (não no
# viewBox 28/traço 1.5 usados nos ícones redesenhados do site) para serem
# uma cópia exata, não uma reinterpretação.
ICON_STORE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M15 21v-5a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v5"/>'
              '<path d="M17.774 10.31a1.12 1.12 0 0 0-1.549 0 2.5 2.5 0 0 1-3.451 0 1.12 1.12 0 0 0-1.548 0 '
              '2.5 2.5 0 0 1-3.452 0 1.12 1.12 0 0 0-1.549 0 2.5 2.5 0 0 1-3.77-3.248l2.889-4.184A2 2 0 0 1 7 2h10a2 2 0 0 1 1.653.873l2.895 4.192a2.5 2.5 0 0 1-3.774 3.244"/>'
              '<path d="M4 10.95V19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8.05"/></svg>')
ICON_STETH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M11 2v2"/><path d="M5 2v2"/>'
              '<path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/>'
              '<path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/></svg>')
ICON_FACTORY = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<path d="M12 16h.01"/><path d="M16 16h.01"/>'
                '<path d="M3 19a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.5a.5.5 0 0 0-.769-.422l-4.462 2.844A.5.5 0 0 1 15 10.5v-2a.5.5 0 0 0-.769-.422L9.77 10.922A.5.5 0 0 1 9 10.5V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2z"/>'
                '<path d="M8 16h.01"/></svg>')

ICON_BANKNOTE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                  'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                  '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/></svg>')
ICON_CALENDAR = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                  'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                  '<path d="M16 14v2.2l1.6 1"/><path d="M16 2v4"/><path d="M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3.5"/>'
                  '<path d="M3 10h5"/><path d="M8 2v4"/><circle cx="16" cy="16" r="6"/></svg>')
ICON_TRENDUP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<path d="M16 7h6v6"/><path d="m22 7-8.5 8.5-5-5L2 17"/></svg>')
ICON_LIST = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>'
             '<path d="M14 4h7"/><path d="M14 9h7"/><path d="M14 15h7"/><path d="M14 20h7"/></svg>')

ICON_BUILDING = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                  'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                  '<path d="M10 12h4"/><path d="M10 8h4"/><path d="M14 21v-3a2 2 0 0 0-4 0v3"/>'
                  '<path d="M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2"/>'
                  '<path d="M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16"/></svg>')
ICON_SHIELD_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                      '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
                      '<path d="m9 12 2 2 4-4"/></svg>')
ICON_FILE_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                    '<path d="M4 22h14a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v4"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
                    '<path d="m3 15 2 2 4-4"/></svg>')
ICON_SCALE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>'
              '<path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>'
              '<path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>')


PAINS = [
    (ICON_ALERT, "Oportunidades perdidas",
     "Aquele ponto comercial estratégico, maquinário em liquidação ou aquisição de um concorrente menor passaram direto porque seu capital estava imobilizado na operação."),
    (ICON_TREND_DOWN, "Descontos deixados na mesa",
     "Fornecedores oferecem grandes descontos para compras à vista em volume. Sem liquidez imediata, você paga o preço cheio e esmaga sua margem de lucro mês a mês."),
    (ICON_WALLET, "Risco ao patrimônio pessoal",
     "Para não perder o timing do mercado, você acaba injetando dinheiro da Pessoa Física na Jurídica, misturando as contas e sacrificando o rendimento do seu próprio bolso."),
    (ICON_SHIELD_ALERT, "Descapitalização perigosa",
     "Usar o fluxo de caixa diário para financiar projetos de longo prazo deixa a empresa vulnerável a crises inesperadas. Crescer drenando o caixa é o maior erro de gestão."),
]

# (ícone, segmento, valor de exemplo, aplicação) — os valores são os do
# material da campanha; a nota logo abaixo da grade, na página, deixa claro
# que são exemplos de aplicação, não valores liberados a um cliente.
SEGMENTS = [
    (ICON_STORE, "Comércio & Varejo", "R$ 120.000",
     "Compra de estoque em volume com desconto agressivo à vista para dominar datas sazonais."),
    (ICON_STETH, "Clínicas & Serviços", "R$ 250.000",
     "Abertura de nova filial, reforma do espaço e aquisição de equipamentos de ponta."),
    (ICON_FACTORY, "Indústria & B2B", "R$ 450.000",
     "Ampliação da linha de produção e capital de giro blindado para suportar prazos maiores de clientes."),
]

CONDITIONS = [
    ("Volume estratégico", "Liberação de até R$ 500 mil. O montante ideal para investir em tecnologia, abertura de novas filiais, ampliação de frota ou aquisição de concorrentes.", ICON_BANKNOTE),
    ("Prazo estendido", "Diluição inteligente em até 96 meses. Prazos longos garantem que sua expansão aconteça sem comprometer a saúde e a liquidez do seu fluxo de caixa atual.", ICON_CALENDAR),
    ("Carência para ROI", "Até 24 meses de carência. O tempo exato e necessário para o seu novo investimento maturar, gerar lucro e pagar a própria parcela com folga.", ICON_TRENDUP),
    ("Foco no crescimento", "Condições exclusivas desenhadas para empresas robustas e estruturadas que buscam capital corporativo com taxas reduzidas para multiplicar resultados.", ICON_LIST),
]

REQUISITOS = [
    ("Empresa operacional", "CNPJ ativo com histórico de faturamento real. A linha não se aplica a empresas recém-abertas ou sem operação.", ICON_BUILDING),
    ("Nome limpo (sócios e CNPJ)", "Nenhuma restrição ativa no SPC, Serasa ou Boa Vista, nem para a empresa, nem para os sócios.", ICON_SHIELD_CHECK),
    ("Regularidade fiscal", "Certidões e obrigações em dia junto à Receita Federal e demais órgãos competentes.", ICON_FILE_CHECK),
    # Não estava no material da campanha: sem o teto, uma empresa acima dele
    # se candidata achando que se enquadra (ver docstring).
    ("Dentro do teto do programa", "Faturamento anual de até R$ 4,8 milhões, que é o limite do Pronampe. Acima disso, a empresa está fora do público elegível.", ICON_SCALE),
]

STEPS = [
    ("Análise estratégica", "Preencha a solicitação de simulação. Nossa equipe de especialistas avaliará o perfil financeiro e o faturamento do seu negócio."),
    ("Estruturação de limite", "Mapeamos a melhor condição dentro das regras do Pronampe para maximizar o volume de capital liberado para a sua expansão."),
    ("Capital na conta", "Após a aprovação, o recurso é creditado diretamente na conta PJ da empresa, pronto para ser alocado em seus novos projetos."),
]

FAQS = [
    ("Qual o perfil ideal de empresa para essa linha?",
     "Buscamos empresas estruturadas, com modelo de negócio consolidado e faturamento superior a R$ 60 mil mensais, que precisam de injeção de capital estratégico para projetos de expansão, aquisições ou ganho de market share."),
    ("Empresas negativadas ou sócios com restrição podem solicitar?",
     "Não. Por ser uma linha de crédito com lastro governamental (FGO) e taxas fortemente subsidiadas, as instituições financeiras exigem impreterivelmente que tanto o CNPJ da empresa quanto o CPF dos sócios não possuam restrições ativas no SPC, Serasa ou Boa Vista."),
    ("Como posso utilizar este capital estrategicamente?",
     "O limite é flexível e de livre destinação. É ideal para abertura de novas unidades, compra de equipamentos premium, aumento de frota, campanhas agressivas de marketing, ou reforço de caixa para aproveitar grandes negociações e descontos com fornecedores comprando à vista."),
    ("Qual a real vantagem sobre linhas de crédito corporativas tradicionais?",
     "Por contar com a garantia do FGO (Fundo Garantidor de Operações), as taxas de juros são consideravelmente menores e os prazos de carência (até 24 meses) são bem mais longos que os do crédito corporativo tradicional, permitindo que o seu investimento mature e gere ROI antes do início das amortizações."),
]


def pages():
    path = "pronampe-2026.html"
    trail = [("Início", "index.html"), ("Programas públicos", "programas.html"), ("Pronampe 2026", None)]

    pain_cards = "".join(
        f'''<div class="pronampe-pain" data-reveal>
          <span class="pronampe-pain__icon">{icon}</span>
          <div><h3>{title}</h3><p>{desc}</p></div>
        </div>''' for icon, title, desc in PAINS
    )

    segment_cards = "".join(
        f'''<div class="pronampe-seg" data-reveal>
          <span class="pronampe-seg__icon">{icon}</span>
          <h3>{title}</h3>
          <p class="pronampe-seg__valor">{valor}</p>
          <p>{desc}</p>
        </div>''' for icon, title, valor, desc in SEGMENTS
    )

    cond_cards = B.iconcards([(t, d, i) for t, d, i in CONDITIONS], four=True, variant="line")
    req_cards = B.iconcards([(t, d, i) for t, d, i in REQUISITOS], four=True)

    # Item 139: seção "Como funciona" com desenho próprio (badge numerado em
    # quadrado com borda, ligado por um filete), pedido do cliente a partir
    # do material original da campanha — não usa mais B.sequence(), que é o
    # componente genérico de passos compartilhado pelo resto do site.
    # Item 141: no mobile, o filete entre os passos só existe no VÃO entre um
    # bloco e o próximo (badge+título+texto) — nunca atravessando o texto,
    # que é como o material de referência do cliente mostra. Por isso não dá
    # para ser um único traço full-height atrás de tudo (era o bug
    # reportado): cada passo, exceto o último, ganha o próprio filete curto,
    # como elemento HTML real entre os cartões.
    n_steps = len(STEPS)
    step_cards = "".join(
        f'''<div class="pronampe-step" data-reveal>
          <div class="pronampe-step__badge">{i}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>''' + ('<div class="pronampe-step__connector" aria-hidden="true"></div>' if i < n_steps else '')
        for i, (title, desc) in enumerate(STEPS, 1)
    )

    body = f"""<style>
{_CSS}
</style>
<div class="pronampe">

<section class="pronampe-hero" data-reveal>
  <div class="pronampe-hero__bg">
    {B.raster_img(path, "assets/img/pronampe-hero.jpg", alt="", cls="pronampe-hero__img", eager=True)}
  </div>
  <div class="shell pronampe-hero__inner">
    <div class="cols cols--7-5" style="align-items:start">
      <div class="pronampe-hero__copy">
        <span class="pronampe-badge">Campanha Pronampe ativa</span>
        <h1>Sua empresa já é lucrativa. Agora é a hora de dominar o mercado.</h1>
        <p class="pronampe-hero__lead">Enquanto a concorrência trava por falta de caixa, sua empresa negocia à vista, abre novas unidades e cresce mais rápido, com capital de giro subsidiado pelo Governo Federal.</p>
        <ul class="pronampe-checks">
          <li>{_ICON_CHECK}<span>Até R$ 500 mil disponíveis</span></li>
          <li>{_ICON_CHECK}<span>96 meses para amortização</span></li>
          <li>{_ICON_CHECK}<span>Carência de até 24 meses</span></li>
        </ul>
      </div>
      <div class="pronampe-formcard">{lead_form(path)}</div>
    </div>
  </div>
</section>

<div class="pronampe-trustbar"><div class="shell"><p>Operações viabilizadas com a garantia do FGO (Governo Federal) em parceria com as principais instituições financeiras do país.</p></div></div>

<section class="band" data-reveal>
  <div class="shell">
    <div class="cols cols--5-7">
      <div class="pronampe-photo" data-reveal>
        {B.raster_img(path, "assets/img/pronampe-custo-invisivel.jpg", alt="Profissional consultando dados em um tablet em um corredor de datacenter", cls="pronampe-photo__img")}
        <div class="pronampe-photo__caption">
          <strong>Expansão Inteligente</strong>
          <p>Preserve seu capital de giro pessoal e da empresa enquanto investe com agressividade usando recursos de fomento governamental.</p>
        </div>
      </div>
      <div>
        {B.sechead("O custo invisível", "O custo invisível de crescer com o próprio caixa",
                   "Empresas lucrativas estagnam todos os dias por um único motivo: falta de liquidez estratégica para aproveitar o momento certo.")}
        <div class="pronampe-pains">{pain_cards}</div>
        <div class="pronampe-inlinecta">
          {B.btn("Ver quanto posso acessar", "contato.html", path, attrs=' data-lead-modal')}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band band--stone" data-reveal>
  <div class="shell">
    {B.sechead("Espelho de mercado", "Como empresas do seu porte usam o Pronampe",
               "Crédito subsidiado não serve para cobrir buracos. Ele é a arma secreta que empresas organizadas usam para engolir a concorrência.")}
    <div class="pronampe-segments">{segment_cards}</div>
    <div class="pronampe-inlinecta">
      {B.btn("Simular para o meu segmento", "contato.html", path, attrs=' data-lead-modal')}
    </div>
  </div>
</section>

<section class="band band--ink pronampe-conditions" data-reveal>
  <div class="pronampe-conditions__bg" aria-hidden="true">
    {B.raster_img(path, "assets/img/pronampe-conditions.jpg", alt="", cls="pronampe-conditions__img")}
  </div>
  <div class="shell pronampe-conditions__inner">
    {B.sechead("Condições da linha", "Condições exclusivas para quem pensa grande",
               "Esqueça as taxas abusivas do mercado tradicional. Use o crédito com lastro governamental como sua principal alavanca de crescimento corporativo.")}
    {cond_cards}
  </div>
</section>

<section class="band" data-reveal>
  <div class="shell">
    {B.sechead("Critérios de aprovação", "Requisitos para acessar o lastro FGO",
               "Por se tratar de uma linha com garantia do Governo Federal, a análise exige um perfil de alta governança. A operação é exclusiva para empresas e sócios sem restrições ativas no mercado.")}
    {req_cards}
    <div class="pronampe-inlinecta">
      {B.btn("Verificar meu enquadramento", "contato.html", path, attrs=' data-lead-modal')}
    </div>
  </div>
</section>

<section class="band band--stone" data-reveal>
  <div class="shell">
    {B.sechead("Como funciona", "O caminho ágil para o seu próximo investimento",
               "Um processo estruturado e focado em aprovar o limite máximo que a sua operação corporativa suporta.")}
    <div class="pronampe-steps">{step_cards}</div>
  </div>
</section>

<section class="band" data-reveal>
  <div class="shell" style="max-width:48rem">
    {B.sechead("Dúvidas frequentes", "Dúvidas sobre a alavancagem",
               "Tudo o que você precisa saber sobre a estruturação da linha de crédito.")}
    {B.accordion(FAQS, ident="pronampe-faq")}
  </div>
</section>

{B.cta_band(path, "Quer saber se sua empresa se enquadra no Pronampe?",
            "Preencha a simulação no topo desta página. Um especialista confirma o enquadramento e as próximas etapas.",
            primary=("Simular meu limite agora", "pronampe-2026.html"), secondary=None, tone="ink", primary_opens_modal=False)}

</div>"""

    return [{
        "path": path, "nav_key": None, "over": True,
        "title": "Pronampe 2026: simule o limite da empresa | Acrópole",
        "desc": B.fit_desc("Linha de capital de giro do Governo Federal com garantia do FGO, para empresas com "
                            "faturamento acima de R$ 60 mil por mês. Simule o enquadramento e os limites."),
        "lead_context": {"campaign": "pronampe-2026"},
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(FAQS), {
            "@context": "https://schema.org", "@type": "FinancialProduct",
            "name": "Pronampe 2026, via Acrópole Capital",
            "description": "Estruturação de acesso ao Pronampe, linha de capital de giro do Governo Federal com garantia do FGO.",
            "provider": {"@type": "Organization", "name": "Acrópole Capital"},
            "areaServed": "BR",
        }],
    }]


_CSS = """
/* Item 121: nada aqui redefine --accent/--cta-grad/--obsidian ou qualquer
   outro token — a página usa exatamente as cores do sistema visual do
   site (static/assets/css/site.css). O que sobra local é só o ARRANJO de
   campanha (topo com foto atrás do texto, cartões de dor, faixa de
   condições escura), não uma paleta própria. */
.pronampe-badge { display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:var(--r-button);
  background:rgba(255,255,255,.12); color:var(--iris-on-dark); font-size:var(--t-xs); font-weight:600;
  text-transform:uppercase; letter-spacing:.06em; margin:20px 0 16px; }
.pronampe-hero { position:relative; overflow:hidden; padding-block: var(--sp-6) var(--sp-5); color:#fff; }
.pronampe-hero__bg { position:absolute; inset:0; z-index:0; }
.pronampe-hero__img { width:100%; height:100%; object-fit:cover; filter:saturate(1.05); }
/* Item 130: véu escuro trocado de preto-azulado (--obsidian) para um
   degradê azul → verde-azulado, a pedido do cliente — azul (derivado de
   --cobalt-ink) do lado esquerdo, sobre o texto, indo a --iris (o
   verde-água institucional) do lado direito, sobre a foto/cartão. Mesma
   família de cores do resto do site, não uma paleta nova para a
   campanha. O radial extra cobre o canto inferior direito: a foto
   original tem um objeto desfocado e estourado de luz bem ali, que
   ficava visível mesmo com o degradê de base (pedido no item 122); ele
   agora usa --petrol-deep para casar com o lado verde-azulado do degradê. */
.pronampe-hero__bg::after { content:""; position:absolute; inset:0;
  background:
    radial-gradient(65% 65% at 100% 100%, rgba(11,80,76,.94) 0%, rgba(11,80,76,.65) 40%, rgba(11,80,76,0) 68%),
    linear-gradient(100deg, rgba(6,16,30,.96) 5%, rgba(10,50,68,.87) 45%, rgba(11,80,76,.74) 100%); }
.pronampe-hero__inner { position:relative; z-index:1; }
/* Mesma receita do topo (foto + véu escuro), aplicada à faixa de
   condições: o `.band--ink` já é escuro (--obsidian) sozinho, a foto
   entra como camada decorativa por trás do texto, com o mesmo véu para
   manter o contraste do texto branco e dos cartões por cima. */
.pronampe-conditions { position:relative; overflow:hidden; }
.pronampe-conditions__bg { position:absolute; inset:0; z-index:0; }
.pronampe-conditions__img { width:100%; height:100%; object-fit:cover; }
/* Item 132: mesmo degradê azul → verde-água do topo (item 130), aplicado
   aqui também — antes essa faixa continuava no preto-azulado antigo
   (--obsidian) enquanto só o topo tinha sido trocado. */
.pronampe-conditions__bg::after { content:""; position:absolute; inset:0;
  background: linear-gradient(100deg, rgba(6,16,30,.96) 5%, rgba(10,50,68,.87) 45%, rgba(11,80,76,.74) 100%); }
.pronampe-conditions__inner { position:relative; z-index:1; }
.pronampe-hero__copy h1 { font-family:var(--display); font-size:34px; line-height:1.15; font-weight:700;
  letter-spacing:var(--track-h1); margin:0 0 16px; }
@media (min-width: 48rem) { .pronampe-hero__copy h1 { font-size:40px; } }
@media (min-width: 75rem) { .pronampe-hero__copy h1 { font-size:44px; } }
.pronampe-hero__lead { font-size:var(--t-body); line-height:1.6; color:var(--slate-1); max-width:42rem; margin:0 0 24px; }
.pronampe-checks { list-style:none; margin:0 0 20px; padding:0; display:grid; gap:10px; }
.pronampe-checks li { display:flex; align-items:center; gap:8px; font-weight:600; font-size:var(--t-body); }
.pronampe-checks svg { width:1.5rem; height:1.5rem; color:var(--iris-on-dark); flex-shrink:0; }
.pronampe-formcard { background:#fff; border-radius:var(--r-card); padding:24px; box-shadow:0 24px 60px rgba(0,0,0,.35);
  border-top:4px solid var(--accent); color:var(--ink); }
.pronampe-form__title { font-family:var(--display); font-size:var(--t-h2); font-weight:700; color:var(--ink); text-align:center; margin:0 0 20px; }
/* Item 131: aviso do prazo de contato trocado de verde (--accent-wash/
   --accent-ink) para azul — usa --cobalt-ink (o azul de destaque do
   site) sobre um fundo bem clarinho derivado dele mesmo, não uma cor
   nova para a campanha. */
.pronampe-notice { display:flex; gap:8px; align-items:flex-start; background:rgba(37,92,170,.08); border:1px solid transparent; border-radius:6px;
  padding:12px; margin:16px 0; }
.pronampe-notice svg { width:1.1rem; height:1.1rem; color:var(--cobalt-ink); flex-shrink:0; margin-top:2px; }
.pronampe-notice p { margin:0; font-size:var(--t-sm); color:var(--cobalt-ink); }
.pronampe-safe { display:flex; align-items:center; justify-content:center; gap:6px; margin-top:16px; font-size:var(--t-xs); color:var(--slate-2); }
.pronampe-safe svg { width:.95rem; height:.95rem; color:var(--accent-ink); }
.pronampe-trustbar { background:var(--cloud); --slate-2:var(--iron); border-bottom:1px solid var(--rule); padding-block:16px; }
.pronampe-trustbar p { margin:0; text-align:center; font-size:var(--t-sm); color:var(--slate-2); }
.pronampe-pains { display:grid; gap:16px; margin-top:24px; }
/* Mesma transição de hover dos cartões-padrão do site (.iconcard--line:hover
   em site.css): sobe 2px e ganha a sombra de cartão ao passar o mouse. */
.pronampe-pain { display:flex; gap:16px; padding:16px 20px; background:#fff; border:1px solid var(--rule); border-radius:16px;
  box-shadow:0 1px 2px rgba(0,0,0,.04); transition:box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease); }
/* Especificidade igual à de "html.js-reveal [data-reveal].is-revealed"
   (site.css), que também define transform e, sendo mais específica que um
   ":hover" simples, apagava o hover sem isso — precisa do mesmo peso
   (mais o ".js-reveal" na cadeia) pra vencer no empate por ordem. */
.pronampe-pain:hover, html.js-reveal .pronampe-pain:hover { transform:translateY(-2px); box-shadow:var(--shadow-card); }
/* Mesmo selo de ícone usado em .iconcard__badge/.mediarow__bullet em toda
   página de produto do site: fundo --accent-wash, ícone --accent-ink. */
.pronampe-pain__icon { flex-shrink:0; width:2.6rem; height:2.6rem; border-radius:50%; background:var(--accent-wash); color:var(--accent-ink);
  display:flex; align-items:center; justify-content:center; }
.pronampe-pain__icon svg { width:1.4rem; height:1.4rem; }
.pronampe-pain h3 { margin:0 0 6px; font-size:var(--t-body); font-weight:700; }
.pronampe-pain p { margin:0; font-size:var(--t-sm); color:var(--slate-2); line-height:1.55; }
/* height:100% (não só min-height) para a foto acompanhar a altura real da
   coluna de cartões ao lado, que no desktop é mais alta que os 22rem
   fixos de antes — sem isso sobrava um vão em branco abaixo da foto
   quando a lista de dores ficava mais alta que ela (apontado no item
   123). min-height continua como piso para quando a coluna ao lado for
   mais baixa. */
.pronampe-photo { position:relative; border-radius:var(--r-card); overflow:hidden; min-height:22rem; height:100%; }
.pronampe-photo__img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
/* Item 132: véu do rodapé (para legibilidade da legenda) recolorido do
   mesmo preto-azulado antigo para a mesma família azul → verde-água. */
.pronampe-photo::after { content:""; position:absolute; inset:0; background:linear-gradient(0deg, rgba(6,16,30,.92) 0%, rgba(6,16,30,.12) 55%, rgba(11,80,76,.36) 100%); }
.pronampe-photo__caption { position:absolute; left:0; right:0; bottom:0; padding:24px; color:#fff; z-index:1; }
.pronampe-photo__caption strong { display:block; font-family:var(--display); font-size:var(--t-h3); margin-bottom:6px; }
.pronampe-photo__caption p { margin:0; font-size:var(--t-sm); color:var(--slate-1); line-height:1.55; max-width:26rem; }
.pronampe-segments { display:grid; gap:20px; grid-template-columns:repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); margin-top:24px; }
.pronampe-seg { background:#fff; border:1px solid var(--rule); border-radius:16px; padding:24px;
  transition:box-shadow var(--dur) var(--ease), transform var(--dur) var(--ease); }
.pronampe-seg:hover, html.js-reveal .pronampe-seg:hover { transform:translateY(-2px); box-shadow:var(--shadow-card); }
/* Escalonamento de entrada (mesma ideia de .iconcards/.cols/.rows em
   site.css, seção "21c"): cada cartão de dor e de segmento já nasce com
   [data-reveal] (ver pages()), mas sem isso a fileira toda cruzava o
   viewport e entrava no mesmo frame — aqui só estende a mesma escala de
   atraso por posição aos dois grupos próprios desta página. */
.pronampe-pains > [data-reveal]:nth-child(2),
.pronampe-segments > [data-reveal]:nth-child(2) { transition-delay: .07s; }
.pronampe-pains > [data-reveal]:nth-child(3),
.pronampe-segments > [data-reveal]:nth-child(3) { transition-delay: .14s; }
.pronampe-pains > [data-reveal]:nth-child(4),
.pronampe-segments > [data-reveal]:nth-child(4) { transition-delay: .21s; }
.pronampe-seg__icon { display:flex; align-items:center; justify-content:center; width:3.2rem; height:3.2rem; border-radius:50%;
  background:var(--accent-wash); color:var(--accent-ink); margin-bottom:16px; }
.pronampe-seg__icon svg { width:1.6rem; height:1.6rem; }
.pronampe-seg h3 { margin:0 0 4px; font-size:var(--t-body); font-weight:700; }
/* Valor de exemplo do segmento: já era um token real do site (petrol-deep). */
.pronampe-seg__valor { margin:0 0 12px; font-weight:700; font-size:var(--t-body); color:var(--petrol-deep); }
.pronampe-seg p { margin:0; font-size:var(--t-sm); color:var(--slate-2); line-height:1.55; }
/* No mobile a foto passou a vir primeiro no HTML (ver pages(), item 123),
   então o respiro precisa ficar depois dela, não antes. */
@media (max-width: 899px) { .pronampe-photo { min-height:16rem; height:auto; margin-bottom:32px; } }
/* Item 133: CTAs intermediárias que abrem o popup de captação
   ([data-lead-modal], ver lead_modal() em build.py) — pontos de saída ao
   longo da página, não só no formulário do topo e na faixa final. */
.pronampe-inlinecta { margin-top:32px; text-align:left; }
/* Item 139: "Como funciona" com desenho próprio — badge quadrado com
   borda ligado por um filete, no lugar do .seq genérico (ver pages()).
   Usa os tokens de azul do site (--cobalt / --cobalt-ink), a mesma
   família de cores já presente no sistema visual, não uma cor nova. */
.pronampe-steps { display:grid; grid-template-columns:repeat(3, 1fr); gap:40px 32px; margin-top:24px; position:relative; }
.pronampe-steps::before { content:""; position:absolute; top:32px; left:16.6%; right:16.6%; height:1px;
  background:linear-gradient(90deg, rgba(49,122,226,.12), rgba(49,122,226,.4) 50%, rgba(49,122,226,.12)); z-index:0; }
.pronampe-step { position:relative; z-index:1; display:flex; flex-direction:column; align-items:center; text-align:center; }
.pronampe-step__badge { display:flex; align-items:center; justify-content:center; width:64px; height:64px;
  border-radius:var(--r-input); background:#fff; color:var(--cobalt); border:1px solid rgba(49,122,226,.28);
  box-shadow:var(--shadow-card); font-family:var(--display); font-size:var(--t-h3); font-weight:700;
  margin-bottom:20px; transition:transform var(--dur) var(--ease); }
.pronampe-step:hover .pronampe-step__badge, html.js-reveal .pronampe-step:hover .pronampe-step__badge { transform:translateY(-3px); }
.pronampe-step h3 { margin:0 0 10px; font-size:var(--t-body); font-weight:700; }
.pronampe-step p { margin:0; font-size:var(--t-sm); color:var(--slate-2); line-height:1.55; max-width:22rem; }
/* Item 141: filete do mobile só existe no vão ENTRE um bloco e o próximo,
   nunca atravessando o título/texto do meio — bug relatado pelo cliente
   (o traço full-height de antes passava por trás do parágrafo inteiro).
   Elemento próprio (.pronampe-step__connector), escondido no desktop, que
   usa a barra horizontal do ::before acima. */
.pronampe-step__connector { display:none; }
@media (max-width: 899px) {
  .pronampe-steps { grid-template-columns:1fr; gap:0; }
  .pronampe-steps::before { display:none; }
  .pronampe-step__connector { display:block; width:1px; height:32px; margin:0 auto;
    background:linear-gradient(180deg, rgba(49,122,226,.12), rgba(49,122,226,.4) 50%, rgba(49,122,226,.12)); }
}
"""
