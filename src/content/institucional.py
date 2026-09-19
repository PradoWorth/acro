# -*- coding: utf-8 -*-
"""Páginas institucionais: Sobre, Como funciona, Empresas, Investidores."""

from content.site import SITE, FACTS, SOLUTIONS, SOL_BY_SLUG, CONTATO, CONDITIONS_NOTICE
import build as B


# --------------------------------------------------------------------- Sobre
def sobre():
    path = "sobre.html"
    trail = [("Início", "index.html"), ("Empresa", None)]

    body = B.pagehead(
        path, trail, "A empresa",
        "Uma casa de estruturação, não um balcão de crédito.",
        "A Acrópole Capital existe para uma pergunta específica: qual é a estrutura financeira "
        "correta para esta decisão, neste prazo, com este patrimônio e este fluxo de caixa.",
        meta=[("Constituição", f"CNPJ {SITE['cnpj']}"),
              ("Atuação", "Assessoria e estruturação de operações"),
              ("Rede", "74+ instituições, Brasil e exterior")],
        variant=0, image_slot="sobre")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Origem", "Por que uma casa dedicada a estruturar.")}
    <div data-reveal class="stack-2">
        <p class="lead">O mercado brasileiro de crédito não é um mercado só. Capital de giro é um problema de fluxo e recorrência. Home equity é uma solução de liquidez com garantia forte e risco patrimonial. Construção depende de cronograma, custo e velocidade de vendas. Tratar tudo isso como “empréstimo” é a origem da maior parte das operações mal desenhadas.</p>
        <p class="muted">A Acrópole Capital foi construída em torno da diferença entre essas coisas. Não somos instituição financeira e não concedemos crédito: analisamos o contexto do cliente, desenhamos a operação e a levamos à rede de instituições em condições de executá-la. Isso nos deixa livres para recomendar a estrutura correta, inclusive quando ela é menor, mais lenta ou menos rentável do que a alternativa óbvia.</p>
        <p class="muted">Trabalhamos com empresas que precisam de capital para crescer, empresários com patrimônio imobilizado, incorporadores que precisam casar terreno, obra e vendas, e investidores que preferem preservar caixa a imobilizá-lo. Em operações corporativas estruturadas, atuamos a partir de R$ 500 mil.</p>
        {B.pullquote("Estrutura errada não aparece na assinatura do contrato. Aparece na terceira renovação.")}
    </div>
    <div class="mt-4">{B.statrail(FACTS)}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--top-rule">
  <div class="shell">
    {B.sechead("Como trabalhamos", "4 compromissos que sustentam a recomendação.",
               "São eles que tornam possível dizer a um cliente que a operação que ele pediu não é a operação que ele deveria contratar.")}
    {B.deflist([
        ("Independência de recomendação",
         "Comparamos instituições pela natureza jurídica, pela base legal da garantia e pelo custo efetivo total. A rede ampla existe para permitir comparação, não para direcionar o cliente a um parceiro preferencial."),
        ("Custo real, não taxa de vitrine",
         "Apresentamos o Custo Efetivo Total, com IOF, tarifas, avaliação, registro e seguros. 2 linhas com a mesma taxa nominal podem ter custos finais bastante distintos."),
        ("Garantia como ferramenta, não como atalho",
         "Só recomendamos comprometer um imóvel ou um veículo quando prazo, capacidade de pagamento e finalidade tornam essa decisão defensável. Dívida de consumo transformada em risco sobre a moradia raramente é."),
        ("Discrição como padrão",
         "Operações relevantes exigem sigilo sobre valores, ativos e intenções. Conduzimos cada estruturação com o cuidado que o porte da operação e a posição do cliente no mercado exigem."),
      ], split=True)}
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Rede", "Acesso amplo é o que permite comparar.",
               "Contamos com braço financeiro próprio e conexão ativa com mais de 74 instituições financeiras no Brasil e no exterior, incluindo Inglaterra, Portugal, Suíça, Estados Unidos e Emirados Árabes Unidos. A rede não é um argumento de vitrine: é o que torna possível recusar uma condição ruim e buscar outra.")}
    <div class="cols cols--1-1">
      <div>{B.pointlist([
        "Bancos de varejo e bancos múltiplos, incluindo Banco do Brasil, Caixa Econômica Federal, Santander e Itaú.",
        "Cooperativas de crédito com atuação nacional, como Sicoob e Sicredi.",
        "Sociedades de Crédito Direto (SCD) e Sociedades de Empréstimo entre Pessoas (SEP), com perfis distintos de previsibilidade e apetite.",
      ])}</div>
      <div>{B.pointlist([
        "Bancos e fintechs digitais especializados em crédito com garantia real.",
        "Fundos de investimento imobiliário, em parcerias pontuais para estruturações específicas.",
        "Instituições no exterior, para operações que se beneficiam de funding internacional.",
      ])}</div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--snug">
  <div class="shell">
    <div class="cols cols--1-1">
      <div>
        <h3 class="h-sub">Como conduzimos uma operação</h3>
        <p class="small muted" style="max-width:44ch">Identificação de cliente, conflito de interesses, proteção de dados e um canal direto para relatar qualquer coisa fora do combinado.</p>
        <div class="mt-1">{B.tlink("Ver os critérios de governança", "governanca.html", path)}</div>
      </div>
      <div>
        <h3 class="h-sub">Não sabe qual estrutura procurar?</h3>
        <p class="small muted" style="max-width:44ch">4 perguntas, sem envio de dados, para apontar a direção antes da conversa.</p>
        <div class="mt-1">{B.tlink("Fazer o diagnóstico rápido", "diagnostico.html", path)}</div>
      </div>
    </div>
  </div>
</section>"""

    body += B.cta_band(path, "Conheça a leitura antes de contratar qualquer coisa.",
                       "A primeira conversa serve para entender o contexto e dizer, com honestidade, se existe uma estrutura melhor do que a que você tem hoje.",
                       secondary=("Ver as soluções", "solucoes.html"), tone="ink")

    return {
        "path": path, "nav_key": "sobre.html", "over": True,
        "title": "Sobre a Acrópole Capital | Independência de recomendação",
        "desc": ("Casa de assessoria e estruturação de crédito, com braço financeiro próprio "
                 "e rede de 74+ instituições no Brasil e no exterior."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.org_schema()],
    }


# ------------------------------------------------------------- Como funciona
PROCESS = [
    ("Diagnóstico",
     ["Conversa inicial para entender o objetivo, o prazo e o contexto. Nenhuma consulta a bureau é feita nesta etapa, e nenhuma informação sensível é exigida antes de haver aderência.",
      "É aqui que decidimos, junto com o cliente, se faz sentido seguir. Uma parte relevante das demandas que chegam se resolve melhor sem crédito novo."]),
    ("Análise",
     ["Levantamento do passivo contratado, do fluxo de caixa e dos ativos disponíveis. Em operações empresariais, avaliamos faturamento, margem, prazo médio de recebimento, concentração de clientes e endividamento.",
      "Quando aplicável, conduzimos consulta prévia a bureau de crédito, com autorização expressa, para que a recomendação parta do enquadramento real e não de uma expectativa inflada."]),
    ("Estruturação",
     ["Desenho da operação: valor, prazo, garantias, carência, cronograma de liberação e composição de fontes. Em operações imobiliárias e de obra, o cronograma físico-financeiro entra aqui."]),
    ("Apresentação da operação",
     ["Comparativo entre as alternativas viáveis, com Custo Efetivo Total, parcela, LTV, prazo e as condições acessórias de cada instituição. Também apresentamos os cenários em que a operação deixa de fazer sentido.",
      "A decisão é do cliente. Nosso papel termina em entregar a informação completa, incluindo o que pesa contra."]),
    ("Formalização",
     ["Reunião de documentação, avaliação do bem quando há garantia real, registro em cartório ou lançamento de gravame, e assinatura do contrato junto à instituição escolhida."]),
    ("Liberação",
     ["Crédito liberado pela instituição financeira, à vista ou por etapas conforme o cronograma. Em operações de obra, cada liberação depende da vistoria de avanço físico."]),
]

FAQ_PROCESS = [
    ("Solicitar uma análise significa que o crédito já foi aprovado?",
     "Não. A análise é um diagnóstico da situação e das estruturas disponíveis. A aprovação, as condições e a decisão final são sempre da instituição financeira responsável pela operação, sujeitas aos critérios dela."),
    ("Quais tipos de operação vocês atendem?",
     "Capital de giro, crédito PJ, crédito com garantia de imóvel, crédito com garantia de veículo, financiamento habitacional e produtivo, aquisição de imóveis e terrenos, construção e operações estruturadas que combinam mais de uma dessas frentes. Para operações corporativas estruturadas, atuamos a partir de R$ 500 mil."),
    ("Preciso ter o imóvel ou o veículo quitado?",
     "Depende da linha e da instituição. Em geral, quanto menor o saldo devedor sobre o bem, maior a margem disponível. Desde a Lei nº 14.711/2023 e sua regulamentação, um mesmo imóvel pode, em determinadas condições, ser usado em mais de uma operação quando há margem. Avaliamos isso caso a caso."),
    ("Quais documentos são necessários?",
     "Varia com o perfil e a garantia. Para pessoa física: documento de identificação, comprovante de renda e de residência, e matrícula atualizada do imóvel ou documento do veículo. Para pessoa jurídica: contrato social, faturamento comprovado, balanço ou demonstrativos, relação de dívidas e documentação dos ativos oferecidos em garantia."),
    ("Quanto tempo leva uma operação?",
     "O prazo depende da modalidade, da instituição, da qualidade da documentação e do registro da garantia. Operações com garantia de veículo tendem a ser as mais rápidas; operações com garantia imobiliária dependem de avaliação e de cartório; operações estruturadas com múltiplas fontes levam mais tempo. Informamos a estimativa realista na apresentação da operação, e não prometemos prazos que não dependem de nós."),
    ("Existe garantia de aprovação?",
     "Não, e desconfie de quem afirmar o contrário. A concessão depende de análise de crédito, de garantia e de política interna da instituição financeira, que pode mudar entre a simulação e a formalização."),
    ("Quais são os critérios de análise?",
     "Capacidade de pagamento demonstrada por fluxo de caixa, qualidade e liquidez da garantia oferecida, histórico de crédito, coerência entre a finalidade e o prazo da operação, e enquadramento nas políticas da instituição. Em operações empresariais, pesam também concentração de clientes, margem e composição do endividamento."),
    ("Vocês cobram do cliente ou da instituição?",
     "A forma de remuneração é apresentada por escrito antes de qualquer contratação, junto com a proposta. Nenhum custo é cobrado sem que esteja explicitado previamente."),
]


def como_funciona():
    path = "como-funciona.html"
    trail = [("Início", "index.html"), ("Como funciona", None)]

    body = B.pagehead(
        path, trail, "Processo",
        "6 etapas, e a possibilidade de parar em qualquer uma delas.",
        "O processo existe para reduzir a chance de contratar a operação errada. Ele é criterioso "
        "de propósito: a maior parte dos problemas de crédito nasce de uma decisão tomada rápido demais.",
        meta=[("Etapas", "Diagnóstico a liberação"),
              ("Consulta a bureau", "Somente com autorização expressa"),
              ("Compromisso", "Nenhum até a formalização")],
        variant=1, image_slot="como-funciona")

    body += f"""<section class="band">
  <div class="shell">{B.sequence(PROCESS)}</div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Documentação", "O que costuma ser pedido.",
               "A lista definitiva depende da instituição e da modalidade. Esta é a base que quase toda operação exige, e reuni-la antes acelera bastante o processo.")}
    <div class="cols cols--1-1">
      <div class="lift" data-reveal><h3 style="margin-top:0">Pessoa física</h3>{B.pointlist([
        "Documento de identificação com foto e CPF.",
        "Comprovante de residência recente.",
        "Comprovação de renda: holerites, declaração de imposto de renda ou extratos, conforme o perfil.",
        "Matrícula atualizada do imóvel, com certidão de ônus, quando há garantia imobiliária.",
        "CRLV e comprovação de propriedade, quando há garantia de veículo.",
      ])}</div>
      <div class="lift" data-reveal><h3 style="margin-top:0">Pessoa jurídica</h3>{B.pointlist([
        "Contrato social ou estatuto e última alteração consolidada.",
        "Faturamento dos últimos 12 meses, com comprovação.",
        "Balanço patrimonial e demonstração de resultado do último exercício.",
        "Relação das dívidas contratadas, com credor, saldo, taxa, prazo e garantias.",
        "Documentação dos ativos oferecidos em garantia e do quadro societário.",
      ])}</div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Critérios", "O que pesa numa análise, e o que não pesa.",
               "Não avaliamos intenção. Avaliamos capacidade demonstrável, qualidade de garantia e coerência entre finalidade e prazo.")}
    {B.deflist([
        ("Capacidade de pagamento", "Fluxo de caixa que sustenta a parcela no cenário realista, não no otimista. Em empresa, o indicador relevante é a geração de caixa operacional, não o faturamento bruto."),
        ("Qualidade da garantia", "Valor de mercado, liquidez, localização, estado de conservação, regularidade documental e existência de ônus. Uma garantia difícil de executar não compensa uma taxa maior."),
        ("Coerência de prazo", "Financiar déficit operacional recorrente com dívida longa apenas desloca o problema. Alongar prazo além da vida útil de um ativo depreciável eleva a perda potencial."),
        ("Composição do passivo", "Concentração de vencimentos, custo médio, cláusulas cruzadas e garantias já comprometidas alteram a viabilidade de qualquer operação nova."),
      ], split=True)}
    <p class="notice mt-3">Nenhum destes critérios substitui a política interna da instituição financeira, que é soberana na decisão. Simulações e comparativos apresentados pela Acrópole Capital não constituem oferta nem promessa de aprovação.</p>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Elegibilidade", "Para quem é essa análise, e para quem não é.",
               "Nem toda empresa está no ponto certo para este processo. Dizer isso já na primeira conversa poupa tempo dos dois lados.")}
    <div class="cols cols--1-1">
      <div class="lift" data-reveal><h3 style="margin-top:0">Para quem é</h3>{B.pointlist([
        "Empresas com faturamento mensal a partir de R$ 100 mil, o patamar mínimo para esta análise.",
        "Empresas com faturamento e patrimônio consistentes que já receberam uma negativa sem entender qual fator pesou contra a aprovação.",
        "Empresas que buscam uma operação estruturada, normalmente acima de R$ 500 mil, sempre analisada caso a caso.",
        "Empresas que preferem comparar instituições por natureza jurídica e custo efetivo antes de comprometer uma garantia.",
      ])}</div>
      <div class="lift" data-reveal><h3 style="margin-top:0">Para quem não é</h3>{B.pointlist([
        "Não trabalhamos com MEI.",
        "Não é para empresas com faturamento mensal abaixo de R$ 100 mil. Nesse porte, linhas padronizadas e programas públicos como Pronampe e PEAC FGI costumam ser mais rápidos e mais adequados.",
        "Não é para quem busca promessa de aprovação. Nenhuma análise substitui a decisão soberana da instituição financeira.",
        "Não é uma resposta automática ou instantânea. Uma leitura séria do passivo e da garantia exige documentação real, não só um formulário.",
      ])}</div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("O que você recebe", "A resposta que sua empresa nunca recebeu do banco.",
               "Antes de qualquer submissão, você recebe uma leitura completa de como sua empresa é vista pelas mesas de crédito, não apenas se ela fatura.")}
    <div class="mt-4">{B.iconcards([
        ("Diagnóstico completo", "Leitura do passivo, do patrimônio e do cadastro, apontando o que fortalece e o que reduz a elegibilidade da operação."),
        ("Comparativo estruturado", "As instituições da rede comparadas por natureza jurídica, garantia e custo efetivo, não uma simulação solta de taxa e prazo."),
        ("Apresentação com um especialista", "Os pontos identificados explicados por quem conduziu a análise, com a estrutura recomendada e os cenários alternativos, não apenas um documento para interpretar sozinho."),
    ])}</div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Antes de solicitar uma análise.")}
    {B.accordion(FAQ_PROCESS, "faqp")}
  </div>
</section>"""

    body += B.cta_band(path, "Comece pelo diagnóstico.",
                       "Sem consulta a bureau, sem documentação e sem compromisso na primeira conversa.",
                       secondary=("Ver as soluções", "solucoes.html"), tone="petrol")

    return {
        "path": path, "nav_key": "como-funciona.html", "over": True,
        "title": "Como funciona uma operação | Acrópole Capital",
        "desc": ("O processo completo de uma operação estruturada: diagnóstico, análise, estruturação, "
                 "apresentação, formalização e liberação. Documentação, critérios e prazos."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(FAQ_PROCESS)],
    }


# Perguntas específicas de quem está pesquisando "crédito empresarial" e
# "como conseguir crédito para minha empresa" — não repete o FAQ_PROCESS
# (mais genérico, cross-produto) acima, e complementa com o recorte PJ.
FAQ_EMPRESAS = [
    ("MEI pode conseguir crédito empresarial?",
     "Sim, dentro de linhas com critério específico para esse porte, como Pronampe e Procred 360. O "
     "enquadramento muda conforme faturamento anual e tempo de CNPJ; ver a página de Programas públicos "
     "para os critérios de cada um."),
    ("Qual a diferença entre capital de giro e financiamento?",
     "Capital de giro cobre o intervalo entre pagar fornecedores e receber de clientes, e não está preso "
     "a um bem específico. Financiamento amarra o crédito a um ativo determinado (imóvel, equipamento, "
     "veículo), com prazo e liberação vinculados a esse bem."),
    ("Um fundo garantidor, como o do Pronampe ou o PEAC FGI, garante a aprovação do crédito?",
     "Não. Esses fundos cobrem parte do risco da operação junto ao banco, o que facilita a análise de "
     "empresas sem garantia real suficiente, mas a aprovação, a taxa e o prazo continuam dependendo da "
     "instituição financeira responsável."),
    ("A partir de que valor a Acrópole atua em crédito empresarial?",
     "Para operações corporativas estruturadas, a partir de R$ 500 mil. Abaixo desse patamar, a maior "
     "parte das empresas costuma ser melhor atendida diretamente por linhas padronizadas, sem o custo e "
     "o tempo de uma estruturação sob medida. Dizemos isso já na primeira conversa."),
]


# ------------------------------------------------------------------ Empresas
def empresas():
    path = "empresas.html"
    trail = [("Início", "index.html"), ("Para empresas", None)]

    body = B.pagehead(
        path, trail, "Para empresas",
        "Uma empresa lucrativa pode ficar sem caixa. Isso tem nome, e tem solução estrutural.",
        "Quando o crédito acompanha a estratégia do negócio, ele financia crescimento. Quando não "
        "acompanha, financia o próprio custo e comprime a margem até o negócio parar de crescer.",
        meta=[("Ticket mínimo", "R$ 500 mil em operações corporativas estruturadas"),
              ("Linhas", "Giro, PJ, garantia real, aquisição e obra"),
              ("Análise", "Fluxo de caixa e composição do passivo")],
        variant=2, image_slot="empresas")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Diagnóstico", "Problemas que trazemos para a mesa antes de falar de valor.",
               "Se algum destes descreve a sua empresa, o próximo passo não é escolher uma linha. É dimensionar o problema.")}
    <div>{B.pointlist([
        "<strong>A necessidade de capital de giro cresce mais rápido que a receita.</strong> Em expansão, mais vendas significam mais estoque, mais produção financiada e prazos maiores concedidos a clientes. O gap cresce de forma não linear.",
        "<strong>Rotativo e cheque especial estão consumindo a margem.</strong> Linhas emergenciais resolvem a semana e comprometem o trimestre. Substituí-las costuma valer mais do que captar dinheiro novo.",
        "<strong>Há patrimônio, mas ele está imobilizado.</strong> Imóveis e equipamentos quitados podem lastrear capital sem que a empresa precise vendê-los, desde que o risco patrimonial seja tratado à parte do risco empresarial.",
        "<strong>Uma oportunidade não cabe no rito documental usual.</strong> Aquisição de concorrente, compra de estoque em condição excepcional ou entrada em licitação exigem prazo que o processo bancário padrão não entrega.",
        "<strong>O passivo está concentrado em poucos vencimentos.</strong> Alongar e redistribuir vencimentos muda a capacidade de pagamento sem alterar uma linha do faturamento.",
        "<strong>Há necessidade de investir sem imobilizar capital próprio.</strong> Equipamentos, imóveis operacionais e obra podem ser financiados preservando o caixa para o giro.",
    ], split=True)}</div>
  </div>
</section>"""

    lines = ["capital-de-giro", "credito-pj", "estruturacao-de-credito", "financiamento", "aquisicao-e-construcao"]
    app_cards = [
        (SOL_BY_SLUG[slug]["title"], SOL_BY_SLUG[slug]["short"],
         "solucoes/" + slug + ".html", "Ver a página")
        for slug in lines
    ]
    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Aplicações", "As estruturas que mais chegam à mesa em contexto empresarial.")}
    {B.linkcards(path, app_cards)}
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Como lemos uma empresa", "O que olhamos antes de sugerir qualquer estrutura.",
               "A segmentação que importa é por ciclo de caixa e qualidade do lastro, não por porte. Uma empresa com recebíveis pulverizados e boa conciliação pode representar risco menor que uma empresa maior concentrada em poucos clientes.")}
    {B.deflist([
        ("Ciclo financeiro", "Prazo médio de estoque, de recebimento e de pagamento. É a diferença entre eles que define o tamanho real da necessidade de giro."),
        ("Concentração", "Percentual da receita nos 5 maiores clientes e dependência de fornecedor único. Concentração alta encarece qualquer operação, com ou sem garantia."),
        ("Margem e volatilidade", "Margem operacional e sua variação nos últimos exercícios. Margem apertada com receita volátil restringe prazo antes de restringir valor."),
        ("Composição do endividamento", "Custo médio ponderado, perfil de vencimentos, garantias já comprometidas e cláusulas restritivas nos contratos vigentes."),
        ("Qualidade do lastro", "Recebíveis, duplicatas, adquirência, estoque, equipamentos e imóveis. O que é cedível, o que já foi cedido e o que é executável na prática."),
        ("Enquadramento em programas", "Pronampe, Procred 360 e PEAC FGI podem reduzir a exigência de garantia real para empresas elegíveis, mudando a estrutura possível."),
      ], split=True)}
  </div>
</section>"""

    body += f"""<section class="band band--stone band--snug">
  <div class="shell">
    {B.media_aside(path, "programas-publicos", "pagehead-1", "Programas públicos",
                   "Crédito com respaldo do governo, quando a empresa se enquadra.",
                   "Pronampe, Procred 360 e PEAC FGI existem para reduzir a exigência de garantia real de empresas elegíveis, ampliando o conjunto de instituições dispostas a analisar a operação.",
                   ["Verificação de enquadramento antes de qualquer proposta.",
                    "Comparação entre o mecanismo público e a alternativa com garantia real.",
                    "Condução junto às instituições credenciadas da rede."],
                   cta=("Falar sobre enquadramento", "contato.html"))}
    <div class="mt-2">{B.tlink("Compare Pronampe, Procred 360, PEAC FGI e BNDES, com simulador", "programas.html", path)}</div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    <div class="cols cols--7-5">
      <div>
        {B.sechead("Critério de atuação", "Onde nossa estrutura agrega, e onde ela não agrega.")}
        <p class="muted">Para operações corporativas estruturadas, trabalhamos a partir de R$ 500 mil. Abaixo desse patamar, a maior parte das empresas é melhor atendida diretamente por linhas padronizadas, sem o custo e o tempo de uma estruturação sob medida. Dizemos isso na primeira conversa, e não cobramos por essa leitura.</p>
        <p class="muted">Operações patrimoniais com garantia de imóvel ou de veículo seguem critérios próprios, ligados ao valor e à liquidez do bem, e são avaliadas caso a caso.</p>
      </div>
      <div>
        <div class="callout" data-reveal>
          <span class="tag">Contexto de mercado</span>
          <p class="mt-2 small muted">Em dezembro de 2025, o Brasil registrava 8,9 milhões de empresas inadimplentes e R$ 213 bilhões em dívidas negativadas, segundo a Serasa Experian. Micro e pequenas empresas respondiam por 8,5 milhões desse universo.</p>
          <p class="small muted">Isso significa que parte relevante da demanda por capital de giro é, na prática, demanda por reestruturação de passivo. Tratar as 2 como a mesma coisa é o erro mais caro desse mercado.</p>
        </div>
      </div>
    </div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Sobre crédito empresarial e capital de giro.")}
    {B.accordion(FAQ_EMPRESAS, "faq-empresas")}
    <p class="notice mt-3">{CONDITIONS_NOTICE}</p>
    <div class="mt-3 stack-2">
      {B.tlink("Como conseguir crédito para a empresa: documentos, prazo e o que pesa na análise", "conteudos/como-conseguir-credito-para-a-empresa.html", path)}
      {B.tlink("Documentos para solicitar crédito empresarial: o checklist antes de procurar um banco", "conteudos/documentos-para-solicitar-credito-empresarial.html", path)}
      {B.tlink("Capital de giro, Pronampe, Procred 360 ou BNDES: como decidir", "conteudos/capital-de-giro-pronampe-procred-360-ou-bndes.html", path)}
      {B.tlink("Como comparar alternativas de crédito empresarial pelo CET", "conteudos/como-comparar-credito-empresarial-pelo-cet.html", path)}
      {B.tlink("Pedido de crédito negado: o que fazer antes de tentar de novo", "conteudos/pedido-de-credito-negado-o-que-fazer.html", path)}
      {B.tlink("Ver o que a consultoria faz e o que não faz", "consultoria.html", path)}
    </div>
  </div>
</section>"""

    body += B.cta_band(path, "Traga o balanço e a lista de dívidas.",
                       "Com esses 2 documentos já é possível dizer se o problema é falta de capital ou composição de passivo, e quanto custaria corrigir cada um.",
                       secondary=("Ver o processo", "como-funciona.html"), tone="petrol")

    return {
        "path": path, "nav_key": "empresas.html", "over": True,
        "title": "Crédito empresarial e capital de giro | Acrópole Capital",
        "desc": ("Como conseguir crédito empresarial: capital de giro pelo ciclo de caixa, reestruturação "
                 "de passivo, aquisição e expansão. A partir de R$ 500 mil."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(FAQ_EMPRESAS)],
    }


# --------------------------------------------------------------- Investidores
def investidores():
    path = "investidores.html"
    trail = [("Início", "index.html"), ("Para investidores", None)]

    body = B.pagehead(
        path, trail, "Para investidores e incorporadores",
        "Capital próprio imobilizado é retorno que deixou de existir.",
        "Aquisição de terreno, incorporação, obra e expansão de ativos exigem uma estrutura que "
        "acompanhe o cronograma. Quando o desembolso não acompanha o avanço físico, a operação "
        "perde margem antes de vender a primeira unidade.",
        meta=[("Frentes", "Terreno, obra, aquisição e expansão"),
              ("Liberação", "Vinculada a avanço físico verificado"),
              ("Garantias", "Imóvel, projeto, recebíveis e corporativas")],
        variant=1, image_slot="investidores")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Contextos", "5 situações em que a estrutura decide o resultado.")}
    <div>{B.pointlist([
        "<strong>Aquisição de terreno com intenção de construir.</strong> Quando terreno e obra são contratados separadamente, o custo cartorário e o descasamento de prazo corroem margem. Avaliamos a viabilidade de contrato único.",
        "<strong>Incorporação com cronograma físico-financeiro.</strong> Liberação por etapa, vistoria de avanço, responsável técnico com ART ou RRT e amortização iniciando após a conclusão. O desenho aqui é tão relevante quanto a taxa.",
        "<strong>Expansão de ativo produtivo.</strong> Galpão, unidade fabril, ampliação. Podem entrar obra civil, instalações, equipamentos e capital de giro associado ao empreendimento financiado.",
        "<strong>Liquidez sobre portfólio imobiliário.</strong> Imóveis prontos, quitados ou com margem disponível, mobilizados como garantia sem que o investidor precise vendê-los em momento desfavorável.",
        "<strong>Recomposição de estrutura de capital.</strong> Substituir dívida cara de curto prazo por estrutura longa com garantia real, alinhando vencimentos ao ciclo de venda das unidades.",
    ], split=True)}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--top-rule">
  <div class="shell">
    {B.sechead("Leitura do projeto", "Os indicadores que acompanhamos em uma operação de obra.",
               "Volume de lançamentos não se confunde com rentabilidade nem com qualidade de crédito. O que sustenta uma operação de construção é a relação entre custo, velocidade de vendas e cronograma.")}
    {B.deflist([
        ("Velocidade de vendas sobre oferta", "Ritmo de absorção das unidades em relação ao estoque disponível. Determina se o cronograma financeiro tem folga ou depende de aceleração improvável."),
        ("Custo por unidade e curva de insumos", "Orçamento por unidade e sensibilidade a variação de material e mão de obra. É o principal vetor de perda de margem em ciclo longo."),
        ("Distratos e repasses", "Histórico de distratos e capacidade de repasse ao final da obra. Afeta diretamente o fluxo previsto de amortização."),
        ("Cobertura de juros durante a obra", "Capacidade de suportar a taxa incidente sobre o valor já liberado, antes do início da amortização."),
      ], split=True)}
    <p class="notice mt-3">Segundo a CBIC, o mercado imobiliário nacional registrou 453.005 unidades lançadas nos 12 meses até o quarto trimestre de 2025, com VGL de R$ 292,3 bilhões, alta de 10,6% sobre 2024. O crescimento conviveu com custo financeiro elevado, o que reforça a seletividade na estruturação.</p>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--snug">
  <div class="shell">
    {B.sechead("Estrutura por fase", "Cada fase tem uma garantia e um custo diferentes.")}
    <div class="rows rows--3">
      <div class="lift"><span class="lift__n figures">Fase 01</span><h3>Aquisição</h3><p class="small muted">Terreno ou imóvel pronto. Garantia sobre o próprio bem, alienação fiduciária e prazo dimensionado pela intenção de uso: revenda, incorporação ou operação.</p></div>
      <div class="lift"><span class="lift__n figures">Fase 02</span><h3>Obra</h3><p class="small muted">Liberação escalonada por vistoria de avanço físico. Durante o período, incide taxa sobre o valor já liberado, sem amortização de principal.</p></div>
      <div class="lift"><span class="lift__n figures">Fase 03</span><h3>Estabilização</h3><p class="small muted">Após a conclusão, início da amortização, repasses e eventual troca da estrutura de obra por uma estrutura de prazo mais longo e custo menor.</p></div>
    </div>
  </div>
</section>"""

    body += B.cta_band(path, "Traga o projeto, o orçamento e o cronograma.",
                       "Com esses 3 elementos é possível dizer qual estrutura sustenta a obra e onde o desenho atual deixa margem na mesa.",
                       secondary=("Ver aquisição e construção", "solucoes/aquisicao-e-construcao.html"), tone="ink")

    return {
        "path": path, "nav_key": "investidores.html", "over": True,
        "title": "Para investidores e incorporadores | Acrópole Capital",
        "desc": ("Estruturação de crédito para aquisição de terreno, incorporação, construção e expansão "
                 "de ativos, com liberação vinculada a cronograma físico-financeiro."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail)],
    }


# --------------------------------------------------------------- Agronegócio
def agronegocio():
    path = "agronegocio.html"
    trail = [("Início", "index.html"), ("Agronegócio", None)]

    body = B.pagehead(
        path, trail, "Para o agronegócio",
        "Safra tem calendário. Capital de giro rural precisa acompanhar esse calendário, não o do banco.",
        "Custeio, investimento em maquinário, armazenagem e comercialização têm ritmos diferentes entre si "
        "e diferentes do crédito empresarial comum. Estruturamos operações rurais respeitando essa "
        "sazonalidade, com a garantia e o instrumento certos para cada etapa do ciclo produtivo.",
        meta=[("Ciclo", "Custeio, investimento e comercialização"),
              ("Garantias", "CPR, penhor rural, alienação fiduciária, imóvel"),
              ("Análise", "Sazonalidade da safra e fluxo de caixa da propriedade")],
        variant=1, image_slot="agronegocio")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Contexto", "Por que crédito rural não é crédito empresarial com outro nome.",
               "A receita de uma operação rural se concentra em poucas janelas do ano. Tratar esse fluxo como se fosse mensal e recorrente, como em uma empresa urbana comum, é a origem de boa parte das operações rurais mal dimensionadas.")}
    <div>{B.pointlist([
        "<strong>Custeio precisa vencer depois da colheita, não antes dela.</strong> Insumo, defensivo e mão de obra são desembolsados no plantio e no manejo, mas a receita só entra na comercialização. Um vencimento mal calendarizado transforma uma safra boa em um problema de caixa.",
        "<strong>Investimento em maquinário compete com o próprio giro da propriedade.</strong> Trator, colheitadeira, silo e sistema de irrigação têm vida útil de anos, mas costumam ser negociados com prazo pensado em meses.",
        "<strong>Armazenagem muda o resultado da venda.</strong> Vender toda a safra na colheita, quando o preço costuma estar mais pressionado, é diferente de ter estrutura e capital para reter parte dela e comercializar de forma escalonada.",
        "<strong>Patrimônio rural é lastro subutilizado com frequência.</strong> Terra, benfeitorias e maquinário quitado podem lastrear operações de prazo mais longo, quando a estrutura da garantia é bem desenhada.",
    ], split=True)}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--top-rule">
  <div class="shell">
    {B.sechead("Instrumentos", "O ferramental próprio do crédito rural.",
               "Cada instrumento resolve uma etapa diferente do ciclo produtivo. Parte do nosso trabalho é identificar qual deles cabe em cada momento da operação, e qual instituição da rede tem apetite para ele.")}
    {B.deflist([
        ("CPR, a Cédula de Produto Rural",
         "Título que representa uma promessa de entrega de produto rural, física ou financeira. Serve tanto para captar recursos antes da colheita quanto para travar preço de venda com antecedência."),
        ("Penhor rural e alienação fiduciária",
         "Garantias específicas para safra em formação, maquinário e semoventes, com regras próprias de constituição e execução, diferentes das garantias usadas em operações urbanas."),
        ("Crédito de custeio agrícola",
         "Linha dimensionada para o intervalo entre o plantio e a colheita, com vencimento alinhado à comercialização da safra financiada."),
        ("Financiamento de investimento rural",
         "Prazo mais longo, voltado a maquinário, benfeitorias, irrigação e armazenagem, com amortização compatível com a vida útil do ativo financiado."),
      ], split=True)}
  </div>
</section>"""

    lines = ["capital-de-giro", "financiamento", "aquisicao-e-construcao", "home-equity"]
    rows = ""
    for slug in lines:
        s = SOL_BY_SLUG[slug]
        rows += B.artrow(path, "solucoes/" + slug + ".html", s.get("image"),
                         s["kicker"], s["title"], s["short"])
    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Aplicações", "As estruturas que também se aplicam ao produtor e à propriedade rural.",
               "As soluções abaixo não são exclusivas do agronegócio, mas costumam ser as mais adequadas quando o cliente é produtor rural ou tem patrimônio ligado à propriedade.")}
    <div class="artlist">{rows}</div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    <div class="cols cols--7-5">
      <div>
        {B.sechead("Como lemos uma operação rural", "O que olhamos antes de sugerir qualquer estrutura.")}
        <p class="muted">Cultura, ciclo produtivo, área própria e arrendada, histórico de produtividade e canal de comercialização definem o formato possível da operação antes de qualquer discussão sobre taxa. Uma safra vendida com contrato futuro tem um perfil de risco diferente de uma safra vendida no mercado à vista, mesmo com a mesma cultura e a mesma área.</p>
        <p class="muted">Também avaliamos o que já está comprometido: CPRs em aberto, penhor sobre a safra atual e financiamentos de maquinário em curso mudam quanto espaço a propriedade ainda tem para uma nova operação.</p>
      </div>
      <div>
        <div class="callout callout--fill" data-reveal>
          <h3>Sobre dados de mercado nesta página</h3>
          <p class="small muted">Não publicamos estatísticas do agronegócio brasileiro nesta página para evitar repetir número desatualizado ou fora de contexto. Na conversa com o produtor, trabalhamos com os dados da própria operação, não com médias de setor.</p>
        </div>
      </div>
    </div>
  </div>
</section>"""

    body += B.cta_band(path, "Traga o calendário da safra e o que já está comprometido.",
                       "Com o ciclo produtivo e o passivo atual em mãos, já é possível apontar qual instrumento se encaixa e em que janela do ano ele deveria vencer.",
                       secondary=("Ver o processo", "como-funciona.html"), tone="ink")

    return {
        "path": path, "nav_key": "agronegocio.html", "over": True,
        "title": "Crédito para o agronegócio | Acrópole Capital",
        "desc": ("Estruturação de crédito rural: custeio agrícola, maquinário, armazenagem, CPR e "
                 "penhor rural, com vencimento calendarizado pela safra."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail)],
    }


# ---------------------------------------------------------- Consultoria
FAQ_CONSULTORIA = [
    ("A Acrópole Capital é um banco?",
     "Não. A Acrópole Capital é uma consultoria de estruturação e intermediação de crédito. Quem "
     "empresta o dinheiro é sempre a instituição financeira parceira escolhida para cada operação."),
    ("Vocês garantem a aprovação do crédito?",
     "Não. Nenhuma consultoria pode garantir aprovação de crédito. O que fazemos é organizar a "
     "operação, o enquadramento e a documentação para que a análise da instituição financeira "
     "aconteça nas melhores condições possíveis, mas a decisão final é sempre do banco ou da "
     "cooperativa responsável."),
    ("Como a Acrópole Capital é remunerada?",
     "A forma de remuneração é apresentada por escrito antes de qualquer contratação, junto com a "
     "proposta da operação. Nenhum custo é cobrado sem estar explicitado previamente, e a "
     "comparação entre instituições parceiras é feita por critério técnico, não por qual delas "
     "remunera melhor a assessoria."),
    ("Vocês pedem senha ou acesso a sistemas da empresa?",
     "Não. Em nenhuma etapa do processo pedimos login, senha, token ou qualquer credencial de "
     "acesso a gov.br, e-CAC, internet banking ou qualquer outro sistema em nome do cliente."),
]


def consultoria():
    path = "consultoria.html"
    trail = [("Início", "index.html"), ("Consultoria de crédito empresarial", None)]

    body = B.pagehead(
        path, trail, "Consultoria e intermediação",
        "Consultoria de crédito empresarial: o que fazemos, e o que não fazemos.",
        "Estruturamos e intermediamos operações de crédito empresarial junto a uma rede de "
        "instituições financeiras. Não emprestamos dinheiro, não aprovamos crédito e não garantimos "
        "taxa. O papel da consultoria é reduzir o retrabalho e o tempo entre a necessidade da "
        "empresa e uma proposta comparável de crédito.",
        meta=[("Natureza", "Consultoria e intermediação, não instituição financeira"),
              ("Rede", "Múltiplas instituições financeiras parceiras"),
              ("Aprovação", "Sempre a critério da instituição financeira")],
        variant=2, image_slot="consultoria")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("O que fazemos", "As cinco etapas do trabalho de intermediação.")}
    <div class="mt-4">{B.sequence([
        ("Diagnóstico de elegibilidade", "Levantamos faturamento, garantias disponíveis, dívidas em aberto e o enquadramento em programas públicos antes de sugerir qualquer linha."),
        ("Organização da documentação", "Reunimos e organizamos o que toda instituição financeira costuma pedir, para reduzir idas e vindas durante a análise."),
        ("Identificação da estrutura adequada", "Definimos se a necessidade é capital de giro, financiamento, garantia real ou outra estrutura, e quais programas públicos se aplicam."),
        ("Comparação entre instituições", "Levamos a operação a mais de uma instituição da rede, e comparamos por custo efetivo total, prazo e condições, não só pela taxa anunciada."),
        ("Acompanhamento até a formalização", "Acompanhamos a negociação e a formalização junto à instituição escolhida, sem acessar sistemas ou credenciais da empresa em nenhum momento."),
    ])}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--top-rule">
  <div class="shell">
    {B.sechead("O que não fazemos", "Os limites do serviço, ditos de forma direta.")}
    <div>{B.pointlist([
        "Não somos um banco nem uma instituição financeira: não emprestamos dinheiro diretamente à empresa.",
        "Não aprovamos crédito. A decisão final, a taxa e o prazo são sempre definidos pela instituição financeira responsável.",
        "Não garantimos taxa, valor ou prazo antes da análise formal do banco ou da cooperativa.",
        "Não pedimos login, senha, token ou qualquer credencial de acesso a sistemas em nome do cliente, em nenhuma etapa.",
        "Não cobramos nenhum valor sem que a forma de remuneração esteja explicitada por escrito antes da contratação.",
    ], split=True)}</div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Sobre o papel da consultoria.")}
    {B.accordion(FAQ_CONSULTORIA, "faq-consultoria")}
    <div class="mt-3 stack-2">
      {B.tlink("Ver o processo completo, etapa por etapa", "como-funciona.html", path)}
      {B.tlink("Ver os critérios de governança", "governanca.html", path)}
      {B.tlink("Crédito empresarial em São Paulo", "credito-empresarial-sao-paulo.html", path)}
    </div>
  </div>
</section>"""

    body += B.cta_band(path, "Quer verificar se sua empresa se enquadra?",
                       "A análise inicial não gera compromisso e não consulta bureau de crédito sem sua autorização expressa.",
                       secondary=("Ver as 8 estruturas de crédito", "solucoes.html"), tone="petrol")

    return {
        "path": path, "nav_key": None, "over": True,
        "title": "Consultoria de crédito empresarial | Acrópole Capital",
        "desc": ("O que uma consultoria de intermediação de crédito empresarial faz, e o que ela não "
                 "faz: diagnóstico, documentação, comparação entre instituições e formalização."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(FAQ_CONSULTORIA)],
    }


FAQ_SP = [
    ("Preciso ir até o escritório na Avenida Paulista?",
     "Não necessariamente. Para empresas da capital e da região metropolitana, oferecemos reunião "
     "presencial mediante agendamento; para empresas do restante do país, o diagnóstico, a estruturação "
     "e a negociação seguem integralmente remotos, sem perda de etapa."),
    ("A Acrópole atende empresas de outras cidades, dentro ou fora de São Paulo?",
     "Sim. O atendimento presencial é mais frequente para empresas da capital e da região metropolitana, "
     "onde parte relevante da rede de instituições parceiras concentra força, mas o processo remoto "
     "atende empresas de qualquer cidade do país."),
    ("Existe um valor mínimo de operação para empresas em São Paulo?",
     "Para operações corporativas estruturadas, atuamos a partir de R$ 500 mil, o mesmo critério aplicado "
     "em qualquer praça. Abaixo desse patamar, a empresa costuma ser mais bem atendida por linhas "
     "padronizadas, sem o custo e o tempo de uma estruturação sob medida."),
]


# ---------------------------------------------- Crédito empresarial em SP
def credito_empresarial_sao_paulo():
    path = "credito-empresarial-sao-paulo.html"
    trail = [("Início", "index.html"), ("Crédito empresarial em São Paulo", None)]

    body = B.pagehead(
        path, trail, "São Paulo",
        "Crédito empresarial em São Paulo",
        f"A Acrópole Capital tem sede em São Paulo, na {CONTATO['endereco']}, e estrutura operações "
        "de crédito empresarial para empresas na cidade e na região metropolitana, com atendimento "
        "remoto para empresas do restante do país junto à mesma rede de instituições financeiras.",
        meta=[("Endereço", CONTATO["endereco"]),
              ("Atendimento", CONTATO["horario"] or "Sob agendamento"),
              ("Alcance", "São Paulo e região, com atendimento remoto nacional")],
        variant=1, image_slot="credito-empresarial-sp")

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Por que estruturar localmente", "Rede de relacionamento bancário concentrada na praça.")}
    <p class="muted">Boa parte da rede de instituições financeiras parceiras da Acrópole Capital opera com força em São Paulo, o que costuma facilitar reuniões presenciais, visitas técnicas e formalização mais rápida para empresas sediadas na cidade e na região metropolitana. Para empresas de outras praças, o processo de diagnóstico, estruturação e negociação segue integralmente remoto, sem perda de etapa.</p>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Estruturas mais buscadas por empresas paulistas", "As mesmas oito estruturas, com aplicação recorrente na praça.")}
    <div>{B.pointlist([
        "Capital de giro para empresas de comércio e serviço com ciclo financeiro apertado pela concentração de fornecedores na região metropolitana.",
        "Home equity e garantia imobiliária, dado o valor de mercado dos imóveis na cidade, para operações de prazo mais longo.",
        "Financiamento e enquadramento em Pronampe, Procred 360 e PEAC FGI para pequenas e médias empresas paulistas.",
    ], split=True)}</div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">{B.sechead("Como funciona, para uma empresa em São Paulo", "As mesmas 6 etapas do processo, com a logística ajustada à praça.")}
    <div>{B.sequence(PROCESS)}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell shell--tight">
    {B.sechead("Perguntas de quem está em São Paulo", "Logística, alcance e o que muda por estar na cidade.")}
    {B.accordion(FAQ_SP, "faq-sp")}
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Onde nos encontrar", "Endereço e formas de contato.")}
    {B.deflist([
        ("Endereço", CONTATO["endereco"]),
        ("Horário", CONTATO["horario"] or "Sob agendamento"),
        ("Atendimento", "Presencial em São Paulo, mediante agendamento, e remoto para todo o Brasil"),
      ], split=True)}
    <div class="mt-3 stack-2">
      {B.tlink("Como conseguir crédito para a empresa: documentos, prazo e o que pesa na análise", "conteudos/como-conseguir-credito-para-a-empresa.html", path)}
      {B.tlink("Ver o que fazemos e o que não fazemos", "consultoria.html", path)}
    </div>
  </div>
</section>"""

    body += B.cta_band(path, "Sua empresa é sediada em São Paulo?",
                       "Agende uma conversa presencial ou remota para levantar o enquadramento da sua empresa.",
                       secondary=("Ver as 8 estruturas de crédito", "solucoes.html"), tone="ink")

    return {
        "path": path, "nav_key": None, "over": True,
        "title": "Crédito empresarial em São Paulo | Acrópole Capital",
        "desc": ("Estruturação de crédito empresarial para empresas em São Paulo: capital de giro, "
                 "home equity, financiamento e programas públicos, com sede na Avenida Paulista."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(FAQ_SP), {
            "@context": "https://schema.org", "@type": "FinancialService",
            "name": "Acrópole Capital", "areaServed": {"@type": "City", "name": "São Paulo"},
            "address": {"@type": "PostalAddress", "streetAddress": CONTATO["endereco"],
                        "addressLocality": "São Paulo", "addressRegion": "SP", "addressCountry": "BR"},
        }],
    }


def pages():
    return [sobre(), como_funciona(), empresas(), investidores(), agronegocio(),
            consultoria(), credito_empresarial_sao_paulo()]
