# -*- coding: utf-8 -*-
"""
Quadro animado "como trabalhamos": um kanban com uma mãozinha arrastando um
caso fictício pelas etapas internas do processo, pedido pelo cliente a
partir de uma referência (peça da Incorapp, para outra marca) que ele mandou
pronta — refeita aqui do zero com a paleta, a tipografia (Inter, sem fonte
externa nova) e os tokens do próprio site, sem GSAP (biblioteca de terceiro
que a referência usava): a animação é toda CSS transition + um punhado de
JS vanilla, do mesmo jeito que o resto do site (ver content/globe.py).

O título/eyebrow que vinham dentro da peça original ("Gestão de projeto" /
"O board no Trello.") NÃO entram aqui — o cliente pediu para tirá-los; quem
banca o título da seção é o B.sechead(...) de quem chama board_html(), como
em qualquer outra seção do site. Também não há botão "Reiniciar" nem legenda
abaixo do quadro (removidos a pedido do cliente) — o quadro só reanima
sozinho ao reentrar no viewport ou após um resize. Em tablet/desktop o
board é uma grade responsiva (repeat(auto-fit, minmax(...))): reflui em
menos colunas por linha conforme o espaço disponível encolhe.

No mobile (< 48rem) a grade vira carrossel horizontal com scroll-snap: as
5 etapas são uma sequência (1→5), e um grid de 2 colunas força ler em
zigue-zague (etapa 1 e 2 lado a lado, 3 e 4 na linha de baixo, 5 sozinha
cortando a viewport). Carrossel devolve a ordem 1→5 num fluxo só, na
direção que já é natural no toque, e cada card ganha a largura cheia pra
ler sem espremer. A mãozinha, o popover "Aprovar" e o confete somem
nessa largura (ver isCarousel() em KANBAN_JS) — mesmo de mouse, numa
janela de notebook simplesmente estreita, não só em toque de verdade.

Já existiu uma versão mais fina desta regra (só excluía TOQUE de
verdade — `hover:none`/`pointer:coarse` — deixando a mão rodar numa
janela de mouse estreita, com o carrossel rolando sozinho para
acompanhar a demonstração). Revertida a pedido do cliente: em celular
de verdade a combinação "carrossel rolando sozinho" + "a própria
pessoa tentando rolar com o dedo ao mesmo tempo" produzia um bug real
onde a pessoa não conseguia mais navegar o quadro — o motivo exato
não foi isolado (a detecção de toque via CSS pode falhar em algum
navegador/aparelho específico, entre outras causas possíveis), mas a
combinação "largura pequena → sem mão, sem scroll automático, carrossel
só reage ao dedo da pessoa" é a mesma que o quadro já usava antes de
qualquer mudança nesta área, e nunca causou esse problema. Não animar
aqui é mais simples e mais seguro do que caçar a causa exata de um bug
que só aparece em aparelho real.
"""

# Uma etapa = (título da coluna, lista de cartões). Cada cartão:
#   tag: "info" | "done" | "alert"  — só 3 cores, as já usadas no resto do
#        site (cobalt / iris / danger), em vez de inventar uma paleta nova
#        só para este componente.
#   label: texto da etiqueta
#   title: título do cartão
#   sub: texto pequeno abaixo (ou None)
#   demo: True no único cartão que a mãozinha manipula
#   pop: True nesse mesmo cartão — é onde abre o menu Aprovar/Pedir ajuste
STAGES = [
    ("Primeiro contato", [
        dict(tag="info", label="Novo", title="Solicitação recebida", sub="via formulário do site"),
        dict(tag="info", label="Em andamento", title="Retorno com consultor agendado", sub="dentro de 1 dia útil"),
    ]),
    ("Diagnóstico com Consultor", [
        dict(tag="done", label="Concluído", title="Leitura do passivo e do patrimônio"),
        dict(tag="info", label="Em andamento", title="Comparação entre instituições"),
    ]),
    ("Elegibilidade", [
        dict(tag="done", label="Aprovado", title="Nenhuma restrição bancária identificada"),
        dict(tag="alert", label="Atenção", title="Pendência em nome de sócio", sub="em regularização"),
    ]),
    ("Documentação", [
        dict(tag="info", label="Recebido", title="Contrato social e balanço"),
        dict(tag="info", label="Para aprovação", title="Conferência de documentos", sub="Processo #1147",
             demo=True, pop=True),
    ]),
    ("Capital de giro", [
        dict(tag="done", label="Concluído", title="Operação liberada", sub="cliente anterior"),
    ]),
]


def _card(c):
    tags = f'<div class="jb__tags"><span class="jb__tag jb__tag--{c["tag"]}">{c["label"]}</span></div>'
    sub = f'<small class="jb__when">{c["sub"]}</small>' if c.get("sub") else ""
    pop = ('<div class="jb__pop" aria-hidden="true">'
           '<span class="jb__pop-ok">✓ Aprovar</span><span class="jb__pop-adj">Pedir ajuste</span></div>') \
          if c.get("pop") else ""
    cls = "jb__card demo" if c.get("demo") else "jb__card"
    return f'<div class="{cls}">{tags}{c["title"]}{sub}{pop}</div>'


def board_html():
    lists = ""
    for i, (title, cards) in enumerate(STAGES, start=1):
        cards_html = "".join(_card(c) for c in cards)
        lists += (f'<div class="jb__list"><p class="jb__lh">'
                  f'<span class="jb__step">Etapa {i}</span>{title}</p>'
                  f'{cards_html}</div>')

    return f"""<div class="jb" id="jb">
  <div class="jb__board" id="jb-board">{lists}</div>
  <button type="button" class="jb__nav jb__nav--prev" id="jb-prev" aria-label="Ver etapa anterior">
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M15 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
  <button type="button" class="jb__nav jb__nav--next" id="jb-next" aria-label="Ver próxima etapa">
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
  <div class="jb__hand" id="jb-hand" aria-hidden="true">
    <i class="jb__ripple" id="jb-ripple"></i>
    <!-- 2 mãos, não 1: pedido do cliente para diferenciar "apontar/clicar" de
         "segurar e arrastar", cada gesto com sua própria mão. São as
         próprias fotos de referência que o cliente mandou (não um desenho
         nosso): recortadas e com o fundo removido (fundo era quadriculado
         de "transparência", sem alpha real, removido via flood-fill a
         partir da borda), exportadas em PNG. Trocadas por CSS
         (.is-grabbing, ver KANBAN_CSS) em vez de desenhadas com JS a cada
         troca de estado. -->
    <!-- Sem loading="lazy" de propósito: a mão só some da tela quando o
         quadro entra no viewport (IntersectionObserver, ver KANBAN_JS) e a
         animação começa em seguida — "carregar só quando precisar" aqui
         seria quase ao mesmo tempo, com o risco real de a imagem ainda não
         estar pronta no primeiro ciclo. width/height evitam reservar
         espaço errado (a caixa já é fixa via CSS, mas mantém a proporção
         intrínseca correta para o navegador). -->
    <picture>
      <source type="image/avif" srcset="assets/img/kanban/mao-apontar.avif">
      <source type="image/webp" srcset="assets/img/kanban/mao-apontar.webp">
      <img class="jb__hand-svg jb__hand-svg--point" src="assets/img/kanban/mao-apontar.png" width="240" height="237" decoding="async" fetchpriority="low" alt="">
    </picture>
    <picture>
      <source type="image/avif" srcset="assets/img/kanban/mao-segurar.avif">
      <source type="image/webp" srcset="assets/img/kanban/mao-segurar.webp">
      <img class="jb__hand-svg jb__hand-svg--grab" src="assets/img/kanban/mao-segurar.png" width="239" height="240" decoding="async" fetchpriority="low" alt="">
    </picture>
  </div>
  <div class="jb__confetti" id="jb-confetti" aria-hidden="true"></div>
</div>
<style>{KANBAN_CSS}</style>
<script>{KANBAN_JS}</script>"""


KANBAN_CSS = """
/* ---------- quadro "como trabalhamos" (ver content/kanban.py) ---------- */
.jb { position: relative; }
/* grid-auto-rows: 1fr é o que garante caixa do mesmo tamanho mesmo com 1
   único cartão dentro: sem isso, align-items:stretch (o padrão do grid) só
   iguala altura entre vizinhos da MESMA linha — e como o board tem 5
   etapas com quantidade ímpar de colunas em larguras intermediárias
   (tablet, ~820-1000px), a última linha sobra com 1 item sozinho, sem
   vizinho pra esticar junto, e a caixa dele fica bem mais baixa que a
   linha de cima (169px contra 307px, medido). grid-auto-rows: 1fr faz
   todas as linhas (não só os itens dentro de cada uma) dividirem a altura
   igualmente, inclusive a que sobra com um item só. */
.jb__board { display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); grid-auto-rows: 1fr; gap: 1rem; }
.jb__list { background: rgba(255,255,255,.03); border: 1px solid var(--rule); border-radius: var(--r-card); padding: 1rem; display: flex; flex-direction: column; gap: .75rem; }
/* Etapa (pequeno, mudo) em cima do título da coluna (maior, --paper),
   quebra de linha própria com pouco espaçamento entre as duas — pedido do
   cliente para virar "ETAPA N" numa linha e o nome da etapa na linha de
   baixo, em vez do número solto ao lado do título. */
.jb__lh { display: flex; flex-direction: column; gap: .125rem; margin: 0 0 .75rem; font: 600 12px/1.3 var(--sans); letter-spacing: .06em; text-transform: uppercase; color: var(--paper); }
.jb__step { font-weight: 500; font-size: 11px; color: var(--slate-2); }
.jb__card { position: relative; background: var(--surface-ink); border-radius: 6px; padding: .75rem 1rem; display: flex; flex-direction: column; gap: .5rem; font: 500 14px/1.35 var(--sans); color: var(--paper); }
.jb__when { font: 400 12px/1 var(--sans); color: var(--slate-2); }
.jb__tags { display: flex; flex-wrap: wrap; gap: .375rem; }
.jb__tag { font: 700 11px/1 var(--sans); letter-spacing: .05em; text-transform: uppercase; padding: .25rem .5rem; border-radius: var(--r-tag); color: #fff; }
.jb__tag--info  { background: var(--cobalt); }
.jb__tag--done  { background: var(--iris); }
.jb__tag--alert { background: var(--danger); }

.jb__pop { position: absolute; left: 0; right: 0; top: calc(100% + .5rem); display: flex; gap: .5rem; padding: .5rem; background: #10161c; border: 1px solid var(--rule); border-radius: 6px; opacity: 0; z-index: 6; box-shadow: 0 18px 36px rgba(0,0,0,.5); pointer-events: none; }
.jb__pop span { flex: 1; text-align: center; font: 600 12px/1 var(--sans); padding: .625rem .375rem; border-radius: 6px; white-space: nowrap; }
.jb__pop-ok { background: var(--iris); color: #fff; }
.jb__pop-adj { background: rgba(255,255,255,.08); color: var(--paper); }

.jb__hand { position: absolute; left: 0; top: 0; width: 40px; height: 40px; z-index: 30; opacity: 0; pointer-events: none; filter: drop-shadow(0 4px 8px rgba(0,0,0,.55)); }
/* As 2 mãos (apontando / segurando, ver o HTML acima) ocupam a mesma caixa,
   uma sobre a outra, e a troca entre elas é só um crossfade de opacidade —
   nunca as duas ao mesmo tempo, e nunca redesenhadas via JS. .is-grabbing
   (ligada pelo KANBAN_JS um instante antes de erguer o cartão, desligada
   depois de soltá-lo) decide qual das duas está visível. */
.jb__hand-svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; object-fit: contain; opacity: 0; transition: opacity .18s ease; }
.jb__hand-svg--point { opacity: 1; }
.jb__hand.is-grabbing .jb__hand-svg--point { opacity: 0; }
.jb__hand.is-grabbing .jb__hand-svg--grab { opacity: 1; }
.jb__ripple { position: absolute; left: 1px; top: -14.5px; width: 32px; height: 32px; border-radius: 50%; border: 2px solid var(--iris-on-dark); opacity: 0; }
.jb__ripple.is-active { animation: jb-ripple .5s ease-out; }
@keyframes jb-ripple { from { transform: scale(.2); opacity: .7; } to { transform: scale(2.6); opacity: 0; } }

.jb__confetti { position: absolute; inset: 0; overflow: visible; pointer-events: none; z-index: 40; }
.jb__confetti i { position: absolute; display: block; top: 0; left: 0; }

/* Seta só existe para o carrossel mobile: em tablet/desktop o grid mostra
   todas as etapas de uma vez, não há "próxima" para ir. Regra base tem que
   vir ANTES do media query que reativa — mesma especificidade, então quem
   fica depois no arquivo vence, e a versão "flex" precisa ser essa. */
.jb__nav { display: none; }

/* CTA logo abaixo do quadro (ver journey() em content/home.py): liga a
   etapa 1 (Primeiro contato) à ação que o leitor precisa tomar agora,
   pedido do cliente para que o quadro não seja só ilustrativo. */
.jb__cta { display: flex; flex-wrap: wrap; align-items: center; gap: 1.5rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--rule-dark-soft); }
.jb__cta-l { margin: 0; font: 600 var(--t-h3)/1.3 var(--sans); color: var(--paper); }

@media (prefers-reduced-motion: reduce) {
  .jb__hand { display: none; }
  .jb__confetti { display: none; }
}

/* Some em QUALQUER largura pequena, mouse incluído — ver a justificativa
   no topo do arquivo (revertida a pedido do cliente: uma versão anterior
   restringia isso a toque de verdade, mas produzia um bug real de
   navegação em celular). */
@media (max-width: 47.99em) {
  .jb__hand, .jb__confetti, .jb__pop { display: none; }
}

/* Carrossel no mobile: ver justificativa no topo do arquivo. */
@media (max-width: 47.99em) {
  .jb__board {
    display: flex;
    /* stretch (o padrão do flex): todas as etapas usam a altura da mais
       alta da fileira, pedido do cliente pra não ter card "baixo" ao lado
       de cards mais cheios. O .jb__pop (balão "Aprovar / Pedir ajuste" do
       cartão de exemplo) já sai do DOM visual via display:none logo
       abaixo, então não entra mais no cálculo de altura "natural" que
       inflava a etapa e cortava o card com uma barra de rolagem vertical
       (defeito antigo, ver seção 24 do README) — overflow-y:hidden segue
       como segunda trava, pra nenhum overflow vertical futuro reabrir
       aquele problema. */
    align-items: stretch;
    overflow-x: auto;
    overflow-y: hidden;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    /* Esmaecimento nas pontas do carrossel: sem isso, a próxima etapa
       espiando na borda da tela aparece cortada de forma abrupta (reto,
       no meio do cartão) em vez de sugerir "tem mais pra rolar". As
       variáveis --jb-fade-l/--jb-fade-r começam em 0 (sem esmaecer nada)
       e o JS (updateFade, mais abaixo) liga cada lado só quando há de
       fato conteúdo pra rolar naquela direção — sem isso, a primeira
       etapa (nada à esquerda ainda) e a última (nada à direita) também
       ficariam com a borda esmaecida sem nenhuma etapa espiando ali,
       cortando texto que está 100% visível à toa. */
    --jb-fade-l: 0px;
    --jb-fade-r: 0px;
    -webkit-mask-image: linear-gradient(to right, transparent, #000 var(--jb-fade-l), #000 calc(100% - var(--jb-fade-r)), transparent);
            mask-image: linear-gradient(to right, transparent, #000 var(--jb-fade-l), #000 calc(100% - var(--jb-fade-r)), transparent);
    /* Ocupa a largura inteira da fileira abaixo, pra sobrar os botões
       de navegação (ver .jb__nav) centralizados numa linha só deles. */
    flex: 0 0 100%;
  }
  .jb__board::-webkit-scrollbar { display: none; }
  .jb__list { flex: 0 0 84%; scroll-snap-align: start; }
  /* Botões de navegação abaixo do quadro, não mais sobrepostos ao
     cartão: sobre o cartão (topo, centro ou perto da base) eles sempre
     acabavam em cima de algum texto em pelo menos uma das 5 etapas,
     porque a quantidade de conteúdo varia de cartão pra cartão — pedido
     do cliente foi justamente parar de atrapalhar a leitura, então a
     única posição que não esbarra em texto nenhum é fora do cartão.
     `.jb` vira uma fileira que quebra em duas linhas nessa largura
     (quadro ocupando a linha inteira, botões centralizados na linha de
     baixo); em tablet/desktop `.jb__nav` segue com display:none (regra
     base) e a estrutura de grid de `.jb__board` não muda. */
  .jb {
    display: flex; flex-wrap: wrap; justify-content: center;
    align-items: center; gap: .75rem;
  }
  .jb__nav {
    display: flex; align-items: center; justify-content: center;
    position: static;
    width: 2.75rem; height: 2.75rem; padding: 0;
    border-radius: 50%; border: 1px solid var(--rule);
    background: rgba(3,11,18,.72); color: var(--paper);
    cursor: pointer;
  }
  .jb__nav:hover, .jb__nav:focus-visible { background: var(--iris); border-color: var(--iris); color: #fff; }
}
"""

# JS: mesma coreografia da peça de referência (mão entra → abre o menu →
# aprova → arrasta até a última coluna → sai → pausa → recomeça), só que sem GSAP —
# CSS transition (via os helpers xform/prop logo abaixo) no lugar de
# gsap.to/fromTo, e um estado {x,y,s,r} guardado no próprio elemento no
# lugar de gsap.getProperty. O restante da lógica (FLIP ao trocar o cartão
# de coluna, cancelar a execução anterior ao reiniciar) é a mesma ideia da
# referência, adaptada. O número ao lado do título de cada coluna é a
# etapa (1 a 5, fixo), não a contagem de cartões — por isso não muda
# durante a demonstração, mesmo quando o cartão troca de coluna.
KANBAN_JS = """
(function(){
  var root = document.getElementById('jb');
  if (!root) return;
  var board     = document.getElementById('jb-board');
  var prevBtn   = document.getElementById('jb-prev');
  var nextBtn   = document.getElementById('jb-next');
  var hand      = document.getElementById('jb-hand');
  var ripple    = document.getElementById('jb-ripple');
  var confettiEl = document.getElementById('jb-confetti');
  var ORIGINAL = board.innerHTML;
  var HX = .253, HY = .005;          // ponta do dedo indicador, fração do ícone (foto da mão apontando, com object-fit: contain)
  var EASE = 'cubic-bezier(.25,.8,.3,1)';
  var run = 0;
  var timers = [];

  function alive(id){ return id === run; }
  function sleep(ms){ return new Promise(function(r){ timers.push(setTimeout(r, ms)); }); }

  function setXform(el, x, y, s, r){
    el._x = x===undefined ? (el._x||0) : x;
    el._y = y===undefined ? (el._y||0) : y;
    el._s = s===undefined ? (el._s===undefined?1:el._s) : s;
    el._r = r===undefined ? (el._r===undefined?0:el._r) : r;
    el.style.transform = 'translate(' + el._x + 'px,' + el._y + 'px) scale(' + el._s + ') rotate(' + el._r + 'deg)';
  }
  // Anima transform (e opcionalmente box-shadow) até o novo estado; resolve
  // por tempo (setTimeout), não por transitionend — mais previsível com
  // várias propriedades mudando junto (evita disparo duplicado/perdido).
  function xform(el, x, y, s, r, dur, boxShadow){
    return new Promise(function(resolve){
      var props = 'transform ' + dur + 's ' + EASE + (boxShadow !== undefined ? ', box-shadow ' + dur + 's ' + EASE : '');
      el.style.transition = props;
      void el.offsetWidth;
      setXform(el, x, y, s, r);
      if (boxShadow !== undefined) el.style.boxShadow = boxShadow;
      timers.push(setTimeout(function(){ el.style.transition = ''; resolve(); }, dur*1000 + 20));
    });
  }
  function fade(el, opacity, dur){
    return new Promise(function(resolve){
      el.style.transition = 'opacity ' + dur + 's ' + EASE;
      void el.offsetWidth;
      el.style.opacity = opacity;
      timers.push(setTimeout(function(){ el.style.transition = ''; resolve(); }, dur*1000 + 20));
    });
  }
  function popShow(pop, show){
    return new Promise(function(resolve){
      pop.style.transition = 'opacity .3s ' + EASE + ', transform .3s ' + EASE;
      void pop.offsetWidth;
      pop.style.opacity = show ? 1 : 0;
      pop.style.transform = show ? 'translateY(0)' : 'translateY(-8px)';
      timers.push(setTimeout(resolve, show ? 320 : 20));
    });
  }
  // Verdadeiro quando o board é carrossel (largura pequena — ver
  // justificativa no topo do arquivo): start() usa isto para decidir se
  // anima a mão, sem distinguir toque de mouse — qualquer largura pequena
  // fica sem mão, popover e confete.
  function isCarousel(){ return board.scrollWidth > board.clientWidth + 1; }
  function rel(el, fx, fy){
    var r = el.getBoundingClientRect(), s = root.getBoundingClientRect();
    return { x: r.left - s.left + r.width*fx + root.scrollLeft, y: r.top - s.top + r.height*fy };
  }
  function handTo(el, fx, fy, dur){
    var p = rel(el, fx, fy);
    return xform(hand, p.x - HX*40, p.y - HY*40, hand._s, 0, dur || .9);
  }
  function click(){
    ripple.classList.remove('is-active'); void ripple.offsetWidth; ripple.classList.add('is-active');
    return xform(hand, hand._x, hand._y, .84, 0, .1).then(function(){
      return xform(hand, hand._x, hand._y, 1, 0, .22);
    });
  }
  function flipMove(card, list, ref){
    var cards = [].slice.call(board.querySelectorAll('.jb__card')), before = new Map();
    cards.forEach(function(c){ before.set(c, c.getBoundingClientRect()); });
    list.insertBefore(card, ref !== undefined ? ref : (list.children[1] || null));
    cards.forEach(function(c){
      if (c === card) return;
      var b = before.get(c), a = c.getBoundingClientRect(), dx = b.left - a.left, dy = b.top - a.top;
      if (Math.abs(dx) + Math.abs(dy) > .5){ setXform(c, dx, dy, 1, 0); xform(c, 0, 0, 1, 0, .55); }
    });
    var b0 = before.get(card), a0 = card.getBoundingClientRect();
    return { dx: b0.left - a0.left, dy: b0.top - a0.top };
  }
  function lift(card){ card.style.zIndex = 10; return xform(card, card._x||0, card._y||0, 1.05, 2.5, .25, '0 22px 40px rgba(0,0,0,.55)'); }
  function drop(card){ return xform(card, 0, 0, 1, 0, .3, '0 0 0 rgba(0,0,0,0)').then(function(){ card.style.zIndex = ''; }); }
  function carry(card, list, dur){
    var m = flipMove(card, list);
    setXform(card, m.dx, m.dy, card._s, card._r);
    xform(hand, hand._x - m.dx, hand._y - m.dy, hand._s, 0, dur);
    return xform(card, 0, 0, card._s, card._r, dur);
  }
  function flash(el, color){
    el.style.transition = 'none'; el.style.color = color; void el.offsetWidth;
    el.style.transition = 'color 1.4s ' + EASE; el.style.color = '';
  }
  // Confetes ao chegar em "Capital de giro": uma explosão de verdade —
  // cada partícula sai do centro do cartão numa direção própria (360°),
  // freia (arrasto do ar) enquanto uma gravidade bem leve puxa tudo pra
  // baixo aos poucos, com um balanço lateral (seno) simulando papel
  // flutuando. É física simples por requestAnimationFrame — em vez de
  // uma única @keyframes com um --dx fixo, cada quadro recalcula posição
  // e opacidade, o que é o que dá a sensação de fluidez/espalhamento
  // (uma transição CSS de A a B não consegue curvar o percurso assim).
  var CONFETTI_COLORS = ['var(--iris)', 'var(--cobalt)', 'var(--danger)', 'var(--iris-on-dark)'];
  var GRAVITY = 210;   // px/s² — bem abaixo da gravidade real: cai devagar, "leve"
  var DRAG    = 1.7;   // 1/s — quão rápido o impulso da explosão se dissipa
  function confettiBurst(target, runId){
    var r = target.getBoundingClientRect(), s = root.getBoundingClientRect();
    var ox = r.left - s.left + r.width / 2, oy = r.top - s.top + r.height * .25;
    var N = 26, parts = [];
    for (var i = 0; i < N; i++){
      var el = document.createElement('i');
      var w = 3 + Math.random() * 3, h = 7 + Math.random() * 5;
      el.style.width = w + 'px';
      el.style.height = h + 'px';
      el.style.background = CONFETTI_COLORS[i % CONFETTI_COLORS.length];
      el.style.borderRadius = (i % 3 === 0) ? '50%' : '1px';
      el.style.opacity = 0;
      confettiEl.appendChild(el);

      var ang = Math.random() * Math.PI * 2;              // direção da explosão, em todas as direções
      var speed = 70 + Math.random() * 150;                // impulso inicial (px/s)
      parts.push({
        el: el, ox: ox, oy: oy, x: 0, y: 0,
        vx: Math.cos(ang) * speed,
        vy: Math.sin(ang) * speed * .7 - 60,               // viés levemente pra cima no instante do encaixe
        rot: Math.random() * 360,
        vr: (Math.random() - .5) * 150,
        swayPhase: Math.random() * Math.PI * 2,
        swaySpeed: 1.1 + Math.random() * 1.3,
        swayAmp: 14 + Math.random() * 18,
        born: null,
        life: 1.7 + Math.random() * .8
      });
    }

    var last = null;
    function frame(now){
      if (last === null) { last = now; parts.forEach(function(pt){ pt.born = now; }); }
      var dt = Math.min((now - last) / 1000, .05);
      last = now;
      parts = parts.filter(function(pt){
        var age = (now - pt.born) / 1000;
        if (age > pt.life || pt.y > 200){ pt.el.remove(); return false; }
        pt.vx *= Math.exp(-DRAG * dt);
        pt.vy += GRAVITY * dt;
        var sway = Math.sin(age * pt.swaySpeed + pt.swayPhase) * pt.swayAmp;
        pt.x += pt.vx * dt;
        pt.y += pt.vy * dt;
        pt.rot += pt.vr * dt;
        var f = age / pt.life;
        var op = f < .12 ? f / .12 : (f < .55 ? 1 : Math.max(0, 1 - (f - .55) / .45));
        pt.el.style.transform = 'translate(' + (pt.ox + pt.x + sway) + 'px,' + (pt.oy + pt.y) + 'px) rotate(' + pt.rot + 'deg)';
        pt.el.style.opacity = op;
        return true;
      });
      if (parts.length && alive(runId)){
        requestAnimationFrame(frame);
      } else {
        parts.forEach(function(pt){ pt.el.remove(); });
      }
    }
    requestAnimationFrame(frame);
  }

  async function demo(id){
    // Só o resto (setup) roda uma vez por chamada de demo() — o quadro
    // inteiro nunca é recriado a cada volta do loop. O único elemento que
    // "reinicia" é o próprio cartão de demonstração: ele some em Capital
    // de giro e reaparece já de volta em Documentação (ver o fim do
    // laço), e a mãozinha simplesmente entra de novo pra arrastá-lo.
    // Todo o resto do quadro fica parado o tempo todo.
    var lists   = board.querySelectorAll('.jb__list');
    var docList = lists[3], giroList = lists[4];
    var card    = board.querySelector('.demo');
    var CARD_HTML = card.innerHTML;   // estado original do cartão, pra restaurar a cada volta

    await sleep(800);
    while (alive(id)){
      var pop  = card.querySelector('.jb__pop');
      var ok   = pop.querySelector('.jb__pop-ok');
      var when = card.querySelector('.jb__when');

      var s = root.getBoundingClientRect();

      setXform(hand, s.width*.66 + root.scrollLeft, s.height + 24, 1, 0);
      hand.style.opacity = 0;
      await fade(hand, 1, .25);                                          if (!alive(id)) return;
      await handTo(card, .6, .55, 1.05);                                  if (!alive(id)) return;

      await popShow(pop, true);
      await sleep(250);
      await handTo(ok, .5, .55, .5);                                      if (!alive(id)) return;
      await click();
      await sleep(200);

      var oldTag = card.querySelector('.jb__tag');
      popShow(pop, false);
      await fade(oldTag, 0, .2);
      oldTag.outerHTML = '<span class="jb__tag jb__tag--done">Aprovado</span>';
      when.textContent = 'documentação completa';
      flash(when, 'var(--iris-on-dark)');
      await sleep(900);                                                   if (!alive(id)) return;

      await handTo(card, .5, .5, .45);                                    if (!alive(id)) return;
      // Troca para a mão aberta (segurar/arrastar) só agora, bem no
      // instante em que ela chega no cartão pra pegá-lo — antes disso
      // (aproximando, apontando, clicando em Aprovar) a mão continua a de
      // apontar/clicar. Some de novo depois de soltar o cartão em "Capital
      // de giro" (ver o remove() logo abaixo), então a próxima interação
      // (o clique seguinte, se houvesse) já volta de mão fechada em ponto.
      hand.classList.add('is-grabbing');
      await lift(card);
      await carry(card, giroList, 1.1);                                   if (!alive(id)) return;
      await drop(card);
      hand.classList.remove('is-grabbing');
      when.textContent = 'operação liberada ✓';
      flash(when, 'var(--iris-on-dark)');
      confettiBurst(card, id);
      await sleep(900);                                                   if (!alive(id)) return;

      await xform(hand, hand._x + 100, hand._y + 60, hand._s, 0, .7);
      await fade(hand, 0, .35);
      await sleep(700);                                                   if (!alive(id)) return;

      // devolve só o cartão pro início — o resto do quadro nem pisca:
      // ele some em Capital de giro, é restaurado e recolocado em
      // Documentação (com um FLIP nos vizinhos que reacomodam, igual
      // já acontece na ida) enquanto está invisível, e reaparece lá.
      await fade(card, 0, .4);                                            if (!alive(id)) return;
      card.style.transition = ''; card.style.boxShadow = ''; card.style.zIndex = '';
      card._x = card._y = card._r = 0; card._s = 1;
      setXform(card, 0, 0, 1, 0);
      card.innerHTML = CARD_HTML;
      flipMove(card, docList, null);              // volta pro fim da lista — depois do card "Recebido", como no início
      await sleep(150);                                                   if (!alive(id)) return;
      await fade(card, 1, .45);                                           if (!alive(id)) return;
      await sleep(600);                                                   if (!alive(id)) return;
    }
  }

  // Liga o esmaecimento de cada ponta do carrossel só quando existe
  // mesmo etapa pra revelar rolando naquela direção — no início (nada à
  // esquerda) ou no fim (nada à direita) do trilho, aquele lado fica sem
  // esmaecer, senão a etapa 1 e a última apareceriam com a própria borda
  // cortada mesmo estando 100% visíveis, sem nada espiando ali.
  function updateFade(){
    var max = board.scrollWidth - board.clientWidth;
    var atStart = board.scrollLeft <= 1;
    var atEnd = max <= 1 || board.scrollLeft >= max - 1;
    board.style.setProperty('--jb-fade-l', atStart ? '0px' : '28px');
    board.style.setProperty('--jb-fade-r', atEnd ? '0px' : '28px');
  }
  var fadeTicking = false;
  board.addEventListener('scroll', function(){
    if (fadeTicking) return;
    fadeTicking = true;
    requestAnimationFrame(function(){ updateFade(); fadeTicking = false; });
  }, { passive: true });

  function start(){
    run++;
    timers.forEach(clearTimeout); timers = [];
    board.style.cssText = ''; board.innerHTML = ORIGINAL;
    hand.style.cssText = ''; hand._x = hand._y = hand._r = 0; hand._s = 1;
    hand.classList.remove('is-grabbing');
    ripple.classList.remove('is-active');
    confettiEl.innerHTML = '';
    updateFade();
    // A mão não roda com "menos movimento" pedido no sistema (regra padrão
    // de acessibilidade) nem em largura pequena/carrossel (ver isCarousel()
    // acima e a docstring do arquivo) — qualquer largura pequena, de mouse
    // ou toque, fica sem a demonstração.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (isCarousel()) return;
    demo(run);
  }

  // Setas do carrossel mobile: avançam/voltam uma etapa por clique e dão a
  // volta (loop) nas pontas, em vez de ficar "presas" no início/fim.
  // #jb-prev/#jb-next ficam fora de #jb-board, então o reset de start()
  // (que só reescreve o board) nunca precisa recriar esses listeners.
  //
  // Não usa "posição atual +/- 1 passo fixo": a última etapa começa numa
  // posição (offsetLeft) que o navegador não consegue rolar até o fim —
  // sobra menos conteúdo depois dela do que a largura da tela — então o
  // ponto de encaixe real dela é sempre menor que offsetLeft. Um passo
  // fixo ultrapassava esse teto antes de chegar lá, e a seta nunca
  // mostrava a última etapa (ia direto de Documentação pro início). Em
  // vez disso, calcula o ponto de encaixe de CADA etapa (offsetLeft
  // limitado ao que dá pra rolar), acha qual é o mais perto da posição
  // atual e vai para o vizinho (anterior ou próximo) da lista — funciona
  // mesmo se a pessoa tiver arrastado o carrossel manualmente entre um
  // clique e outro.
  function stepTo(delta) {
    var lists = [].slice.call(board.querySelectorAll('.jb__list'));
    if (!lists.length) return;
    var reducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var max = board.scrollWidth - board.clientWidth;
    var stops = lists.map(function (l) { return Math.min(l.offsetLeft, max); });
    var current = board.scrollLeft, idx = 0, bestDiff = Infinity;
    stops.forEach(function (s, i) {
      var diff = Math.abs(s - current);
      if (diff < bestDiff) { bestDiff = diff; idx = i; }
    });
    var nextIdx = (idx + delta + stops.length) % stops.length;
    board.scrollTo({ left: stops[nextIdx], behavior: reducedMotion ? 'auto' : 'smooth' });
  }
  if (prevBtn) prevBtn.addEventListener('click', function () { stepTo(-1); });
  if (nextBtn) nextBtn.addEventListener('click', function () { stepTo(1); });

  window.addEventListener('resize', function(){ clearTimeout(start._t); start._t = setTimeout(start, 250); });
  if ('IntersectionObserver' in window){
    var started = false;
    new IntersectionObserver(function(entries){
      if (entries[0].isIntersecting && !started){ started = true; start(); }
    }, { threshold: .2 }).observe(root);
  } else {
    start();
  }
})();
"""
