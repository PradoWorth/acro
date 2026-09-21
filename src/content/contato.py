# -*- coding: utf-8 -*-
"""Página de contato, com formulário progressivo."""

from content.site import (SITE, SOLUTIONS, PENDENTE, CARGOS, PORTES, FATURAMENTOS,
                           RESTRICAO, VALORES_BUSCADOS, URGENCIAS, ORIGENS)
import build as B


def _req_mark(required):
    # Marca visível de campo obrigatório. O formulário usa novalidate +
    # validação própria em JS (ver site.js), então o asterisco nativo que o
    # navegador mostraria sozinho em campos "required" nunca aparece — sem
    # isso, quem enxerga não tinha nenhuma pista visual de quais campos são
    # obrigatórios antes de tentar enviar e cair no erro. aria-hidden porque
    # o próprio atributo "required" no elemento já é o que o leitor de tela
    # anuncia; duplicar como texto lido em voz alta ficaria redundante.
    return ' <span class="req" aria-hidden="true">*</span>' if required else ""


def _select(name, label, options, hint=None, required=True, full=False):
    opts = "".join(f'<option value="{o}">{o}</option>' for o in options)
    hint_html = f'<span class="hint" id="{name}-hint">{hint}</span>' if hint else ""
    req = " required" if required else ""
    # aria-describedby aponta pro hint (quando existe) e sempre pro erro: o
    # erro fica display:none por padrão (ver site.css) e só aparece quando
    # data-invalid="true" muda esse display — como o id já está associado
    # de forma estática, o leitor de tela lê o texto assim que ele fica
    # visível, sem precisar de nenhum JS a mais pra ligar os dois na hora.
    described = " ".join(x for x in [f"{name}-hint" if hint else None, f"{name}-err"] if x)
    aria = f' aria-describedby="{described}"'
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{name}">{label}{_req_mark(required)}</label>
      <select id="{name}" name="{name}"{req}{aria}>
        <option value="">Selecione</option>{opts}
      </select>
      {hint_html}
      <span class="field__err" id="{name}-err">Selecione uma opção para continuar.</span>
    </div>"""


def _input(name, label, kind="text", placeholder="", hint=None, mask=None,
           validate=None, required=True, err="Preencha este campo.", full=False):
    described = " ".join(x for x in [f"{name}-hint" if hint else None, f"{name}-err"] if x)
    attrs = f'type="{kind}" id="{name}" name="{name}" aria-describedby="{described}"'
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
    hint_html = f'<span class="hint" id="{name}-hint">{hint}</span>' if hint else ""
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{name}">{label}{_req_mark(required)}</label>
      <input {attrs}>
      {hint_html}
      <span class="field__err" id="{name}-err">{err}</span>
    </div>"""


def _textarea(name, label, placeholder="", hint=None, required=False, full=True):
    """Campo de texto livre, opcional por padrão — o único do formulário
    sem valor pré-definido (os demais são select/radio/telefone/e-mail,
    todos com formato fechado). Pedido do cliente: dar à pessoa um espaço
    para descrever a situação com as próprias palavras, sem obrigar
    ninguém que prefira só preencher os campos objetivos e enviar."""
    described = f"{name}-hint" if hint else None
    aria = f' aria-describedby="{described}"' if described else ""
    hint_html = f'<span class="hint" id="{name}-hint">{hint}</span>' if hint else ""
    req = " required" if required else ""
    cls = "field field--full" if full else "field"
    return f"""<div class="{cls}">
      <label for="{name}">{label}</label>
      <textarea id="{name}" name="{name}" rows="4"{req}{aria}{f' placeholder="{placeholder}"' if placeholder else ""}></textarea>
      {hint_html}
    </div>"""


def _choice(name, legend, options, hint=None):
    items = "".join(
        f'<label class="choice"><input type="radio" name="{name}" value="{o}"><span>{o}</span></label>'
        for o in options
    )
    hint_html = f'<p class="hint" id="{name}-hint" style="margin:.5rem 0 0">{hint}</p>' if hint else ""
    described = " ".join(x for x in [f"{name}-hint" if hint else None, f"{name}-err"] if x)
    return f"""<div class="field field--full" data-required-group>
      <span class="fieldset-legend">{legend}{_req_mark(True)}</span>
      <div class="choicegrid" role="radiogroup" aria-label="{legend}" aria-describedby="{described}">{items}</div>
      {hint_html}
      <span class="field__err" id="{name}-err">Escolha uma opção.</span>
    </div>"""


def form(path):
    estruturas = [s["title"] for s in SOLUTIONS] + ["Ainda não sei, preciso de diagnóstico"]
    return f"""<form class="form" data-endpoint-form data-whatsapp-redirect="{SITE['whatsapp_lead_href']}" novalidate>
  <p class="xs muted req-legend" style="margin:0 0 1rem"><span class="req" aria-hidden="true">*</span> campo obrigatório</p>
  <div class="fgrid fgrid--2">
    {_input("nome", "Nome completo", "text", "Como consta no documento", err="Informe seu nome completo.")}
    {_input("telefone", "Telefone ou WhatsApp", "tel", "(00) 00000-0000", mask="phone",
            validate="phone", err="Informe um número com DDD.")}
    {_input("email", "E-mail", "email", "nome@empresa.com.br", validate="email",
            err="Informe um e-mail válido.")}
    {_input("empresa", "Nome da empresa", "text", "Razão social ou nome fantasia", err="Informe o nome da empresa.")}
    {_select("cargo", "Cargo", CARGOS)}
    {_select("porte", "Porte da empresa", PORTES)}
    {_select("faturamento", "Qual o faturamento anual da sua empresa?", FATURAMENTOS, full=True)}
    {_select("estrutura", "Qual estrutura você imagina que precisa?", estruturas, full=True)}
    {_select("valor", "Qual valor aproximado você busca captar?", VALORES_BUSCADOS)}
    {_select("urgencia", "Em quanto tempo precisa resolver isso?", URGENCIAS)}
    {_choice("restricao", "A empresa ou os sócios têm alguma restrição no CPF/CNPJ hoje (protesto, negativação, ação judicial)?", RESTRICAO)}
    {_select("origem", "Como você conheceu a Acrópole Capital?", ORIGENS, required=False, full=True)}
    {_textarea("detalhes", "Descreva a situação (opcional)",
               placeholder="Conte o que achar relevante: o contexto da operação, um prazo, uma restrição específica.",
               hint="Nenhum campo acima obriga isso; use este espaço só se achar que ajuda.")}
  </div>

  <div class="hp" aria-hidden="true">
    <label for="company_website">Não preencha este campo</label>
    <input type="text" id="company_website" name="company_website" tabindex="-1" autocomplete="off">
  </div>

  <label class="consent mt-2">
    <input type="checkbox" name="consentimento" required>
    <span>Autorizo o contato da Acrópole Capital para tratar desta solicitação e o tratamento dos meus dados conforme a <a href="{B.rel(path, 'politica-de-privacidade.html')}">Política de Privacidade</a>. O envio não representa solicitação formal de crédito nem aprovação.</span>
    <span class="consent__err">Marque a caixa acima pra continuar.</span>
  </label>

  <div class="formfoot formfoot--wide">
    <div class="btn-row">
      <button type="submit" class="btn" data-step-submit>
        <span class="spinner" aria-hidden="true"></span>Enviar solicitação
      </button>
    </div>
    <p class="xs muted" style="margin:0;max-width:34ch">Retornamos em até 2 minutos pelo canal que você indicar.</p>
  </div>

  {B.form_status("ok", f"<strong>Solicitação enviada.</strong> Recebemos os seus dados e você será direcionado ao WhatsApp em instantes para adiantar a conversa com um especialista. Se a página não abrir sozinha, <a href='{SITE['whatsapp_lead_href']}' target='_blank' rel='noopener'>toque aqui</a>.")}
  {B.form_status("err", f"<strong>O envio não foi concluído.</strong> Tente novamente em alguns instantes. Se o problema persistir, escreva para {SITE['email'] if not B.is_placeholder(SITE['email']) else 'o e-mail no rodapé'} com as mesmas informações.")}
</form>"""


def pages():
    path = "contato.html"
    trail = [("Início", "index.html"), ("Contato", None)]

    body = B.pagehead(
        path, trail, "Contato",
        "Descreva a operação. Devolvemos uma leitura técnica.",
        "O formulário pede apenas o necessário para começar. Nenhum campo aqui representa "
        "solicitação formal de crédito, e nenhuma consulta a bureau é feita sem autorização expressa.",
        meta=[("Retorno", "Até 2 minutos"),
              ("Consulta a bureau", "Somente com autorização"),
              ("Compromisso", "Nenhum até a formalização")],
        variant=2, image_slot="contato")

    body += f"""<section class="band">
  <div class="shell">
    <div class="cols cols--7-5 cols--split">
      <div>{form(path)}</div>
      <div><div class="stack-4 stickycol">
        <div>
          <h2 class="h-block">O que acontece depois do envio</h2>
          {B.sequence([
            ("Leitura do contexto", "Um especialista lê o que você escreveu e identifica se a demanda é de capital novo, de reestruturação de passivo ou de ambos."),
            ("Conversa inicial", "Contato pelo canal indicado para completar o que faltar. Sem documentação e sem consulta a bureau nesta etapa."),
            ("Retorno com alternativas", "Apresentamos as estruturas viáveis, com custo efetivo, prazo e o que pesa contra cada uma delas."),
          ])}
        </div>
        <div class="callout">
          <span class="tag">Antes de preencher</span>
          <p class="small muted mt-2" style="margin-bottom:0">Se ainda não sabe qual estrutura procurar, o diagnóstico rápido leva menos de um minuto e não envia nenhum dado.</p>
          <div class="mt-2">{B.tlink("Fazer o diagnóstico rápido", "diagnostico.html", path)}</div>
        </div>
        <div class="callout callout--fill">
          <h3 class="h-sub">Outros canais</h3>
          <dl class="deflist" style="border-top:0">
            <div class="deflist__row" style="padding-top:.5rem"><dt>WhatsApp</dt><dd>{B.clink(SITE['whatsapp_label'], SITE['whatsapp_href'], pendente=PENDENTE['whatsapp_label'], attrs=' data-lead-modal')}</dd></div>
            {f'<div class="deflist__row"><dt>Telefone</dt><dd>{B.clink(SITE["phone_label"], SITE["phone_href"], pendente=PENDENTE["phone_label"])}</dd></div>' if not B.is_placeholder(SITE['phone_label']) else ''}
            <div class="deflist__row"><dt>E-mail</dt><dd>{B.mail_link()}</dd></div>
            {B.field_row('Atendimento', SITE['hours'], PENDENTE['hours']) if not B.is_placeholder(SITE['hours']) else ''}
          </dl>
        </div>
      </div></div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--snug">
  <div class="shell">
    {B.sechead("O que analisamos com você", "3 pontos que pesam mais do que a taxa anunciada.",
               "Você não precisa chegar com essas respostas prontas. É justamente isso que resolvemos juntos na conversa.")}
    <div class="rows rows--3">
      <div class="lift"><span class="lift__n figures">01</span><h3>O prazo cabe na vida útil do ativo?</h3><p class="small muted">Em garantia móvel, um prazo maior do que a curva de depreciação deixa o saldo devedor acima do próprio bem. A gente verifica isso com você.</p></div>
      <div class="lift"><span class="lift__n figures">02</span><h3>O custo efetivo, não só a taxa</h3><p class="small muted">IOF, tarifas, avaliação, registro e seguros mudam a comparação entre instituições. A taxa de vitrine raramente conta a história inteira, e essa conta nós fazemos com você.</p></div>
      <div class="lift"><span class="lift__n figures">03</span><h3>A parcela cabe no fluxo realista?</h3><p class="small muted">Alongar reduz a parcela e estende o compromisso. Simulamos os 2 cenários junto com você antes de decidir.</p></div>
    </div>
  </div>
</section>"""

    return [{
        "path": path, "nav_key": "contato.html", "over": True,
        "title": "Contato e solicitação de análise | Acrópole Capital",
        "desc": ("Descreva a operação e receba uma leitura técnica das estruturas viáveis. "
                 "Sem compromisso e sem consulta a bureau de crédito sem autorização expressa."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), {
            "@context": "https://schema.org", "@type": "ContactPage",
            "name": "Contato | Acrópole Capital", "url": SITE["domain"] + "/contato",
        }],
    }]
