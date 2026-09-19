# -*- coding: utf-8 -*-
"""Governança e conformidade: postura de compliance da assessoria."""
import build as B


def pages():
    path = "governanca.html"
    trail = [("Início", "index.html"), ("Governança", None)]

    body = B.pagehead(
        path, trail, "Governança",
        "Estrutura, critério e um canal aberto quando algo foge do combinado.",
        "Operações de crédito envolvem dados sensíveis, patrimônio e, com frequência, mais de "
        "uma parte interessada. Esta página descreve os critérios que seguimos para conduzir "
        "isso com responsabilidade.",
        meta=[("Natureza", "Assessoria, não instituição financeira"),
              ("Base legal de dados", "LGPD, Lei nº 13.709/2018"),
              ("Canal de conduta", "Descrito na seção 5")],
        variant=2, image_slot="governanca")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("1", "Natureza da atividade e limites de atuação")}
    <div class="stack-2">
      <p class="lead">A Acrópole Capital atua na assessoria e na estruturação de operações de crédito. Não é instituição financeira, não capta recursos do público, não concede crédito diretamente e não custodia recursos de clientes.</p>
        <p class="muted">A aprovação, as condições e a decisão final de qualquer operação são de competência exclusiva da instituição financeira responsável, sujeitas às políticas e aos critérios dela. Nosso papel termina em estruturar a operação e apresentar as alternativas com informação completa, incluindo o que pesa contra cada uma.</p>
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--top-rule">
  <div class="shell">
    {B.sechead("2", "Identificação de cliente e origem dos recursos")}
    <div class="stack-2">
      <p class="muted">Antes de estruturar qualquer operação, coletamos documentação suficiente para identificar quem é o titular da operação e, em pessoa jurídica, o quadro societário. Isso vale tanto para pessoa física quanto para empresas.</p>
        {B.pointlist([
            "Não damos andamento a operações quando a origem dos recursos ou do patrimônio oferecido em garantia não pode ser razoavelmente esclarecida.",
            "Não estruturamos operações para terceiros não identificados, nem aceitamos instruções para ocultar o titular real de uma operação.",
            "Documentação, comunicações e simulações trocadas ao longo do processo são mantidas pelo prazo necessário ao atendimento e às obrigações legais aplicáveis, conforme descrito na Política de Privacidade.",
        ])}
    </div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("3", "Conflito de interesses e remuneração")}
    <div class="stack-2">
      {B.pointlist([
            "A forma de remuneração da Acrópole Capital é apresentada por escrito antes de qualquer contratação, junto com a proposta da operação.",
            "A comparação entre instituições parceiras é feita por critério técnico, principalmente custo efetivo total e adequação da estrutura, não por qual delas remunera melhor a assessoria.",
            "Quando existe qualquer relação comercial entre a Acrópole Capital e uma instituição que possa influenciar a recomendação, isso é informado ao cliente antes da decisão.",
        ])}
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("4", "Proteção de dados")}
    <div class="stack-2">
      <p class="muted">O tratamento de dados pessoais segue a Lei Geral de Proteção de Dados. Os detalhes sobre finalidade, base legal, retenção, compartilhamento com instituições parceiras e direitos do titular estão descritos na íntegra na Política de Privacidade.</p>
        <div class="mt-1">{B.tlink("Ler a Política de Privacidade", "politica-de-privacidade.html", path)}</div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("5", "Canal de conduta")}
    <div class="stack-2">
      <p class="muted">Se em algum momento da estruturação você identificar algo que pareça contrariar os critérios descritos nesta página, seja por parte da nossa equipe, seja por parte de uma instituição parceira indicada por nós, há um canal direto para relatar isso.</p>
        <div class="callout callout--fill mt-2">
          <span class="tag">Canal de conduta</span>
          <p class="mt-2" style="margin-bottom:0">{B.mail_link()}</p>
          <p class="small muted mt-1" style="margin-bottom:0">Relatos são analisados pela liderança da empresa, fora do fluxo comercial da operação em questão.</p>
        </div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("6", "Revisão")}
    <div class="stack-2">
      <p class="muted">Estes critérios são revisados periodicamente. A versão vigente é sempre a publicada nesta página.</p>
        <p class="notice mt-2">Esta página descreve critérios internos de conduta da Acrópole Capital. Ela não constitui certificação, selo ou atestado de terceiros, e não deve ser lida como tal.</p>
    </div>
  </div>
</section>"""

    body += B.cta_band(
        path, "Alguma dúvida sobre como conduzimos uma operação?",
        "Pergunte antes de começar. É mais barato esclarecer um critério agora do que no meio de uma estruturação.",
        primary=("Falar com um especialista", "contato.html"),
        secondary=("Ver como funciona o processo", "como-funciona.html"), tone="petrol")

    return [{
        "path": path, "nav_key": None, "over": True,
        "title": "Governança e conformidade | Acrópole Capital",
        "desc": ("Critérios de identificação de cliente, conflito de interesses, proteção de dados "
                 "e canal de conduta na assessoria e estruturação de crédito."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail)],
    }]
