/* =========================================================================
   Acrópole Capital — comportamento de interface
   Sem dependências. Nenhuma credencial, chave ou endpoint sensível aqui:
   o envio de formulários usa window.ACROPOLE_CONFIG.endpoint, definido em
   assets/js/config.js e apontando sempre para uma função de servidor.
   ========================================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isCoarsePointer = window.matchMedia('(pointer: coarse)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* Trava de rolagem do body: gaveta e popup podem, em tese, se sobrepor,
     então cada um registra a própria trava em vez de ligar/desligar a
     classe direto — só destrava quando nenhuma das duas está mais aberta. */
  var bodyLocks = {};
  var setBodyLock = function (key, state) {
    bodyLocks[key] = state;
    var any = Object.keys(bodyLocks).some(function (k) { return bodyLocks[k]; });
    document.body.classList.toggle('is-locked', any);
  };

  /* Ligações globais (cabeçalho, gaveta, trilho de contato) rodam uma vez.
     Ligações de página rodam de novo sempre que o conteúdo do <main> muda,
     o que permite reaproveitar este mesmo arquivo em um roteador. */
  function bindGlobal() {
  /* ---------------------------------------------------------------- ano */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* -------------------------------------------- rolagem suave (trackpad) */
  /* Pedido do cliente: a rolagem por trackpad/roda do mouse "passava rápido
     demais" — difícil de controlar. Em vez de aplicar a rolagem bruta do
     evento `wheel` direto na página, acumulamos um alvo e animamos a
     posição real a cada quadro com uma fração fixa da distância restante
     (interpolação): isso segura a velocidade — a página não pula direto
     pro alvo — mas continua fluida, porque o alvo só se atualiza a cada
     novo movimento, nunca trava a animação em andamento (mesma sensação de
     "inércia" de um trackpad de qualidade).
     Importante: isso só entra em ação pro gesto de trackpad/roda do mouse
     (evento `wheel`). Arrastar a barra de rolagem, teclado (setas, Page
     Down, Home/End) e rolagem por toque continuam 100% nativos, na
     velocidade normal — são duas formas de navegar diferentes, e uma não
     pode travar a outra (ver a checagem de "rolagem que não veio da nossa
     animação", logo abaixo, que existe exatamente pra garantir isso).
     Também não se aplica a: quem pediu rolagem sem animação
     (`prefers-reduced-motion`), zoom por Ctrl+scroll, rolagem
     majoritariamente horizontal, nem rolagem dentro de qualquer painel com
     scroll próprio de verdade (gaveta mobile, menu do select, modal de
     contato, tabela larga de artigo — a esteira de depoimentos NÃO entra
     aqui: no desktop ela não tem scroll próprio nenhum, é só uma animação
     de CSS, então tratá-la como "painel com scroll próprio" só fazia a
     rolagem da página alternar entre suave e nativa toda hora que o cursor
     passava por cima dela mesmo durante um gesto contínuo — o segundo bug
     relatado). */
  if (!reduced) {
    var SMOOTH_SKIP = '.drawer__panel, .cs-menu, .leadmodal__dialog, .prose .tablewrap, textarea';
    var scrollTarget = window.scrollY;
    var scrollRaf = null;
    /* Guarda o valor exato que a nossa própria animação acabou de mandar
       pro navegador. O listener de `scroll`, mais abaixo, compara a
       posição real com esse valor pra saber se foi a nossa animação que
       moveu a página ou algo externo (barra de rolagem, teclado, toque) —
       mais confiável que uma flag de "aconteceu por último", que pode
       perder a sincronia quando o navegador agrupa vários eventos de
       `scroll` num só. */
    var lastSetY = window.scrollY;
    var maxScroll = function () {
      return document.documentElement.scrollHeight - window.innerHeight;
    };
    var setScroll = function (y) {
      lastSetY = y;
      /* `behavior: 'instant'` é essencial aqui: sem ele, o `scroll-behavior:
         smooth` do <html> (ver CSS, ---------- 1. Variáveis ----------)
         reanima cada chamada por conta própria, e as duas animações — a
         nossa e a nativa do navegador — competem, deixando a rolagem bem
         mais lenta e travada do que o pedido. */
      window.scrollTo({ top: y, left: 0, behavior: 'instant' });
    };
    var stepScroll = function () {
      var current = window.scrollY;
      var diff = scrollTarget - current;
      if (Math.abs(diff) < 0.5) { setScroll(scrollTarget); scrollRaf = null; return; }
      setScroll(current + diff * 0.18);
      scrollRaf = requestAnimationFrame(stepScroll);
    };
    window.addEventListener('wheel', function (e) {
      if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      if (e.target.closest && e.target.closest(SMOOTH_SKIP)) return;
      e.preventDefault();
      scrollTarget = Math.max(0, Math.min(maxScroll(), scrollTarget + e.deltaY * 0.7));
      if (!scrollRaf) scrollRaf = requestAnimationFrame(stepScroll);
    }, { passive: false });
    /* Bug relatado pelo cliente: arrastar a barra de rolagem "brigava" com
       a nossa animação e travava a página, puxando de volta pro ponto de
       onde ele tinha saído. Causa: nossa animação seguia perseguindo um
       alvo antigo por cima do que a barra de rolagem estava tentando
       fazer. Correção: todo evento de `scroll` cuja posição não bate com o
       que a nossa própria animação acabou de mandar (`lastSetY`) é
       rolagem externa — barra de rolagem, teclado, toque — e assume o
       controle na hora: cancela qualquer animação nossa em andamento e
       realinha o alvo pra posição atual, sem disputa nenhuma. */
    window.addEventListener('scroll', function () {
      if (Math.abs(window.scrollY - lastSetY) < 1) return;
      if (scrollRaf) { cancelAnimationFrame(scrollRaf); scrollRaf = null; }
      scrollTarget = window.scrollY;
      lastSetY = window.scrollY;
    }, { passive: true });
  }

  /* ------------------------------------------------- contato no scroll */
  /* O cabeçalho é fixo (ver ---------- 7. Cabeçalho / navegação ---------- no
     CSS) e mantém sempre a mesma cor, a do topo da página (pedido do
     cliente) — não muda de aparência ao rolar. O botão flutuante de
     contato aparece depois de rolar mais, num limiar próprio. */
  var onScroll = function () {
    var rail = $('.rail');
    if (rail) rail.setAttribute('data-show', window.scrollY > 620 ? 'true' : 'false');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* --------------------------------------------------- aviso de cookies */
  /* Mostra uma vez, na primeira visita, e some para sempre depois que a
     pessoa clicar em "Aceitar" — a escolha fica em localStorage. Tentativa
     de leitura/escrita embrulhada em try/catch: em navegação privada
     alguns navegadores bloqueiam localStorage e lançam erro só de acessar
     a propriedade — sem isso, o aviso quebraria o carregamento da página
     inteira para quem estiver nesse modo. Se não der pra lembrar a
     escolha, a barra some ao clicar mesmo assim (só volta a aparecer na
     próxima visita, o que é um mau-menor aceitável). */
  var cookiebar = $('#cookiebar');
  if (cookiebar) {
    var COOKIE_KEY = 'cookieconsent:v1';
    var alreadyAccepted = false;
    try { alreadyAccepted = localStorage.getItem(COOKIE_KEY) === 'accepted'; } catch (e) {}

    /* Empurra o botão flutuante de contato pra cima da caixinha enquanto
       ela está visível — os dois vivem no mesmo canto (inferior direito)
       e, sem isso, um tampa o outro. A altura da caixinha varia com o
       tamanho da tela (o texto quebra em mais ou menos linhas), então é
       medida de verdade em vez de um valor fixo, com uma folga extra de
       12px pra não ficarem colados — e reagimos ao redimensionamento da
       janela enquanto a caixinha estiver na tela. */
    var updateCookiebarOffset = function () {
      var h = cookiebar.getAttribute('data-show') === 'true' ? cookiebar.offsetHeight + 12 : 0;
      document.documentElement.style.setProperty('--cookiebar-h', h + 'px');
    };

    if (!alreadyAccepted) {
      cookiebar.setAttribute('data-show', 'true');
      updateCookiebarOffset();
      window.addEventListener('resize', updateCookiebarOffset);
    }
    $('[data-cookie-accept]', cookiebar).addEventListener('click', function () {
      try { localStorage.setItem(COOKIE_KEY, 'accepted'); } catch (e) {}
      cookiebar.setAttribute('data-show', 'false');
      updateCookiebarOffset();
      window.removeEventListener('resize', updateCookiebarOffset);
    });
  }

  /* ------------------------------------------------- painel de soluções */
  // Os listeners de document (Escape e clique fora) eram registrados uma
  // vez POR item de mega-menu dentro do forEach: com N itens, N listeners
  // de keydown e N de click ficavam pendurados em document pro resto da
  // vida da página, cada um recomparando о mesmo evento contra o seu
  // próprio item. Nenhum bug (cada handler checa só o item dele antes de
  // agir), só trabalho repetido a cada tecla/clique na página inteira.
  // Registrando uma vez só e iterando a lista de itens abertos no momento
  // do evento, o custo por evento fica O(itens abertos) em vez de O(itens
  // registrados) crescendo com listeners cada um plugado direto em document.
  var megaItems = [];
  $$('.nav__item[data-mega]').forEach(function (item) {
    var trigger = $('.nav__link', item);
    var panel = $('.megapanel', item);
    if (!trigger || !panel) return;
    var timer;

    var open = function (state) {
      item.classList.toggle('is-open', state);
      trigger.setAttribute('aria-expanded', state ? 'true' : 'false');
    };

    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      open(!item.classList.contains('is-open'));
    });
    item.addEventListener('mouseenter', function () { clearTimeout(timer); open(true); });
    item.addEventListener('mouseleave', function () { timer = setTimeout(function () { open(false); }, 160); });
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) open(false);
    });
    megaItems.push({ item: item, trigger: trigger, open: open });
  });
  if (megaItems.length) {
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      megaItems.forEach(function (m) {
        if (m.item.classList.contains('is-open')) { m.open(false); m.trigger.focus(); }
      });
    });
    document.addEventListener('click', function (e) {
      megaItems.forEach(function (m) {
        if (!m.item.contains(e.target)) m.open(false);
      });
    });
  }

  /* --------------------------------------------------- gaveta (mobile) */
  var burger = $('.burger');
  var drawer = $('.drawer');
  if (burger && drawer) {
    var lastFocus = null;
    var setDrawer = function (state) {
      // inert acompanha aria-hidden: sem ele, os links da gaveta fechada
      // continuam alcançáveis por Tab mesmo fora da tela (o CSS só desliza
      // com transform, não tira do fluxo), o que quebra o foco do teclado
      // e conflita com aria-hidden="true" para leitores de tela.
      if (state) drawer.removeAttribute('inert');
      drawer.setAttribute('data-open', state ? 'true' : 'false');
      drawer.setAttribute('aria-hidden', state ? 'false' : 'true');
      burger.setAttribute('aria-expanded', state ? 'true' : 'false');
      setBodyLock('drawer', state);
      if (state) {
        lastFocus = document.activeElement;
        var first = $('a, button', drawer);
        if (first) first.focus();
      } else {
        drawer.setAttribute('inert', '');
        if (lastFocus) lastFocus.focus();
      }
    };
    burger.addEventListener('click', function () {
      setDrawer(drawer.getAttribute('data-open') !== 'true');
    });
    $$('[data-drawer-close]', drawer).forEach(function (el) {
      el.addEventListener('click', function () { setDrawer(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.getAttribute('data-open') === 'true') setDrawer(false);
    });
    // Sub-níveis
    $$('[data-drawer-toggle]', drawer).forEach(function (btn) {
      var sub = document.getElementById(btn.getAttribute('aria-controls'));
      btn.addEventListener('click', function () {
        var open = sub.getAttribute('data-open') === 'true';
        sub.setAttribute('data-open', open ? 'false' : 'true');
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      });
    });
    // Confinamento simples de foco
    drawer.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || drawer.getAttribute('data-open') !== 'true') return;
      var f = $$('a[href], button:not([disabled])', drawer).filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ------------------------------------------ popup de captação rápida */
  /* Intercepta cliques em qualquer CTA marcado com [data-lead-modal] —
     "Solicitar uma análise", os links de WhatsApp do cabeçalho, gaveta,
     rodapé e trilho flutuante — e abre o popup no lugar da navegação.
     Delegado no document (não em cada botão) porque parte desses CTAs
     vive dentro do <main>, que é reconstruído a cada troca de rota no
     pacote navegável; delegação continua funcionando sem precisar
     religar nada em bindPage(). */
  var leadModal = $('#lead-modal');
  if (leadModal) {
    var leadDialog = $('.leadmodal__dialog', leadModal);
    var leadForm = $('form', leadModal);
    var leadLastFocus = null;

    /* Trava de zoom do popup em toque: pedido explícito da cliente —
       enquanto o popup está aberto no celular/tablet, nenhum toque (foco
       em campo, duplo toque, pinça) pode dar zoom nem deixar a tela
       arrastável para os lados; tem que ficar fixa. A forma confiável de
       garantir isso é reescrever a própria tag <meta name="viewport">
       enquanto o popup está aberto, e devolver o valor original ao
       fechar — assim o resto do site continua com zoom normal (pinça
       livre é acessibilidade), só o popup fica travado. No desktop essa
       tag não tem efeito nenhum, então nem mexemos nela. */
    var viewportMeta = document.querySelector('meta[name="viewport"]');
    var viewportDefault = viewportMeta ? viewportMeta.getAttribute('content') : null;
    var lockZoom = function (state) {
      if (!viewportMeta || !isCoarsePointer) return;
      viewportMeta.setAttribute('content', state
        ? 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover'
        : viewportDefault);
    };

    var setLeadModal = function (state) {
      lockZoom(state);
      leadModal.setAttribute('data-open', state ? 'true' : 'false');
      leadModal.setAttribute('aria-hidden', state ? 'false' : 'true');
      setBodyLock('leadModal', state);
      if (state) {
        leadLastFocus = document.activeElement;
        if (leadForm) {
          var ok = $('.formstate--ok', leadForm), err = $('.formstate--err', leadForm);
          ok && ok.setAttribute('data-show', 'false');
          err && err.setAttribute('data-show', 'false');
        }
        /* Sem foco automático em toque (celular/tablet): no iOS, chamar
           .focus() num campo enquanto o popup ainda está com transform em
           transição (entrada de .3s, ver .leadmodal__dialog) faz o Safari
           calcular errado o zoom ao abrir o teclado. Com a trava de zoom
           acima isso já não seria mais possível de qualquer forma, mas
           continuamos sem focar sozinho em toque: a pessoa que toque no
           campo que quiser, na hora que quiser. No desktop, com teclado
           físico, o foco automático continua (ajuda quem navega só pelo
           teclado, e lá não existe esse risco de zoom). */
        if (!isCoarsePointer) {
          var firstField = $('input, select', leadModal);
          if (firstField) firstField.focus();
        }
      } else if (leadLastFocus) {
        leadLastFocus.focus();
      }
    };

    document.addEventListener('click', function (e) {
      var opener = e.target.closest && e.target.closest('[data-lead-modal]');
      if (opener) { e.preventDefault(); setLeadModal(true); return; }
      var closer = e.target.closest && e.target.closest('[data-lead-close]');
      if (closer) { e.preventDefault(); setLeadModal(false); }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && leadModal.getAttribute('data-open') === 'true') setLeadModal(false);
    });

    // Confinamento simples de foco, igual à gaveta
    leadModal.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || leadModal.getAttribute('data-open') !== 'true') return;
      var f = $$('a[href], button:not([disabled]), input, select, textarea', leadDialog || leadModal)
        .filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ---------------------------------------- fechar select customizado */
  var closeAllSelects = function () {
    $$('.cs-menu:not([hidden])').forEach(function (m) { m.hidden = true; });
    $$('.cs-trigger.is-open').forEach(function (t) {
      t.classList.remove('is-open'); t.setAttribute('aria-expanded', 'false');
      t.removeAttribute('aria-activedescendant');
    });
  };
  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('.cs')) closeAllSelects();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllSelects();
  });

  } /* fim bindGlobal */

  function bindPage(scope) {
    scope = scope || document;
    var $ = function (s, c) { return (c || scope).querySelector(s); };
    var $$ = function (s, c) { return Array.prototype.slice.call((c || scope).querySelectorAll(s)); };

  /* ------------------------------------------- revelação ao rolar -----
     Marca cada [data-reveal] ainda não observado e usa um único
     IntersectionObserver por chamada para revelar (fade + leve subida,
     ver CSS) assim que o bloco cruza o viewport — para de observar no
     mesmo instante, então nenhum bloco continua custando nada depois da
     primeira vez que aparece. document.documentElement só carrega a
     classe .js-reveal quando o script síncrono no <head> já confirmou
     suporte a IntersectionObserver e que a pessoa não pediu menos
     movimento (ver site.css, seção 21); sem ela, os blocos já nascem
     visíveis e este bloco não faz nada. */
  if (document.documentElement.classList.contains('js-reveal')) {
    var toReveal = $$('[data-reveal]:not(.is-revealed)').filter(function (el) {
      return !el.dataset.revealBound;
    });
    if (toReveal.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-revealed');
          io.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.01 });
      toReveal.forEach(function (el) {
        el.dataset.revealBound = '1';
        io.observe(el);
        /* Rede de segurança: se por qualquer motivo o observer nunca disparar
           para este elemento (âncora que pula direto pro meio da página,
           bfcache restaurando scroll, layout instável no momento do
           observe()), o bloco não pode ficar invisível para sempre — texto e
           números não são decoração, são conteúdo. 2.5s é folga suficiente
           para qualquer entrada por scroll legítima já ter revelado antes
           disso; se chegou aqui é porque o observer não serviu. */
        setTimeout(function () {
          if (!el.classList.contains('is-revealed')) {
            el.classList.add('is-revealed');
            io.unobserve(el);
          }
        }, 2500);
      });
    }
  }

  /* ------------------------------ anima só o que está na tela --------
     Algumas animações são infinitas por natureza: as ~100 estrelinhas do
     hero, a esteira de bancos parceiros e os detalhes dos diagramas de
     solução (setas subindo/descendo, tracejado correndo). Sem nada que as
     controle, todas continuam rodando mesmo quando ficaram milhares de
     pixels acima — o navegador segue compondo quadro a quadro de coisas
     que ninguém está vendo, e esse orçamento sai justamente de onde faz
     falta: a rolagem.

     Um único observador marca o container como .is-anim-idle quando ele
     sai da tela (o CSS então pausa as animações dele e dos filhos) e tira
     a marca quando volta. A margem de 200px faz a retomada acontecer
     ANTES de entrar no campo de visão, então nada aparece congelado.
     Diferente do bloco de revelação acima, aqui não se pode dar
     unobserve: o estado precisa alternar a cada ida e volta. */
  if ('IntersectionObserver' in window) {
    var idleTargets = $$('.hero-stars, .partners__track, .diagram').filter(function (el) {
      return !el.dataset.animIdleBound;
    });
    if (idleTargets.length) {
      var idleIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          entry.target.classList.toggle('is-anim-idle', !entry.isIntersecting);
        });
      }, { rootMargin: '200px 0px' });
      idleTargets.forEach(function (el) {
        el.dataset.animIdleBound = '1';
        idleIO.observe(el);
      });
    }
  }

  /* ------------------------------------------------------- acordeões
     dataset.accBound evita ligar o mesmo botão 2 vezes quando bindPage()
     roda mais de uma vez sobre o mesmo conteúdo — no arquivo único
     navegável, o roteador já religa a rota inicial (render() chama
     bindPage(main)) antes do boot() do próprio site.js rodar de novo com
     bindPage(document) no DOMContentLoaded. Sem essa guarda, um único
     clique disparava os 2 listeners em sequência (abre, fecha) e a
     pergunta parecia "sem resposta" — só na primeira rota carregada. */
  $$('.acc__btn').forEach(function (btn) {
    if (btn.dataset.accBound) return;
    btn.dataset.accBound = '1';
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      panel.setAttribute('data-open', open ? 'false' : 'true');
    });
  });

  /* ------------------------------------------- índice de soluções */
  var solList = $('.solindex__list');
  if (solList && !solList.dataset.solindexBound) {
    solList.dataset.solindexBound = '1';
    var rows = $$('.solrow', solList);
    var select = function (key) {
      rows.forEach(function (r) { r.setAttribute('aria-selected', r.dataset.sol === key ? 'true' : 'false'); });
      $$('.solpanel').forEach(function (p) { p.setAttribute('data-active', p.dataset.sol === key ? 'true' : 'false'); });
    };
    rows.forEach(function (r) {
      r.addEventListener('click', function () { select(r.dataset.sol); });
      r.addEventListener('mouseenter', function () { if (window.matchMedia('(min-width: 940px)').matches) select(r.dataset.sol); });
      r.addEventListener('focus', function () { select(r.dataset.sol); });
    });
    solList.addEventListener('keydown', function (e) {
      var i = rows.indexOf(document.activeElement);
      if (i < 0) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); rows[(i + 1) % rows.length].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); rows[(i - 1 + rows.length) % rows.length].focus(); }
    });
  }

  /* ------------------------------------------- select customizado ------
     Troca a caixa nativa de opções por um botão + lista no design do
     site (mesma caixa, mesma borda, mesma tipografia dos outros campos).
     O <select> real continua no DOM — só some visualmente — então
     validação, leitores de tela e testes automatizados seguem lendo o
     valor dele normalmente. */
  $$('select', scope).forEach(function (sel) {
    if (sel.dataset.csDone) return;
    sel.dataset.csDone = 'true';

    var wrap = document.createElement('div');
    wrap.className = 'cs';
    sel.parentNode.insertBefore(wrap, sel);
    wrap.appendChild(sel);
    sel.classList.add('sr');
    sel.tabIndex = -1;

    var trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'cs-trigger';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    // O nome acessível do botão não pode depender só do texto da opção
    // escolhida: antes de qualquer seleção (estado placeholder), esse texto
    // está vazio e o botão fica sem nome para leitor de tela. O <label>
    // nativo do campo (sempre presente, ver build.py) cobre isso — mas
    // usar só aria-label="Cargo" (substituindo o nome acessível por
    // inteiro) faz o nome acessível NUNCA incluir o texto visível do botão
    // ("Selecione", ou a opção escolhida depois), o que viola WCAG 2.5.3
    // (Label in Name): quem usa comando de voz e fala o texto que vê na
    // tela não consegue ativar o campo, porque o nome que o software de
    // voz reconhece é outro. Em vez de aria-label, aria-labelledby
    // apontando pro <label> do campo E pro span do texto visível junta os
    // dois textos content live — sempre que o span mudar, o nome acessível
    // muda junto, sem precisar atualizar nada manualmente a cada render().
    var fieldLabel = sel.id && document.querySelector('label[for="' + sel.id + '"]');
    var labelSpanId = sel.id ? sel.id + '-cs-label' : '';
    if (fieldLabel && labelSpanId) {
      if (!fieldLabel.id) fieldLabel.id = sel.id + '-cs-fieldlabel';
      trigger.setAttribute('aria-labelledby', fieldLabel.id + ' ' + labelSpanId);
    }
    trigger.innerHTML = '<span class="cs-trigger-label"' + (labelSpanId ? ' id="' + labelSpanId + '"' : '') + '></span>' +
      '<svg class="cs-chev" viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true">' +
      '<path d="M1 1l5 5 5-5"/></svg>';
    wrap.insertBefore(trigger, sel);

    var menu = document.createElement('ul');
    menu.className = 'cs-menu';
    menu.setAttribute('role', 'listbox');
    menu.hidden = true;
    wrap.insertBefore(menu, sel);

    // optionEls fica sincronizado com os <li> reais a cada render() (o menu
    // é reconstruído do zero a cada mudança de valor, então não dá pra
    // guardar uma referência antiga). activeIdx é a opção destacada por
    // teclado enquanto o menu está aberto — o foco de verdade nunca sai do
    // botão (padrão ARIA APG de listbox popup), só aria-activedescendant
    // muda, então o leitor de tela anuncia cada opção normalmente.
    var optionEls = [];
    var activeIdx = -1;

    var closeMenu = function () {
      menu.hidden = true;
      trigger.classList.remove('is-open');
      trigger.setAttribute('aria-expanded', 'false');
      trigger.removeAttribute('aria-activedescendant');
      activeIdx = -1;
    };

    var highlight = function (idx) {
      activeIdx = idx;
      optionEls.forEach(function (o, n) { o.li.classList.toggle('is-active', n === idx); });
      if (idx >= 0 && optionEls[idx]) {
        trigger.setAttribute('aria-activedescendant', optionEls[idx].li.id);
        optionEls[idx].li.scrollIntoView({ block: 'nearest' });
      } else {
        trigger.removeAttribute('aria-activedescendant');
      }
    };

    var chooseOption = function (idx) {
      var o = optionEls[idx];
      if (!o) return;
      sel.value = o.opt.value;
      sel.dispatchEvent(new Event('change', { bubbles: true }));
      closeMenu();
      trigger.focus();
    };

    var render = function () {
      var opt = sel.options[sel.selectedIndex];
      $('.cs-trigger-label', trigger).textContent = opt ? opt.textContent : '';
      trigger.classList.toggle('cs-trigger--placeholder', !sel.value);
      menu.innerHTML = '';
      optionEls = [];
      Array.prototype.forEach.call(sel.options, function (o) {
        if (!o.value) return;
        var n = optionEls.length;
        var li = document.createElement('li');
        li.id = (sel.id || 'cs') + '-opt-' + n;
        li.className = 'cs-option' + (o.selected ? ' is-selected' : '');
        li.setAttribute('role', 'option');
        li.setAttribute('aria-selected', o.selected ? 'true' : 'false');
        li.textContent = o.textContent;
        li.addEventListener('click', function () { chooseOption(n); });
        menu.appendChild(li);
        optionEls.push({ li: li, opt: o });
      });
    };

    var openMenu = function () {
      $$('.cs-menu:not([hidden])').forEach(function (m) { m.hidden = true; });
      menu.hidden = false;
      trigger.classList.add('is-open');
      trigger.setAttribute('aria-expanded', 'true');
      var startIdx = 0;
      optionEls.forEach(function (o, n) { if (o.opt.selected) startIdx = n; });
      highlight(startIdx);
    };

    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var wasOpen = !menu.hidden;
      if (wasOpen) { closeMenu(); return; }
      openMenu();
    });

    trigger.addEventListener('keydown', function (e) {
      if (!optionEls.length) return;
      var isOpen = !menu.hidden;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!isOpen) { openMenu(); return; }
        highlight(Math.min(activeIdx + 1, optionEls.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (!isOpen) { openMenu(); return; }
        highlight(Math.max(activeIdx - 1, 0));
      } else if (isOpen && e.key === 'Home') {
        e.preventDefault();
        highlight(0);
      } else if (isOpen && e.key === 'End') {
        e.preventDefault();
        highlight(optionEls.length - 1);
      } else if (isOpen && (e.key === 'Enter' || e.key === ' ')) {
        e.preventDefault();
        if (activeIdx >= 0) chooseOption(activeIdx);
      } else if (isOpen && e.key === 'Escape') {
        e.preventDefault();
        closeMenu();
      }
    });

    sel.addEventListener('change', render);
    render();
  });

  /* ---------------------------------------------- máscaras de entrada */
  var onlyDigits = function (v) { return (v || '').replace(/\D+/g, ''); };

  var masks = {
    phone: function (v) {
      var d = onlyDigits(v).slice(0, 11);
      if (d.length <= 2) return d.length ? '(' + d : '';
      if (d.length <= 6) return '(' + d.slice(0, 2) + ') ' + d.slice(2);
      if (d.length <= 10) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
      return '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
    },
    doc: function (v) {
      var d = onlyDigits(v).slice(0, 14);
      if (d.length <= 11) {
        // CPF: 000.000.000-00. As duas primeiras trocas de "." são a
        // mesma regra aplicada duas vezes (cada uma pega o próximo bloco
        // de 3 dígitos ainda sem separador — por isso não dá pra
        // combinar num regex global só, o padrão muda de posição a cada
        // passada); a terceira troca o traço antes dos 2 dígitos finais.
        return d.replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d)/, '$1.$2').replace(/(\d{3})(\d{1,2})$/, '$1-$2');
      }
      // CNPJ: 00.000.000/0000-00. Quatro passos, um símbolo por vez, na
      // ordem em que aparecem da esquerda pra direita: 1º ponto (depois
      // dos 2 primeiros dígitos), 2º ponto (depois do bloco de 3
      // seguinte), a barra (depois do bloco de 3 seguinte) e por fim o
      // traço antes dos 2 dígitos finais.
      return d.replace(/^(\d{2})(\d)/, '$1.$2').replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
              .replace(/\.(\d{3})(\d)/, '.$1/$2').replace(/(\d{4})(\d{1,2})$/, '$1-$2');
    },
    currency: function (v) {
      // Esse campo só trabalha com reais inteiros (sem centavos). Sem essa
      // linha, alguém que digita ",50" ou ".50" no final (hábito normal de
      // escrever valor em reais) via os dois dígitos de centavo virarem
      // dígitos inteiros a mais — "1.000,50" virava R$ 100.050, 100x o
      // valor pretendido, silenciosamente. Descartar um sufixo de
      // separador decimal + 1-2 dígitos antes de raspar o resto evita essa
      // inflação sem mudar o comportamento normal de digitar só números.
      var d = onlyDigits((v || '').replace(/[.,]\d{1,2}$/, '')).slice(0, 12);
      if (!d) return '';
      return 'R$ ' + Number(d).toLocaleString('pt-BR');
    }
  };

  $$('[data-mask]').forEach(function (input) {
    if (input.dataset.maskBound) return;
    input.dataset.maskBound = '1';
    var fn = masks[input.dataset.mask];
    if (!fn) return;
    input.addEventListener('input', function () {
      var atEnd = input.selectionStart === input.value.length;
      input.value = fn(input.value);
      if (atEnd) input.setSelectionRange(input.value.length, input.value.length);
    });
  });

  /* --------------------------------------------------- validadores */
  var isEmail = function (v) { return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v.trim()); };
  var isPhone = function (v) { return onlyDigits(v).length >= 10; };
  var isDoc = function (v) { var n = onlyDigits(v).length; return n === 11 || n === 14; };

  function validateField(field) {
    var el = $('input, select, textarea', field);
    if (!el || el.disabled) return true;
    var v = (el.value || '').trim();
    var ok = true;
    if (el.required && !v) ok = false;
    if (ok && v && el.dataset.validate === 'email') ok = isEmail(v);
    if (ok && v && el.dataset.validate === 'phone') ok = isPhone(v);
    if (ok && v && el.dataset.validate === 'doc') ok = isDoc(v);
    if (ok && el.type === 'checkbox' && el.required) ok = el.checked;
    field.setAttribute('data-invalid', ok ? 'false' : 'true');
    el.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }

  function validateScope(scope) {
    var fields = $$('.field', scope);
    var ok = true;
    fields.forEach(function (f) { if (!validateField(f)) ok = false; });
    // grupos de escolha obrigatórios
    $$('[data-required-group]', scope).forEach(function (group) {
      var checked = $('input:checked', group);
      group.setAttribute('data-invalid', checked ? 'false' : 'true');
      if (!checked) ok = false;
    });
    // consentimento
    $$('.consent input[required]', scope).forEach(function (cb) {
      var wrap = cb.closest('.consent');
      if (!cb.checked) { ok = false; wrap.setAttribute('data-invalid', 'true'); }
      else wrap.setAttribute('data-invalid', 'false');
    });
    return ok;
  }

  $$('.field').forEach(function (f) {
    if (f.dataset.fieldBound) return;
    f.dataset.fieldBound = '1';
    var el = $('input, select, textarea', f);
    if (!el) return;
    // Só valida no blur se o campo tem valor (ex.: formato de e-mail errado).
    // Um campo obrigatório vazio que a pessoa nunca chegou a preencher não
    // deve acender erro só por ter passado o foco por ele (efeito colateral
    // do foco automático no primeiro campo do popup de captação, por
    // exemplo) — o obrigatório continua barrado no avanço/envio, via
    // validateScope.
    el.addEventListener('blur', function () { if (el.value) validateField(f); });
    el.addEventListener('input', function () { if (f.getAttribute('data-invalid') === 'true') validateField(f); });
  });

  /* ---------------------------------- CTA só libera após o consentimento */
  $$('form[data-endpoint-form]').forEach(function (form) {
    if (form.dataset.consentBound) return;
    form.dataset.consentBound = '1';
    var consent = $('input[name="consentimento"]', form);
    var cbtn = $('[data-step-submit], button[type="submit"]', form);
    if (!consent || !cbtn) return;
    var syncConsent = function () {
      cbtn.disabled = !consent.checked;
      cbtn.setAttribute('aria-disabled', String(!consent.checked));
    };
    consent.addEventListener('change', syncConsent);
    syncConsent();
  });

  /* ------------------------------------------------- envio de formulário */
  $$('form[data-endpoint-form]').forEach(function (form) {
    if (form.dataset.submitBound) return;
    form.dataset.submitBound = '1';
    var btn = $('[data-step-submit], button[type="submit"]', form);
    var ok = $('.formstate--ok', form);
    var err = $('.formstate--err', form);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // Trava contra duplo clique/duplo Enter enquanto o envio anterior
      // ainda está em voo: sem isso, dois cliques rápidos no botão disparam
      // dois POSTs (dois leads duplicados) antes do primeiro "finish" rodar
      // e desabilitar visualmente o botão — aria-disabled sozinho não barra
      // um novo evento de submit, só o estilo/leitor de tela.
      if (form.classList.contains('is-loading')) return;
      ok && ok.setAttribute('data-show', 'false');
      err && err.setAttribute('data-show', 'false');

      if (!validateScope(form)) {
        var bad = $('[data-invalid="true"] input, [data-invalid="true"] select, [data-invalid="true"] textarea', form);
        if (bad) { bad.focus(); bad.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' }); }
        return;
      }
      // Armadilha simples contra robôs
      var hp = $('.hp input', form);
      if (hp && hp.value) return;

      var cfg = window.ACROPOLE_CONFIG || {};
      var payload = {};
      new FormData(form).forEach(function (v, k) {
        if (k === 'company_website') return;
        payload[k] = typeof v === 'string' ? v.slice(0, 2000) : v;
      });
      payload.page = location.pathname;

      form.classList.add('is-loading');
      btn && btn.setAttribute('aria-disabled', 'true');

      var finish = function (success) {
        form.classList.remove('is-loading');
        btn && btn.removeAttribute('aria-disabled');
        if (success) {
          form.reset();
          // form.reset() limpa o <select> real, mas não dispara "change" —
          // o rótulo do menu customizado (.cs-trigger-label) ficaria
          // mostrando a opção antiga até o usuário mexer nele de novo.
          $$('select', form).forEach(function (s) {
            s.dispatchEvent(new Event('change', { bubbles: true }));
          });
          ok && ok.setAttribute('data-show', 'true');
          ok && ok.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' });
          // Formulários de captação de lead (modal e /contato) levam a
          // pessoa para o WhatsApp logo depois da confirmação, com uma
          // mensagem pronta. O link manual no formstate--ok cobre o caso
          // de o navegador bloquear o redirecionamento automático.
          var waUrl = form.getAttribute('data-whatsapp-redirect');
          if (waUrl) {
            setTimeout(function () { window.location.href = waUrl; }, 4000);
          }
        } else {
          err && err.setAttribute('data-show', 'true');
        }
      };

      if (!cfg.endpoint) {
        // Sem endpoint configurado: modo demonstração, nada é transmitido.
        setTimeout(function () { finish(true); }, 700);
        return;
      }

      // Timeout defensivo: sem isso, um endpoint que trava (DNS lento,
      // função morta, firewall silencioso) nunca resolve nem rejeita a
      // Promise, e o formulário fica preso em "is-loading" para sempre,
      // sem feedback nenhum pra pessoa tentar de novo.
      var controller = window.AbortController ? new AbortController() : null;
      var timer = setTimeout(function () {
        controller && controller.abort();
      }, 12000);

      fetch(cfg.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller ? controller.signal : undefined
      }).then(function (r) {
        clearTimeout(timer);
        finish(r.ok);
      }).catch(function () {
        clearTimeout(timer);
        finish(false);
      });
    });
  });

  /* ------------------------------------------------ filtros do blog */
  var artlist = $('[data-artlist]');
  if (artlist && !artlist.dataset.artlistBound) {
    artlist.dataset.artlistBound = '1';
    var rows = $$('.artrow', artlist);
    var empty = $('.artlist__empty', artlist);
    var search = $('[data-artsearch]');
    var count = $('[data-artcount]');
    var cat = 'todas';

    var norm = function (s) {
      return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    };

    var apply = function () {
      var q = norm(search ? search.value : '');
      var shown = 0;
      rows.forEach(function (r) {
        var mCat = cat === 'todas' || r.dataset.cat === cat;
        var mQ = !q || norm(r.dataset.index).indexOf(q) > -1;
        var show = mCat && mQ;
        r.style.display = show ? '' : 'none';
        if (show) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
      if (count) count.textContent = shown === 1 ? '1 artigo' : shown + ' artigos';
    };

    $$('.filter').forEach(function (f) {
      f.addEventListener('click', function () {
        cat = f.dataset.cat;
        $$('.filter').forEach(function (x) { x.setAttribute('aria-pressed', x === f ? 'true' : 'false'); });
        apply();
      });
    });
    if (search) search.addEventListener('input', apply);
    apply();
  }

  /* ------------------------------------------------------ compartilhar */
  $$('[data-share]').forEach(function (btn) {
    if (btn.dataset.shareBound) return;
    btn.dataset.shareBound = '1';
    btn.addEventListener('click', function () {
      var url = location.href;
      var title = document.title;
      if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function () {
          var old = btn.textContent;
          btn.textContent = 'Link copiado';
          setTimeout(function () { btn.textContent = old; }, 2200);
        });
      }
    });
  });
  } /* fim bindPage */

  window.Acropole = { bindGlobal: bindGlobal, bindPage: bindPage };

  function boot() { bindGlobal(); bindPage(document); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
