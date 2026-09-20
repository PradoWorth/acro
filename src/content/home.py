# -*- coding: utf-8 -*-
"""Página inicial."""

from content.site import SITE, FACTS, SOLUTIONS, PARTNERS
from content import art
from content.kanban import board_html
import build as B


# Céu estrelado atrás do globo do hero: estrelas piscando + meteoros raros,
# confinados ao container do globo (não à viewport inteira, como no
# protótipo original) via getBoundingClientRect do próprio container, para
# que a densidade e o alcance dos meteoros acompanhem o tamanho real da
# caixa em qualquer breakpoint. Respeita prefers-reduced-motion: nesse caso
# as estrelas aparecem estáticas na opacidade máxima e nenhum meteoro é
# agendado — mesmo tratamento que o globo já dá ao giro automático.
STARFIELD_JS = """(function () {
  var container = document.getElementById('acr-stars-hero');
  if (!container) return;
  var prefersReducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var STAR_COLORS = ['#ffffff', '#ffffff', '#ffffff', '#fff4d6', '#d6e6ff'];

  function starCountForContainer() {
    var rect = container.getBoundingClientRect();
    var area = Math.max(rect.width, 1) * Math.max(rect.height, 1);
    var density = 0.00028;
    return Math.max(40, Math.min(140, Math.round(area * density)));
  }

  function makeStar() {
    var star = document.createElement('div');
    star.className = 'hero-stars__star';
    var roll = Math.random();
    var size, maxOpacity, glow;
    if (roll < 0.75) { size = Math.random() * 0.5 + 0.3; maxOpacity = Math.random() * 0.35 + 0.25; glow = false; }
    else if (roll < 0.95) { size = Math.random() * 0.6 + 0.8; maxOpacity = Math.random() * 0.3 + 0.5; glow = false; }
    else { size = Math.random() * 0.8 + 1.4; maxOpacity = Math.random() * 0.2 + 0.8; glow = true; }
    var colorIdx = Math.floor(Math.random() * STAR_COLORS.length);
    var color = STAR_COLORS[colorIdx];
    star.style.width = size + 'px';
    star.style.height = size + 'px';
    star.style.background = color;
    star.style.left = (Math.random() * 100) + '%';
    star.style.top = (Math.random() * 100) + '%';
    if (prefersReducedMotion) {
      star.style.opacity = maxOpacity.toFixed(2);
    } else {
      star.style.setProperty('--min-o', (Math.random() * 0.08 + 0.02).toFixed(2));
      star.style.setProperty('--max-o', maxOpacity.toFixed(2));
      star.style.animationDuration = (size > 1.2 ? (Math.random() * 4 + 4) : (Math.random() * 3 + 1.5)) + 's';
      star.style.animationDelay = (Math.random() * 6) + 's';
    }
    if (glow) star.style.boxShadow = '0 0 ' + (size * 1.8).toFixed(1) + 'px ' + color;
    return star;
  }

  function clearStars() {
    var old = container.querySelectorAll('.hero-stars__star');
    for (var i = 0; i < old.length; i++) old[i].remove();
  }

  function createStars() {
    // Mede o container ANTES de remover as estrelas antigas, não depois:
    // clearStars() tira nós do DOM (uma escrita que invalida o layout), e
    // pedir getBoundingClientRect() logo em seguida força o navegador a
    // recalcular o layout ali mesmo, de forma síncrona, só para responder
    // a leitura — um "reflow forçado" (detectado pela auditoria de
    // performance). Como remover as estrelas antigas não muda o tamanho do
    // próprio container (elas não influenciam a caixa dele), inverter a
    // ordem (ler primeiro, escrever depois) dá exatamente o mesmo número,
    // sem forçar nenhum recálculo de layout fora do ciclo normal do
    // navegador.
    var count = starCountForContainer();
    clearStars();
    var frag = document.createDocumentFragment();
    for (var i = 0; i < count; i++) frag.appendChild(makeStar());
    container.appendChild(frag);
  }

  createStars();

  var resizeTimeout;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function () {
      if (!container.isConnected) return;
      createStars();
    }, 250);
  });

  if (prefersReducedMotion) return; // sem meteoros: respeita a preferência de menos movimento

  function createMeteor() {
    if (!container.isConnected) return;
    var rect = container.getBoundingClientRect();
    if (rect.width < 10 || rect.height < 10) return;
    var meteor = document.createElement('div');
    meteor.className = 'hero-stars__meteor';
    var startX = Math.random() * rect.width * 0.6 + rect.width * 0.2;
    var startY = -10;
    var angleDeg = 55 + Math.random() * 15;
    var distance = Math.random() * (rect.height * 0.5) + rect.height * 0.35;
    var rad = angleDeg * Math.PI / 180;
    var dx = Math.cos(rad) * distance;
    var dy = Math.sin(rad) * distance;
    meteor.style.left = startX + 'px';
    meteor.style.top = startY + 'px';
    meteor.style.setProperty('--dx', dx + 'px');
    meteor.style.setProperty('--dy', dy + 'px');
    meteor.style.setProperty('--peak-o', (Math.random() * 0.3 + 0.25).toFixed(2));
    meteor.style.animationDuration = (Math.random() * 1.0 + 1.1) + 's';
    var core = document.createElement('div');
    core.className = 'hero-stars__meteor-core';
    core.style.setProperty('--angle', angleDeg + 'deg');
    meteor.appendChild(core);
    container.appendChild(meteor);
    meteor.addEventListener('animationend', function () { meteor.remove(); });
  }

  function scheduleMeteor() {
    if (!container.isConnected) return; // rota trocou: encerra a cadeia em vez de acumular timers
    var longPause = Math.random() < 0.35;
    var delay = longPause ? (Math.random() * 9000 + 9000) : (Math.random() * 5000 + 4000);
    setTimeout(function () {
      createMeteor();
      scheduleMeteor();
    }, delay);
  }

  scheduleMeteor();
  setTimeout(createMeteor, 2200);
})();"""


MARKET = [
    ("R$ 7,07 bi",
     "Concessões de capital de giro PJ acima de 365 dias em julho de 2026, ante R$ 10,70 bi em junho.",
     "Séries SGS, Banco Central do Brasil"),
    ("23,55% a.a.",
     "Taxa média da mesma modalidade no período. A dispersão entre instituições é o que decide o custo real.",
     "Séries SGS, Banco Central do Brasil"),
    ("+25,83%",
     "Crescimento das concessões de crédito com garantia de imóvel no primeiro trimestre de 2026.",
     "Abecip"),
    ("R$ 213 bi",
     "Dívidas empresariais negativadas em dezembro de 2025, com 8,9 milhões de empresas inadimplentes.",
     "Serasa Experian"),
]


def hero(path):
    facts = "".join(
        f'<div class="factrail__cell"><span class="factrail__n figures">{v}</span>'
        f'<span class="factrail__l">{l}</span></div>' for v, l in FACTS
    )
    return f"""<section class="hero">
  <div class="hero__grid">
    <div class="hero__inner">
      <h1>Crédito como ferramenta de crescimento, não como solução emergencial.</h1>
      <p class="hero__sub">Estruturamos crédito corporativo e capital de giro para empresas com demandas financeiras robustas, com inteligência, discrição e visão de longo prazo.</p>
      <div class="btn-row">
        {B.btn("Solicitar uma análise", "contato.html", path)}
        {B.btn("Conhecer as soluções", "solucoes.html", path, "btn--line")}
      </div>
    </div>
    <div class="hero__media hero__media--globe" aria-hidden="true">
      <div class="hero-stars" id="acr-stars-hero"></div>
      <canvas id="acr-globe-hero"></canvas>
    </div>
  </div>
  <div class="factrail-rule"></div>
  <div class="shell"><div class="factrail">{facts}</div></div>
  <script>{STARFIELD_JS}</script>
</section>"""


def positioning(path):
    body = f"""<div class="stack-2">
          <p class="lead">2 empresas com o mesmo faturamento e a mesma necessidade de caixa raramente deveriam contratar a mesma operação. O que muda não é o valor: é o ciclo, a qualidade do lastro, o passivo já contratado e o horizonte da decisão.</p>
          <p class="muted">Por isso não trabalhamos com um catálogo. Levantamos o contexto, dimensionamos a necessidade real e só então procuramos, dentro da nossa rede, a estrutura que sustenta aquele objetivo pelo prazo em que ele precisa ser sustentado. Quando a resposta certa é não contratar, dizemos isso.</p>
          {B.pullquote("A pergunta não é quanto capital cabe. É qual estrutura sustenta a decisão pelo prazo em que ela precisa ser sustentada.")}
      </div>"""
    return f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Posicionamento", "Estruturamos a operação antes de procurar o capital.")}
    {B.media_row(path, "home-estrutura", "pagehead-0", body)}
    <div class="mt-4">{B.iconcards([
        ("Objetivo", "O que o capital precisa viabilizar, e em que prazo isso se paga.", B.ICON_TARGET),
        ("Estrutura", "O passivo já existente, seu custo e o que dele pode ser substituído.", B.ICON_LAYERS),
        ("Patrimônio e garantias", "Quais ativos podem ser mobilizados sem comprometer a operação ou a família.", B.ICON_SHIELD),
        ("Capacidade e risco", "O fluxo de caixa que efetivamente sustenta a parcela, no cenário realista.", B.ICON_GAUGE),
    ], four=True, variant="line")}</div>
  </div>
</section>"""


def solutions(path):
    rows = "".join(
        f'<button class="solrow" role="tab" id="solrow-{s["slug"]}" data-sol="{s["slug"]}" '
        f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="solpanel-{s["slug"]}">'
        f'<span class="solrow__n">{i + 1:02d}</span>'
        f'<span class="solrow__body">'
        f'<span class="solrow__t">{s["title"]}</span>'
        f'<span class="solrow__k">{s["kicker"]}</span></span></button>'
        for i, s in enumerate(SOLUTIONS)
    )
    panels = ""
    for i, s in enumerate(SOLUTIONS):
        chips = "".join(f'<span class="chip">{c}</span>' for c in s["chips"])
        panels += f"""<div class="solpanel" role="tabpanel" id="solpanel-{s['slug']}"
          aria-labelledby="solrow-{s['slug']}" data-sol="{s['slug']}" data-active="{'true' if i == 0 else 'false'}">
          <div class="solpanel__art">{B.inline_diagram(s["art"])}</div>
          <h3>{s['title']}</h3>
          <p class="muted">{s['short']}</p>
          <div class="solpanel__facts">{chips}</div>
          {B.tlink("Ver a página de " + s["title"], "solucoes/" + s["slug"] + ".html", path)}
        </div>"""

    return f"""<section class="band band--ink band--top-rule">
  <div class="shell">
    {B.sechead("Soluções", "8 formas de estruturar capital. Cada uma responde a um problema diferente.",
               "Percorra a lista para ver o desenho de cada operação, o que ela resolve e onde ela costuma ser mal empregada.")}
    <div class="solindex">
      <div class="solindex__list" role="tablist" aria-label="Soluções da Acrópole Capital">{rows}</div>
      <div class="soldetail">{panels}</div>
    </div>
  </div>
</section>"""


def method(path):
    body = B.sequence([
            ("Leitura do passivo",
             "Mapeamos as dívidas contratadas, taxas, prazos e garantias já comprometidas. Boa parte do ganho de uma operação bem estruturada vem daqui, antes de qualquer dinheiro novo entrar."),
            ("Leitura do patrimônio",
             "Avaliamos os ativos disponíveis, o saldo devedor de cada um e a margem realista de aproveitamento. Garantia superavaliada não é vantagem: é atraso na formalização."),
            ("Comparação estrutural",
             "Comparamos instituições pela natureza jurídica, pela base legal da garantia e pelo custo efetivo total. Taxa de vitrine e custo real quase nunca coincidem."),
            ("Recomendação técnica",
             "Apresentamos a estrutura recomendada com os números da simulação e os cenários alternativos. A decisão final é sempre do cliente, com a informação completa na mesa."),
        ])
    # Depoimentos entram dentro desta mesma seção clara ("band" lisa, sem
    # tom próprio), logo abaixo do bloco de metodologia — pedido do
    # cliente para não ter uma faixa cinza (band--stone) separando os dois
    # visualmente, já que o assunto (a leitura que o diagnóstico faz) é o
    # mesmo. A cor só muda depois, na faixa seguinte ("Resultado").
    return f"""<section class="band">
  <div class="shell">
    {B.sechead("Metodologia", "Como um diagnóstico é conduzido.",
               note="O processo completo, com documentação e prazos, está descrito na página dedicada.",
               link=("Ver o processo completo", "como-funciona.html"), path=path)}
    <div class="mt-4">{B.media_row(path, "home-diagnostico", "pagehead-1", body)}</div>
    <div class="mt-4">{_testimonials_block()}</div>
  </div>
</section>"""


def journey(path):
    """Quadro animado "como trabalhamos" (ver content/kanban.py) — um caso
    fictício avançando pelas etapas internas, para dar ao visitante a visão
    geral do processo (as 5 etapas) antes do zoom no diagnóstico, em
    method(), logo a seguir. O CTA abaixo do quadro liga a etapa 1
    (Primeiro contato) à ação que o próprio leitor precisa tomar agora —
    pedido do cliente, para que o quadro não seja só ilustrativo. Sem
    band--top-rule: essa seção vem logo depois de "Soluções", também
    escura — a linha de separação (pensada para marcar transição de cor)
    ficava sobrando entre duas seções do mesmo tom, a pedido do cliente."""
    return f"""<section class="band band--ink">
  <div class="shell">
    {B.sechead("Como trabalhamos", "Da primeira conversa ao capital liberado.",
               "Um retrato simplificado de como um caso avança pelas etapas internas; cada operação real tem seu próprio ritmo.",
               link=("Ver o processo completo", "como-funciona.html"), path=path)}
    <div class="mt-4" data-reveal>{board_html()}</div>
    <div class="jb__cta" data-reveal>
      <p class="jb__cta-l">Etapa 1 começa por aqui.</p>
      {B.btn("Solicitar análise", "contato.html", path)}
    </div>
  </div>
</section>"""


def results(path):
    return f"""<section class="band band--stone band--top-rule">
  <div class="shell">
    <div data-reveal class="stack-2">
      <span class="tag sechead__tag">Resultado</span>
      <h2 class="measure-narrow"><span class="figures">92%</span> de aprovação nas operações que estruturamos.</h2>
      <p class="lead">O número nasce de um filtro anterior à submissão: só chega ao crédito a operação já comparada por natureza jurídica, garantia e custo efetivo entre as instituições da rede.</p>
      <p class="notice">Refere-se às operações estruturadas e submetidas pela Acrópole Capital às instituições parceiras. A aprovação final, as condições e o prazo são sempre decisão exclusiva da instituição financeira responsável.</p>
    </div>
  </div>
</section>"""


def audiences(path):
    cards = [
        ("card-empresas", "Empresas", "empresas.html", "Ver soluções para empresas",
         "Capital de giro dimensionado pela necessidade real, reestruturação de passivo caro, aquisição de ativos e expansão. Para operações corporativas estruturadas, trabalhamos a partir de R$ 500 mil."),
        ("card-investidores", "Investidores e incorporadores", "investidores.html", "Ver soluções para investidores",
         "Aquisição de terreno, incorporação, obra e expansão de ativos, com liberação vinculada a cronograma físico-financeiro e estrutura de garantias desenhada por fase."),
        ("card-agro", "Agronegócio", "agronegocio.html", "Ver soluções para o agro",
         "Custeio de safra, CPR, aquisição de maquinário e expansão de área, com garantia e prazo pensados para o calendário agrícola, não para o calendário bancário."),
        ("card-patrimonio", "Patrimônio pessoal", "solucoes/home-equity.html", "Ver home equity",
         "Empresários e famílias com patrimônio imobiliário que buscam liquidez ou substituição de dívida cara, com avaliação honesta do risco de comprometer o bem."),
    ]
    out = ""
    for i, (slot, title, href, link_label, text) in enumerate(cards, 1):
        img = B.card_photo(path, slot)
        out += f"""<div class="lift">
          {img}
          <span class="lift__n figures">0{i}</span>
          <h3>{title}</h3>
          <p class="muted small" style="max-width:38ch">{text}</p>
          <div class="mt-1">{B.tlink(link_label, href, path)}</div>
        </div>"""
    return f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Quem atendemos", "4 contextos, exigências distintas.", wide=True)}
    <div class="rows rows--3">{out}</div>
  </div>
</section>"""


def network(path):
    return B.netband(
        path, "Rede",
        "74 instituições. 6 nações. 1 pilar.",
        "Acesso amplo não é argumento de vitrine: é o que permite recusar uma condição ruim e "
        "buscar outra. Contamos com braço financeiro próprio e conexão ativa com mais de 74 "
        "instituições no Brasil, na Inglaterra, em Portugal, na Suíça, nos Estados Unidos e "
        "nos Emirados Árabes Unidos.",
        [
            "<strong>Bancos, cooperativas, SCDs, SEPs e fintechs de crédito com garantia real.</strong> Cada natureza jurídica se comporta de um jeito quando o cenário aperta, e é por isso que comparamos entre elas.",
            "<strong>Funding nacional e internacional.</strong> Operações que se beneficiam de custo ou prazo diferentes dos praticados internamente podem ser levadas ao exterior.",
            "<strong>Um único pilar sustenta a operação do cliente</strong>, mesmo quando ela envolve mais de um credor, garantias hierarquizadas e formalizações em sequência.",
        ],
        cta=("Conhecer a estrutura da empresa", "sobre.html"))


def partners(path):
    strip = B.partners_strip(path, PARTNERS)
    if not strip:
        return ""
    return f"""<section class="band band--stone band--tight band--top-rule">
  <div class="shell">{strip}</div>
</section>"""


def market(path):
    cells = ""
    for v, d, src in MARKET:
        cells += f"""<div class="statrail__c">
          <span class="statrail__v figures">{v}</span>
          <span class="statrail__l">{d}</span>
          <span class="statrail__l" style="color:var(--slate-2);margin-top:.5rem">{src}</span>
        </div>"""
    return f"""<section class="band band--top-rule">
  <div class="shell">
    {B.sechead("Leitura de mercado",
               "Trabalhamos com os números públicos, não com impressões.",
               "Acompanhamos as séries do Banco Central, os dados setoriais e os indicadores de inadimplência porque eles mudam a recomendação. Um mesmo pedido de capital de giro recebe respostas diferentes conforme o custo do funding e a seletividade do momento.")}
    <div class="statrail statrail--4" data-reveal>{cells}</div>
    <p class="notice mt-3">Dados públicos referentes ao período mais recente disponível em cada fonte, consultados em setembro de 2026. Séries de concessão são fluxo mensal e sofrem sazonalidade relevante: uma queda mensal não indica, por si só, contração estrutural.</p>
  </div>
</section>"""


# Mesmos 4 programas de content/programas.py (nome + slug da âncora na
# página). Lista curta e estável o bastante para não valer a pena importar
# o módulo inteiro só por isto; se um programa for adicionado ou renomeado
# lá, replicar aqui.
_PROGRAM_CHIPS = [
    ("BNDES", "bndes"),
    ("PEAC FGI", "peac-fgi"),
    ("Pronampe", "pronampe"),
    ("Procred 360", "procred-360"),
]


def programs(path):
    # Vai direto para a página isolada do programa (programas/<slug>.html),
    # não para a âncora na página de visão geral — mesma mudança de
    # navegação feita no menu (ver mega_programas/drawer em build.py).
    chips = "".join(
        f'<a class="chip" href="{B.rel(path, "programas/" + slug + ".html")}">{name}</a>'
        for name, slug in _PROGRAM_CHIPS
    )
    return f"""<section class="band band--stone">
  <div class="shell">
    {B.media_aside(path, "programas-publicos", "pagehead-1", "Simulador gratuito",
                   "BNDES, PEAC FGI, Pronampe e Procred 360, num só lugar.",
                   "Antes de procurar garantia real, verificamos se a empresa se enquadra em algum programa "
                   "público de crédito ou garantia. Quando cabe, isso costuma reduzir exigência de garantia "
                   "ou baixar o custo final. Veja como funciona cada um e simule valor, taxa e parcela.",
                   ["Regras de elegibilidade de cada programa, lado a lado.",
                    "Simulador de valor, taxa e parcela, sem enviar nenhum dado.",
                    "Verificação de enquadramento junto a um especialista, quando fizer sentido."],
                   cta=("Simular agora", "programas.html"))}
    <p class="xs muted" style="margin:2rem 0 .5rem">Ir direto para:</p>
    <div class="solpanel__facts">{chips}</div>
  </div>
</section>"""


# Depoimentos reais de clientes do Diagnóstico 360 (produto anterior da
# Acrópole Capital), reaproveitados a pedido do cliente. Sem foto (o material
# de origem também não tinha), sem sobrenome completo e sem nome de empresa,
# só o setor e o estado — mesmo nível de identificação do material original.
TESTIMONIALS = [
    ("A restrição que travava tudo tava no CPF do meu sócio, e nenhum banco tinha me dito isso antes. "
     "Foi o diagnóstico que trouxe essa resposta com clareza.", "Marcos T.", "Indústria · SP"),
    ("O relatório mostrou exatamente o que a mesa de crédito enxergava como risco, e isso me deu tempo "
     "pra corrigir antes de fazer um novo pedido.", "Renata C.", "Comércio · MG"),
    ("Já levei duas negativas sem entender o porquê. O diagnóstico não enrolou, foi direto nos pontos "
     "que eu precisava corrigir na empresa.", "Fábio A.", "Serviços · PR"),
    ("Eu sempre achei que faturamento era tudo o que importava. O diagnóstico abriu meus olhos pra "
     "outros pontos que vinham pesando contra a aprovação.", "Juliana M.", "Varejo · RS"),
    ("Antes eu só pedia crédito e ficava na expectativa. Hoje sei exatamente o que uma mesa de crédito "
     "olha, e isso mudou completamente como preparo a empresa antes de qualquer pedido.",
     "Rodrigo L.", "Logística · GO"),
    ("Eu já desconfiava que o problema não era só faturamento, mas não sabia por onde começar a "
     "investigar. O diagnóstico organizou isso em poucos dias e me poupou meses de tentativa e erro.",
     "André P.", "Agronegócio · MT"),
]


def _testimonials_block():
    """Bloco de depoimentos (sem <section> própria): chamado de dentro da
    seção "Metodologia", em method(), para os cartões ficarem na mesma
    faixa clara em vez de numa seção separada com cor própria — pedido
    do cliente, ver comentário em method()."""
    def card(quote, name, tag):
        return f"""<div class="lift testirow__card">
          <p>“{quote}”</p>
          <div class="lift__foot">
            <strong>{name}</strong>
            <span class="small muted">{tag}</span>
          </div>
        </div>"""
    cards = "".join(card(*t) for t in TESTIMONIALS)
    # Lista real para leitor de tela: a esteira animada duplica os cartões
    # pra fechar o loop sem costura (ver partners_strip, mesmo raciocínio),
    # e essa duplicação fica oculta de quem usa leitor de tela — aqui embaixo
    # está o conteúdo de verdade, uma vez só, na ordem certa.
    sr = "".join(
        f"<li>“{quote}” <strong>{name}</strong>, {tag}</li>" for quote, name, tag in TESTIMONIALS
    )
    # Sem cabeçalho visível (tag + título) — pedido do cliente para os
    # cartões não anunciarem uma seção própria no meio do caminho. O
    # <h2> continua existindo, só oculto visualmente (classe .sr, o
    # mesmo recurso da lista de leitor de tela abaixo), pra manter a
    # hierarquia de títulos da página sem reintroduzir o texto na tela.
    return f"""<h2 class="sr">Depoimentos: o que dizem empresários que já passaram pelo diagnóstico</h2>
    <div class="testirow" data-reveal>
      <ul class="sr">{sr}</ul>
      <div class="testirow__track" aria-hidden="true">{cards}{cards}</div>
    </div>"""


def featured(path):
    from content.conteudos import ARTICLES
    rows = ""
    for a in ARTICLES[:3]:
        rows += B.artrow(path, "conteudos/" + a["slug"] + ".html", a.get("image"),
                          a["category"], a["title"], a["excerpt"],
                          foot=f"{a['date_label']} · {a['read']}")
    return f"""<section class="band band--top-rule">
  <div class="shell">
    {B.sechead("Conteúdos", "Material técnico para quem decide sobre crédito.",
               "Escrevemos sobre o que costuma custar caro por falta de informação: custo efetivo, prazo, garantia e o momento certo de cada estrutura.")}
    <div class="artlist">{rows}</div>
    <div class="mt-3">{B.tlink("Ver todos os conteúdos", "conteudos.html", path)}</div>
  </div>
</section>"""


# Perguntas que cruzam qualquer estrutura, não uma dúvida específica de
# solução (essas já têm FAQ própria em cada página). Cada resposta reaproveita
# um fato já publicado em algum outro lugar do site (prazo de retorno e
# ausência de compromisso em contato.py, natureza da empresa em LEGAL_LINE),
# nunca uma promessa nova.
FAQ_HOME = [
    ("Vocês são um banco ou uma instituição financeira?",
     "Não. A Acrópole atua na assessoria e estruturação de operações de crédito, e não concede "
     "crédito diretamente. A decisão final, a taxa e o prazo são sempre definidos pela instituição "
     "financeira responsável pela operação."),
    ("Preencher o formulário de contato me compromete a alguma coisa?",
     "Não. O envio não representa solicitação formal de crédito nem aprovação, e nenhuma consulta a "
     "bureau de crédito é feita sem a sua autorização expressa."),
    ("Em quanto tempo eu recebo uma resposta?",
     "Em até 2 minutos, pelo canal que você indicar no formulário de contato. A leitura técnica "
     "completa da operação vem na conversa seguinte."),
    ("Preciso já saber qual das 8 estruturas procurar?",
     "Não. Se não tiver certeza, o diagnóstico rápido leva menos de um minuto e aponta uma direção "
     "antes da conversa, ou você pode simplesmente descrever a situação no formulário de contato."),
]


def faq(path):
    return f"""<section class="band band--stone">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Antes de você escrever para a gente.",
               "Perguntas que aparecem antes de qualquer detalhe da operação. As dúvidas específicas de cada estrutura estão na página dela.")}
    {B.accordion(FAQ_HOME, "faq-home")}
    <div class="mt-3">{B.tlink("Não encontrou sua dúvida? Fale com um especialista", "contato.html", path)}</div>
  </div>
</section>"""


def pages():
    path = "index.html"
    # Ordem pensada como uma leitura sequencial única (pedido do cliente):
    # Posicionamento (por quê) -> Soluções (o quê) -> Como trabalhamos, a
    # visão geral do processo em 5 etapas -> Metodologia, o zoom na etapa
    # de diagnóstico que acabou de aparecer no quadro, com os Depoimentos
    # (a prova social) dentro da própria seção, na mesma faixa clara ->
    # Resultado, reforçando a credibilidade que os depoimentos acabaram de
    # construir -> daí em diante, segmentação, amplitude, autoridade e
    # conversão, na mesma ordem de antes.
    #
    # "programs" (BNDES/PEAC FGI/Pronampe/Procred 360) subiu de perto do fim
    # da página para logo depois de "solutions": o cliente relatou que, ao
    # navegar pelo próprio site, não achava com facilidade onde pesquisar
    # essas linhas — enterrada como 11ª de 13 seções, a leitura sequencial
    # original nunca chegava lá pra quem não rolava a página inteira. Ficou
    # como continuação natural de "o que fazemos" (soluções) com "o que já
    # existe pronto" (programas públicos), antes de entrar no processo.
    body = (hero(path) + partners(path) + positioning(path) + solutions(path)
            + programs(path)
            + journey(path) + method(path)
            + results(path) + audiences(path) + network(path) + market(path)
            + featured(path)
            + faq(path)
            + B.cta_band(path,
                         "Traga o contexto. Devolvemos uma leitura técnica.",
                         "Uma conversa inicial não gera compromisso nem consulta a bureau. Serve para entender se a estrutura que você procura existe e sob quais condições.",
                         tone="petrol"))
    return [{
        "path": path,
        "nav_key": None,
        "over": True,
        "title": "Acrópole Capital | Estruturação de crédito e capital de giro",
        "desc": ("Assessoria em estruturação de crédito, capital de giro, home equity, auto equity e "
                 "financiamento. Comparação por custo efetivo total, rede de 74+ instituições."),
        "body": body,
        "schema": [B.org_schema(), {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Acrópole Capital",
            "url": SITE["domain"],
            "inLanguage": "pt-BR",
        }, B.faq_schema(FAQ_HOME)],
    }]
