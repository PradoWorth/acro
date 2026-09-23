# -*- coding: utf-8 -*-
"""Testes de interação: navegação, gaveta, acordeão, índice de soluções,
busca do blog, etapas e validação do formulário, teclado e foco."""
import base64
import http.server
import json
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

_R = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(_R) if os.path.basename(_R) == "src" else _R, "dist")
PORT = 8811
BASE = f"http://127.0.0.1:{PORT}"
fails = []


def check(label, cond, extra=""):
    print(("  ok  " if cond else "FALHA ") + label + (f"  {extra}" if extra and not cond else ""))
    if not cond:
        fails.append(label)


def serve():
    """Sobe o servidor e ajusta BASE para a porta realmente aberta — se a
    preferida estiver ocupada (socket em TIME_WAIT de uma execução anterior,
    por exemplo), usa porta 0 e deixa o sistema escolher, em vez de abortar."""
    global BASE
    os.chdir(DIST)
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", PORT), http.server.SimpleHTTPRequestHandler)
    except OSError:
        httpd = socketserver.TCPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
    BASE = f"http://127.0.0.1:{httpd.server_address[1]}"
    threading.Thread(target=httpd.serve_forever, daemon=True).start()


def run():
    serve()
    with sync_playwright() as p:
        br = p.chromium.launch()

        # ---------------------------------------------------------- desktop
        ctx = br.new_context(viewport={"width": 1440, "height": 900}, locale="pt-BR")
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        # Intercepta o webhook de leads (n8n) pra manter os testes
        # determinísticos e offline — sem isso, cada envio válido do
        # formulário durante os testes bateria de verdade no webhook de
        # TESTE da cliente, poluindo o fluxo dela no n8n com leads falsos
        # toda vez que a suíte roda. Guarda o corpo de cada chamada em
        # webhook_calls pra inspecionar depois (chaves obrigatórias do
        # payload: name/email/whatsapp/faturamento/tracking_params).
        webhook_calls = []

        def mock_webhook(route):
            try:
                webhook_calls.append(json.loads(route.request.post_data or "{}"))
            except Exception:
                webhook_calls.append({})
            route.fulfill(status=200, content_type="application/json", body='{"ok":true}')

        pg.route("https://n8n.srv1800205.hstgr.cloud/**", mock_webhook)

        print("\n[navegação de topo]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        sol_item = pg.locator(".nav__item[data-mega]").nth(0)
        prog_item = pg.locator(".nav__item[data-mega]").nth(1)
        sol_item.locator(".nav__link").hover()
        pg.wait_for_timeout(400)
        check("painel de soluções abre no hover", sol_item.locator(".megapanel a").first.is_visible())
        check("painel lista as 8 soluções", sol_item.locator(".megapanel__link").count() == 8)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        check("Escape fecha o painel", not sol_item.locator(".megapanel a").first.is_visible())

        pg.mouse.move(20, 600)          # tira o ponteiro do item antes de reabrir
        pg.wait_for_timeout(300)
        prog_item.locator(".nav__link").hover()
        pg.wait_for_timeout(400)
        check("painel de programas abre no hover", prog_item.locator(".megapanel a").first.is_visible())
        check("painel lista os 4 programas públicos", prog_item.locator(".megapanel__link").count() == 4)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        check("Escape fecha o painel de programas", not prog_item.locator(".megapanel a").first.is_visible())

        pg.mouse.move(20, 600)
        pg.wait_for_timeout(300)
        prog_item.locator(".nav__link").hover()
        pg.wait_for_timeout(400)
        prog_item.locator('.megapanel__link:has-text("Pronampe")').click()
        pg.wait_for_load_state("networkidle")
        check("link do painel de programas navega direto para a página isolada",
              pg.url.endswith("/programas/pronampe.html"), pg.url)
        check("migalha marca a página do Pronampe", pg.locator('.crumbs [aria-current]').count() == 1)

        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        sol_item = pg.locator(".nav__item[data-mega]").nth(0)
        pg.mouse.move(20, 600)
        pg.wait_for_timeout(300)
        sol_item.locator(".nav__link").hover()
        pg.wait_for_timeout(400)
        sol_item.locator('.megapanel__link:has-text("Home Equity")').click()
        pg.wait_for_load_state("networkidle")
        check("link do painel navega para página real",
              pg.url.endswith("/solucoes/home-equity.html"), pg.url)
        check("migalha marca a página atual", pg.locator('.crumbs [aria-current]').count() == 1)

        print("\n[cabeçalho fixo]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        bg_before = pg.evaluate("getComputedStyle(document.querySelector('.masthead')).backgroundColor")
        top_before = pg.evaluate("document.querySelector('.masthead').getBoundingClientRect().top")
        pg.mouse.wheel(0, 900)
        pg.wait_for_timeout(400)
        bg_after = pg.evaluate("getComputedStyle(document.querySelector('.masthead')).backgroundColor")
        check("cabeçalho mantém a mesma cor do topo ao rolar (não solidifica)",
              bg_before == bg_after, f"{bg_before} -> {bg_after}")
        top_after = pg.evaluate("document.querySelector('.masthead').getBoundingClientRect().top")
        check("cabeçalho continua fixo no topo da viewport ao rolar",
              top_before == 0 and top_after == 0, f"{top_before} -> {top_after}")
        pg.mouse.wheel(0, -1200)
        pg.wait_for_timeout(400)
        bg_top_again = pg.evaluate("getComputedStyle(document.querySelector('.masthead')).backgroundColor")
        check("cabeçalho segue com a mesma cor ao voltar ao topo",
              bg_before == bg_top_again, f"{bg_before} -> {bg_top_again}")
        pg.mouse.wheel(0, 900)
        pg.wait_for_timeout(500)
        check("contato discreto aparece só depois", pg.get_attribute(".rail", "data-show") == "true")
        check("botão flutuante entra na tela por transform, não por bottom (animação compositada na GPU, sem custo de layout — apontado pelo Lighthouse)",
              pg.eval_on_selector(".rail", "el => getComputedStyle(el).transform") != "none")
        check("nenhuma transição anima a propriedade bottom do botão flutuante",
              "bottom" not in pg.eval_on_selector(".rail", "el => getComputedStyle(el).transitionProperty"))

        print("\n[rolagem suave no trackpad/mouse]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(200)
        pg.mouse.wheel(0, 600)
        y_logo = pg.evaluate("window.scrollY")
        pg.wait_for_timeout(700)
        y_final = pg.evaluate("window.scrollY")
        check("rolagem não pula direto pro alvo (fica visivelmente pra trás logo após o gesto)",
              0 < y_logo < y_final * 0.85, f"logo após: {y_logo}, final: {y_final}")
        check("rolagem termina de convergir com folga (fluida, não trava antes do alvo)",
              y_final > y_logo, f"logo após: {y_logo}, final: {y_final}")
        # dentro de um painel com scroll próprio, a rolagem continua nativa —
        # não pode empurrar a página por trás dele.
        pg.goto(f"{BASE}/contato.html", wait_until="networkidle")
        pg.click(".cs-trigger")
        pg.wait_for_timeout(300)
        y_before = pg.evaluate("window.scrollY")
        menu_box = pg.locator(".cs-menu:not([hidden])").first.bounding_box()
        pg.mouse.move(menu_box["x"] + menu_box["width"] / 2, menu_box["y"] + menu_box["height"] / 2)
        pg.mouse.wheel(0, 200)
        pg.wait_for_timeout(300)
        y_after = pg.evaluate("window.scrollY")
        menu_scroll = pg.evaluate("document.querySelector('.cs-menu:not([hidden])').scrollTop")
        check("rolagem dentro do select customizado não move a página atrás dele",
              y_before == y_after and menu_scroll > 0, f"{y_before} -> {y_after}, menu scrollTop: {menu_scroll}")
        pg.keyboard.press("Escape")
        # Bug relatado pelo cliente: arrastar a barra de rolagem (ou qualquer
        # rolagem nativa disparada no meio de uma animação nossa) "brigava"
        # com a nossa rolagem suave e puxava a página de volta. Simula uma
        # rolagem externa instantânea (o mesmo mecanismo de uma barra de
        # rolagem arrastada ou da tecla End) enquanto a nossa animação ainda
        # está em andamento, e confirma que ela assume o controle na hora,
        # sem disputa.
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.evaluate("window.scrollTo({top: 0, left: 0, behavior: 'instant'})")
        pg.wait_for_timeout(200)
        pg.mouse.wheel(0, 2000)
        pg.wait_for_timeout(60)
        pg.evaluate("window.scrollTo({top: 5000, left: 0, behavior: 'instant'})")
        pg.wait_for_timeout(500)
        y_scrollbar = pg.evaluate("window.scrollY")
        check("rolagem externa (ex.: barra de rolagem) não é disputada pela animação — fica onde foi solta",
              abs(y_scrollbar - 5000) < 5, f"esperado ~5000, ficou em {y_scrollbar}")
        # Bug relatado pelo cliente: rolar por cima da esteira de depoimentos
        # travava a página. Causa: a esteira não tem rolagem própria no
        # desktop (é só uma animação de CSS), mas estava sendo tratada como
        # se tivesse — a rolagem suave alternava com a nativa toda hora que
        # o cursor passava por cima dela. Confirma que a rolagem continua
        # suave (convergindo aos poucos) mesmo com o cursor sobre a esteira.
        pg.evaluate("window.scrollTo({top: 0, left: 0, behavior: 'instant'})")
        testirow = pg.locator(".testirow")
        box = None
        for _ in range(30):
            pg.mouse.wheel(0, 400)
            pg.wait_for_timeout(80)
            if testirow.count():
                b = testirow.bounding_box()
                if b and 0 < b["y"] < 800:
                    box = b
                    break
        if box:
            pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            y_before_hover = pg.evaluate("window.scrollY")
            pg.mouse.wheel(0, 500)
            y_right_after = pg.evaluate("window.scrollY")
            pg.wait_for_timeout(700)
            y_hover_final = pg.evaluate("window.scrollY")
            check("rolagem sobre a esteira de depoimentos continua suave (não pula direto)",
                  y_before_hover <= y_right_after < y_hover_final,
                  f"antes: {y_before_hover}, logo após: {y_right_after}, final: {y_hover_final}")
        else:
            check("esteira de depoimentos encontrada pra testar", False, "não encontrada na rolagem")

        # Pedido do cliente: arrastar a esteira de depoimentos (mouse ou
        # dedo) pros dois lados, e ao soltar ela retoma sozinha o
        # deslizamento automático — antes, o pause por :hover/:focus-within
        # do CSS "grudava" no toque (ver comentário em site.css/site.js).
        print("\n[esteira de depoimentos: arrastar]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        testirow2 = pg.locator(".testirow")
        testirow2.scroll_into_view_if_needed()
        pg.wait_for_timeout(400)

        def track_transform():
            return pg.evaluate("document.querySelector('.testirow__track').style.transform")

        box2 = testirow2.bounding_box()
        cx, cy = box2["x"] + box2["width"] / 2, box2["y"] + box2["height"] / 2
        t0 = track_transform()
        pg.mouse.move(cx, cy)
        pg.mouse.down()
        pg.mouse.move(cx + 150, cy, steps=10)
        pg.wait_for_timeout(50)
        t_right = track_transform()
        pg.mouse.move(cx - 100, cy, steps=10)
        pg.wait_for_timeout(50)
        t_left = track_transform()
        pg.mouse.up()
        check("arrastar com o mouse move a esteira pros dois lados",
              t0 != t_right and t_right != t_left,
              f"antes: {t0}, arrastando p/ direita: {t_right}, arrastando p/ esquerda: {t_left}")
        t_release = track_transform()
        pg.wait_for_timeout(1200)
        t_depois = track_transform()
        check("ao soltar, a esteira retoma sozinha o deslizamento automático",
              t_release != t_depois, f"logo ao soltar: {t_release}, 1,2s depois: {t_depois}")

        print("\n[índice de soluções]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.click('.solrow[data-sol="auto-equity"]')
        pg.wait_for_timeout(300)
        check("clique troca o painel",
              pg.get_attribute('.solpanel[data-sol="auto-equity"]', "data-active") == "true")
        check("painel anterior fecha",
              pg.get_attribute('.solpanel[data-sol="capital-de-giro"]', "data-active") == "false")
        pg.focus('.solrow[data-sol="auto-equity"]')
        pg.keyboard.press("ArrowDown")
        pg.wait_for_timeout(200)
        check("setas navegam a lista",
              pg.evaluate("() => document.activeElement.dataset.sol") == "credito-pj")

        print("\n[acordeão de dúvidas]")
        pg.goto(f"{BASE}/como-funciona.html", wait_until="networkidle")
        first = pg.locator(".acc__btn").first
        check("acordeão começa fechado", first.get_attribute("aria-expanded") == "false")
        first.click()
        pg.wait_for_timeout(400)
        check("abre ao clicar", first.get_attribute("aria-expanded") == "true")
        check("painel fica visível", pg.locator(".acc__panel[data-open='true']").count() == 1)

        print("\n[busca e filtros do blog]")
        pg.goto(f"{BASE}/conteudos.html", wait_until="networkidle")
        total = pg.locator(".artrow").count()
        check("lista todos os artigos ao abrir", pg.inner_text("[data-artcount]") == f"{total} artigos")
        pg.click('.filter[data-cat="Capital de Giro"]')
        pg.wait_for_timeout(250)
        vis = pg.evaluate("() => [...document.querySelectorAll('.artrow')].filter(r=>r.style.display!=='none').length")
        check("filtro por categoria reduz a lista", 0 < vis < total, f"visíveis={vis}")
        pg.click('.filter[data-cat="todas"]')
        pg.fill("[data-artsearch]", "depreciacao")   # sem acento, testa a normalização
        pg.wait_for_timeout(250)
        vis = pg.evaluate("() => [...document.querySelectorAll('.artrow')].filter(r=>r.style.display!=='none').length")
        check("busca ignora acentuação", vis >= 1, f"visíveis={vis}")
        pg.fill("[data-artsearch]", "zzzzzz")
        pg.wait_for_timeout(250)
        check("estado vazio aparece", pg.is_visible(".artlist__empty"))

        print("\n[select customizado]")
        pg.goto(f"{BASE}/contato.html", wait_until="networkidle")
        pg.click('.field:has(#cargo) .cs-trigger')
        check("menu do select customizado abre", pg.is_visible('.field:has(#cargo) .cs-menu'))
        pg.click('.field:has(#cargo) .cs-option:text-is("Diretor")')
        check("opção clicada atualiza o select real",
              pg.eval_on_selector("#cargo", "el => el.value") == "Diretor")
        check("rótulo do botão mostra a opção escolhida",
              pg.inner_text('.field:has(#cargo) .cs-trigger-label') == "Diretor")
        check("menu fecha depois de escolher", not pg.is_visible('.field:has(#cargo) .cs-menu'))

        print("\n[formulário de contato]")
        check("botão Enviar sempre visível (formulário de uma etapa só)",
              pg.is_visible("[data-step-submit]"))
        # Pedido do cliente reconsiderado (risco de LGPD): a caixa de
        # consentimento nasce desmarcada, e o botão de Enviar NÃO fica mais
        # travado (disabled) enquanto ela está assim — ver comentário em
        # site.js. Confirma os dois: a caixa começa desmarcada, e o botão
        # já responde ao clique mesmo sem marcar.
        check("caixa de consentimento nasce desmarcada",
              pg.eval_on_selector('input[name="consentimento"]', "el => el.checked") is False)
        check("botão de enviar nunca fica travado (disabled) por causa da caixa",
              pg.eval_on_selector("[data-step-submit]", "el => el.disabled") is False)

        pg.click("[data-step-submit]")
        pg.wait_for_timeout(250)
        check("bloqueia envio com campos vazios", pg.locator('[data-invalid="true"]').count() > 0)
        check("tentar enviar sem marcar a caixa mostra o erro dela, visível",
              pg.get_attribute(".consent", "data-invalid") == "true" and pg.is_visible(".consent__err"))

        pg.fill("#telefone", "31988887777")
        check("máscara de telefone", pg.input_value("#telefone") == "(31) 98888-7777",
              pg.input_value("#telefone"))

        pg.fill("#nome", "Teste de Formulário")
        pg.fill("#empresa", "Empresa Teste Ltda")
        pg.select_option("#porte", "Média empresa")
        pg.select_option("#faturamento", "De R$ 5 a R$ 10 milhões ao ano")
        pg.select_option("#estrutura", "Capital de Giro")
        pg.select_option("#valor", "De R$ 500 mil a R$ 1 milhão")
        pg.select_option("#urgencia", "Nos próximos 3 meses")
        pg.check('input[name="restricao"][value="Não"]')
        pg.fill("#email", "endereco-invalido")
        pg.click("[data-step-submit]")
        pg.wait_for_timeout(300)
        check("e-mail inválido bloqueia o envio",
              pg.get_attribute("#email", "aria-invalid") == "true")
        check("com o resto certo, só a caixa de consentimento continua marcada como erro",
              pg.get_attribute(".consent", "data-invalid") == "true")

        pg.check('input[name="consentimento"]')
        check("marcar a caixa limpa o erro dela na hora, sem precisar tentar enviar de novo",
              pg.get_attribute(".consent", "data-invalid") == "false" and not pg.is_visible(".consent__err"))

        pg.fill("#email", "contato@empresa.com.br")
        pg.click("[data-step-submit]")
        pg.wait_for_timeout(1400)
        check("envio válido mostra confirmação", pg.is_visible(".formstate--ok"))

        check("webhook de leads recebeu exatamente 1 chamada nesse envio",
              len(webhook_calls) == 1, len(webhook_calls))
        if webhook_calls:
            body = webhook_calls[-1]
            for key in ("name", "email", "whatsapp", "faturamento", "tracking_params"):
                check(f'payload do webhook (contato) inclui a chave "{key}" preenchida',
                      bool(body.get(key)), body.get(key))
            check('"name" veio do campo "nome" do formulário de contato',
                  body.get("name") == "Teste de Formulário", body.get("name"))
            check('"whatsapp" veio do campo "telefone" do formulário de contato',
                  body.get("whatsapp") == "(31) 98888-7777", body.get("whatsapp"))
            try:
                tp = json.loads(body.get("tracking_params") or "{}")
            except Exception:
                tp = {}
            check("tracking_params é um JSON com page_location/user_agent/captured_at",
                  all(k in tp for k in ("page_location", "user_agent", "captured_at")), tp)

        print("\n[bug relatado: caixa marcada por autofill não limpava o aviso de erro]")
        # Print da cliente mostrava a caixa já MARCADA (verde) com a mensagem
        # "Marque a caixa acima pra continuar." ainda visível ao mesmo tempo —
        # sintoma de autofill/gerenciador de senha marcando a caixa sem
        # disparar o evento `change` que limpa esse aviso (ver comentário em
        # site.js). Reproduz o cenário sem depender de autofill de verdade:
        # gera o erro pelo caminho normal (tentar enviar sem marcar), depois
        # marca a caixa via JS SEM emitir `change` (como um autofill faria) e
        # confirma que o aviso continua preso até a sincronização de
        # `pageshow` (voltar por bfcache) rodar.
        pg.goto(f"{BASE}/contato.html", wait_until="networkidle")
        pg.click("[data-step-submit]")
        pg.wait_for_timeout(250)
        check("(preparação) tentar enviar sem marcar mostra o erro",
              pg.get_attribute(".consent", "data-invalid") == "true" and pg.is_visible(".consent__err"))
        pg.eval_on_selector('input[name="consentimento"]', "el => { el.checked = true; }")
        pg.wait_for_timeout(100)
        check("caixa marcada sem o evento `change` (como autofill faz) ainda deixa o aviso preso — reproduz o bug relatado",
              pg.get_attribute(".consent", "data-invalid") == "true" and pg.is_visible(".consent__err"))
        pg.evaluate("window.dispatchEvent(new Event('pageshow'))")
        pg.wait_for_timeout(100)
        check("ao voltar por bfcache (evento pageshow), o aviso é sincronizado e some — corrigido",
              pg.get_attribute(".consent", "data-invalid") == "false" and not pg.is_visible(".consent__err"))

        print("\n[programas: imagem + texto]")
        pg.goto(f"{BASE}/programas.html", wait_until="networkidle")
        check("cada programa tem uma imagem ao lado do título/resumo (.mediarow)",
              pg.locator("#pronampe .mediarow").count() == 1)
        check("imagem fica à esquerda do cabeçalho no desktop",
              pg.eval_on_selector("#pronampe .mediarow__media", "el => el.getBoundingClientRect().left")
              < pg.eval_on_selector("#pronampe .mediarow__body", "el => el.getBoundingClientRect().left"))
        check("tabela de condições volta a ocupar a largura inteira (fora do painel de imagem)",
              pg.locator("#pronampe .mediarow dl").count() == 0
              and pg.locator("#pronampe dl").count() == 1)
        check("link \"ver a página completa\" continua presente",
              pg.locator("#pronampe a:has-text('Ver a página completa')").count() == 1)
        check("âncora do programa continua funcionando (#pronampe)",
              pg.eval_on_selector("#pronampe", "el => el.tagName") == "SECTION")

        print("\n[simulador: só a taxa ao mês, sem taxa ao ano]")
        pg.select_option("#sim-programa", "pronampe")
        pg.wait_for_timeout(200)
        pg.fill("#sim-faturamento", "1000000")
        pg.fill("#sim-valor", "100000")
        pg.click("form[data-sim-form] button[type=submit]")
        pg.wait_for_timeout(400)
        taxa_row = pg.eval_on_selector("[data-sim-taxa-am]", "el => el.parentElement.textContent")
        check("mostra a taxa ao mês (pedido do cliente: valor mensal não assusta)",
              "ao mês" in taxa_row, taxa_row)
        check("NÃO mostra a taxa ao ano em lugar nenhum (pedido explícito do cliente)",
              "ao ano" not in taxa_row, taxa_row)

        print("\n[simulador de página individual: campo \"valor\" não fica órfão na grade]")
        pg.goto(f"{BASE}/programas/pronampe.html", wait_until="networkidle")
        check("campo \"valor que você gostaria de captar\" ocupa a linha inteira (sem gerar buraco do lado)",
              "field--full" in pg.eval_on_selector("#sim-valor", "el => el.closest('.field').className"))
        valor_w = pg.eval_on_selector("#sim-valor", "el => el.closest('.field').getBoundingClientRect().width")
        form_w = pg.eval_on_selector(".fgrid", "el => el.getBoundingClientRect().width")
        check("largura do campo bate com a largura do formulário (realmente cheio, não só a classe)",
              abs(valor_w - form_w) < 2, f"{valor_w} vs {form_w}")
        prazo_top = pg.eval_on_selector("#sim-prazo", "el => el.closest('.field').querySelector('.cs-trigger').getBoundingClientRect().top")
        fat_top = pg.eval_on_selector("#sim-faturamento", "el => el.getBoundingClientRect().top")
        check("\"Prazo desejado\" e \"Faturamento anual\" começam na mesma altura (rótulos do mesmo tamanho, sem quebrar linha um e não o outro)",
              abs(prazo_top - fat_top) < 2, f"{prazo_top} vs {fat_top}")

        print("\n[validação de CNPJ: checksum real, não só contagem de dígitos]")
        pg.goto(f"{BASE}/pronampe-2026.html", wait_until="networkidle")
        # Bloqueia a consulta à BrasilAPI pra manter este bloco determinístico
        # — aqui o alvo é só o checksum local (isValidCNPJ/isValidCPF), que
        # roda antes e independe de rede.
        pg.route("https://brasilapi.com.br/**", lambda route: route.abort())

        pg.fill("#pn-cnpj", "11444777000000")  # 14 dígitos, mas verificadores errados
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(200)
        check("CNPJ com dígitos verificadores errados é rejeitado (checksum mod-11, não só contagem)",
              pg.get_attribute("#pn-cnpj", "aria-invalid") == "true")

        pg.fill("#pn-cnpj", "11222333000181")  # CNPJ numérico com checksum correto
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(200)
        check("CNPJ numérico com checksum correto é aceito",
              pg.get_attribute("#pn-cnpj", "aria-invalid") == "false")
        check("máscara formata como 00.000.000/0000-00",
              pg.input_value("#pn-cnpj") == "11.222.333/0001-81", pg.input_value("#pn-cnpj"))

        # Formato alfanumérico (vigente desde 07/2026): letras maiúsculas nas
        # 12 primeiras posições, dígitos verificadores sempre numéricos.
        pg.fill("#pn-cnpj", "12ABC34501DE35")
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(200)
        check("CNPJ alfanumérico com checksum correto é aceito",
              pg.get_attribute("#pn-cnpj", "aria-invalid") == "false")
        check("máscara alfanumérica formata como AA.AAA.AAA/AAAA-00",
              pg.input_value("#pn-cnpj") == "12.ABC.345/01DE-35", pg.input_value("#pn-cnpj"))

        pg.fill("#pn-cnpj", "12ABC34501DE00")  # mesma raiz, DVs trocados
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(200)
        check("CNPJ alfanumérico com dígitos verificadores errados é rejeitado",
              pg.get_attribute("#pn-cnpj", "aria-invalid") == "true")

        print("\n[consulta de situação do CNPJ na BrasilAPI: informativa, nunca trava]")
        # Mocka a resposta da BrasilAPI (sem SLA, gratuita) pra não depender de
        # rede real neste teste. Confirma que a nota some/aparece com o tom
        # certo e que, mesmo com uma situação desfavorável, o campo continua
        # validando normalmente — a checagem é só um aviso, não um bloqueio.
        def mock_cnpj_status(situacao):
            def handler(route):
                route.fulfill(status=200, content_type="application/json",
                               body=f'{{"descricao_situacao_cadastral": "{situacao}"}}')
            return handler

        pg.unroute("https://brasilapi.com.br/**")
        pg.route("https://brasilapi.com.br/api/cnpj/v1/**", mock_cnpj_status("ATIVA"))
        pg.fill("#pn-cnpj", "11222333000181")
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(500)
        check("CNPJ ativo mostra nota positiva",
              "ativo" in pg.inner_text("#pn-cnpj-note").lower())
        check("nota positiva não marca o campo como inválido",
              pg.get_attribute("#pn-cnpj", "aria-invalid") == "false")
        pg.unroute("https://brasilapi.com.br/api/cnpj/v1/**")

        pg.route("https://brasilapi.com.br/api/cnpj/v1/**", mock_cnpj_status("BAIXADA"))
        pg.fill("#pn-cnpj", "12ABC34501DE35")  # CNPJ diferente, pra não bater no cache do anterior
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(500)
        check("CNPJ baixado mostra nota de atenção",
              "baixada" in pg.inner_text("#pn-cnpj-note").lower())
        check("nota de atenção sobre situação cadastral NÃO marca o campo como inválido nem trava o envio",
              pg.get_attribute("#pn-cnpj", "aria-invalid") == "false")
        pg.unroute("https://brasilapi.com.br/api/cnpj/v1/**")

        # Falha de rede/API (timeout, erro etc.): a nota deve simplesmente
        # sumir em silêncio, sem quebrar a validação do campo.
        pg.route("https://brasilapi.com.br/api/cnpj/v1/**", lambda route: route.abort())
        pg.fill("#pn-cnpj", "11444777000161")
        pg.locator("#pn-cnpj").blur()
        pg.wait_for_timeout(500)
        check("falha na consulta não deixa nenhuma nota visível nem invalida o campo",
              not pg.is_visible("#pn-cnpj-note") and pg.get_attribute("#pn-cnpj", "aria-invalid") == "false")
        pg.unroute("https://brasilapi.com.br/api/cnpj/v1/**")

        print("\n[formulário do Pronampe: e-mail agora obrigatório + webhook com chaves canônicas]")
        # Item novo (pedido da cliente): todo formulário do site passa a
        # enviar um webhook de lead com as chaves obrigatórias
        # name/email/whatsapp/faturamento/tracking_params. O Pronampe não
        # tinha campo de e-mail nenhum antes — precisou ganhar um. Confirma
        # que ele agora bloqueia sem e-mail válido, e que o payload chega
        # com as chaves canônicas mesmo os campos internos deste formulário
        # tendo nomes diferentes (telefone -> whatsapp, faturamento_mensal
        # -> faturamento).
        pg.goto(f"{BASE}/pronampe-2026.html", wait_until="networkidle")
        pg.route("https://brasilapi.com.br/**", lambda route: route.abort())
        pg.fill("#pn-nome", "Lead Pronampe Teste")
        pg.fill("#pn-telefone", "31988887777")
        pg.fill("#pn-email", "invalido")
        pg.fill("#pn-cnpj", "11222333000181")
        pg.select_option("#pn-faturamento", label="Abaixo de R$ 60.000/mês")
        # A página também tem o popup de captação (oculto) com os mesmos
        # seletores genéricos (name="consentimento", [data-step-submit]) —
        # escopar ao card do formulário do Pronampe evita pegar o do popup.
        # force=True porque essa página tem animações de "revelar ao
        # rolar" (data-reveal) nos blocos ao redor do formulário — sem
        # isso, a checagem de estabilidade do Playwright intercala com uma
        # transição ainda em andamento e o clique acaba não sendo único.
        # delay=100 entre mousedown/mouseup: sem isso o clique instantâneo
        # às vezes colide com o blur do campo de faturamento preenchido
        # logo antes (o navegador não registra o clique como único gesto
        # down+up no mesmo elemento) e a caixa nunca fica marcada de
        # verdade — descoberto isolando down/up manualmente com um atraso.
        consent_pn = pg.locator('.pronampe-formcard input[name="consentimento"]')
        consent_pn.scroll_into_view_if_needed()
        pg.wait_for_timeout(300)
        consent_pn.click(force=True, delay=100)
        pg.wait_for_timeout(100)
        pg.click(".pronampe-formcard [data-step-submit]")
        pg.wait_for_timeout(300)
        check("e-mail inválido bloqueia o envio no Pronampe (campo novo, agora obrigatório)",
              pg.get_attribute("#pn-email", "aria-invalid") == "true")

        pg.fill("#pn-email", "lead@empresa.com.br")
        calls_before = len(webhook_calls)
        pg.click(".pronampe-formcard [data-step-submit]")
        pg.wait_for_timeout(1400)
        check("envio válido do Pronampe mostra confirmação", pg.is_visible(".formstate--ok"))
        check("webhook recebeu a chamada do envio do Pronampe",
              len(webhook_calls) == calls_before + 1, len(webhook_calls))
        if len(webhook_calls) > calls_before:
            body = webhook_calls[-1]
            for key in ("name", "email", "whatsapp", "faturamento", "tracking_params"):
                check(f'payload do webhook (Pronampe) inclui a chave "{key}" preenchida',
                      bool(body.get(key)), body.get(key))
            check('"whatsapp" veio do campo "telefone" do Pronampe (alias de nome de campo)',
                  body.get("whatsapp") == "(31) 98888-7777", body.get("whatsapp"))
            check('"faturamento" veio do campo "faturamento_mensal" do Pronampe (alias — nome interno diferente)',
                  body.get("faturamento") == "abaixo-60k", body.get("faturamento"))
        pg.unroute("https://brasilapi.com.br/**")

        print("\n[teclado e foco]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.keyboard.press("Tab")
        check("primeiro Tab chega ao atalho de conteúdo",
              pg.evaluate("() => document.activeElement.className") == "skip")

        pg.eval_on_selector(".rail[data-lead-modal]", "el => el.click()")
        pg.wait_for_timeout(400)
        check("popup de captação foca o 1º campo no desktop (teclado físico)",
              pg.evaluate("() => document.activeElement.id") == "lm-nome")

        print("\n[cache busting: CSS/JS versionados por hash do conteúdo]")
        # Bug relatado pela cliente rastreado até isso: sem uma URL que muda
        # a cada deploy, o navegador (e a borda da Vercel) podem continuar
        # servindo um site.css velho por até 1h depois do HTML novo já estar
        # no ar — CSS e HTML descompassados na mesma visita (ver
        # cache_bust em build.py). Confirma que toda folha de estilo/script
        # externo carrega com "?v=<hash>" e responde 200 — ou seja, a versão
        # é sempre a que bate com o HTML que a referencia.
        css_href = pg.get_attribute('link[rel="stylesheet"]', "href")
        site_js_src = pg.eval_on_selector('script[src*="site.js"]', "el => el.getAttribute('src')")
        config_js_src = pg.eval_on_selector('script[src*="config.js"]', "el => el.getAttribute('src')")
        check("site.css é servido com \"?v=<hash>\" na URL", "?v=" in (css_href or ""), css_href)
        check("site.js é servido com \"?v=<hash>\" na URL", "?v=" in (site_js_src or ""), site_js_src)
        check("config.js é servido com \"?v=<hash>\" na URL", "?v=" in (config_js_src or ""), config_js_src)
        css_status = pg.evaluate(f"() => fetch('{css_href}').then(r => r.status)")
        check("a URL versionada do CSS responde 200 (não é um link quebrado)", css_status == 200, css_status)

        print("\n[tracking_params: captura de UTM/gclid/fbclid e cookie de atribuição]")
        # Lógica pedida pela cliente (mesma da landing do Diagnóstico 360,
        # adaptada aqui): UTMs e cliques pagos na URL viram um cookie
        # próprio (app_attribution, 30 dias) e são replicados em JSON no
        # campo oculto tracking_params de todo formulário do site.
        pg.context.clear_cookies()
        pg.goto(f"{BASE}/contato.html?utm_source=google&utm_medium=cpc&utm_campaign=teste-sessao&gclid=abc123",
                wait_until="networkidle")
        pg.wait_for_timeout(200)
        tp_value = pg.eval_on_selector('input[name="tracking_params"]', "el => el.value")
        try:
            tp = json.loads(tp_value or "{}")
        except Exception:
            tp = {}
        check("utm_source da URL foi capturado no campo tracking_params",
              tp.get("utm_source") == "google", tp)
        check("utm_medium da URL foi capturado", tp.get("utm_medium") == "cpc", tp)
        check("utm_campaign da URL foi capturado", tp.get("utm_campaign") == "teste-sessao", tp)
        check("gclid da URL foi capturado", tp.get("gclid") == "abc123", tp)
        check("cookie app_attribution foi gravado (30 dias)",
              any(c["name"] == "app_attribution" for c in pg.context.cookies()))

        # Navega para OUTRA página sem UTM na URL: a atribuição já capturada
        # tem que sobreviver (não pode se perder ao trocar de página), e o
        # campo oculto da nova página (formulário diferente) também chega
        # preenchido com os mesmos dados.
        pg.goto(f"{BASE}/pronampe-2026.html", wait_until="networkidle")
        pg.wait_for_timeout(200)
        tp2_value = pg.eval_on_selector('input[name="tracking_params"]', "el => el.value")
        try:
            tp2 = json.loads(tp2_value or "{}")
        except Exception:
            tp2 = {}
        check("atribuição sobrevive à navegação entre páginas (sem UTM novo na URL)",
              tp2.get("utm_source") == "google" and tp2.get("gclid") == "abc123", tp2)

        print("\n[comentários (login Google) nos artigos de Conteúdos]")
        ARTICLE = "credito-empresarial-como-funciona"
        # Sem googleClientId configurado (estado real hoje, até a cliente
        # publicar o backend PHP na Hostinger e preencher config.js), a
        # seção inteira tem que ficar oculta — nunca aparecer quebrada
        # (sem login, sem comentário nenhum carregando).
        pg.goto(f"{BASE}/conteudos/{ARTICLE}.html", wait_until="networkidle")
        check("sem googleClientId configurado, a seção de comentários fica oculta",
              pg.get_attribute("[data-comments]", "hidden") is not None)

        # A partir daqui, simula o recurso já publicado: intercepta
        # config.js pra injetar um googleClientId de teste, o script do GIS
        # (nunca o real — sem rede externa aqui, e não precisamos da UI
        # oficial do Google pra testar NOSSA lógica) por uma versão fake
        # mínima que só expõe initialize/renderButton/disableAutoSelect, e
        # os 3 endpoints PHP (não existe backend PHP nesse servidor de
        # teste, que só serve os arquivos estáticos de dist/).
        real_config_js = open(os.path.join(DIST, "assets", "js", "config.js"), encoding="utf-8").read()
        fake_config_js = real_config_js.replace('googleClientId:""', 'googleClientId:"test-client-id.apps.googleusercontent.com"')
        assert fake_config_js != real_config_js, "não achou a linha googleClientId em config.js pra substituir no teste"
        pg.route("**/assets/js/config.js*", lambda route: route.fulfill(
            status=200, content_type="application/javascript", body=fake_config_js))

        fake_gsi_js = """
        window.google = { accounts: { id: {
          initialize: function (opts) { window.__acropoleGsiCallback = opts.callback; },
          renderButton: function () {},
          disableAutoSelect: function () {}
        } } };
        """
        pg.route("https://accounts.google.com/gsi/client", lambda route: route.fulfill(
            status=200, content_type="application/javascript", body=fake_gsi_js))

        posted = []

        def mock_comments_list(route):
            route.fulfill(status=200, content_type="application/json",
                           body=json.dumps({"ok": True, "comments": posted}))

        def mock_comments_post(route):
            body = json.loads(route.request.post_data or "{}")
            comment = {
                "id": len(posted) + 1, "body": body.get("body", ""),
                "created_at": "2026-01-01T12:00:00Z",
                "google_sub": "g-sub-teste", "name": "Fulano de Teste",
                "avatar_url": "https://lh3.googleusercontent.com/fake",
            }
            posted.append(comment)
            route.fulfill(status=200, content_type="application/json",
                           body=json.dumps({"ok": True, "comment": comment}))

        def mock_comments_delete(route):
            body = json.loads(route.request.post_data or "{}")
            posted[:] = [c for c in posted if c["id"] != body.get("id")]
            route.fulfill(status=200, content_type="application/json", body='{"ok":true}')

        pg.route("**/api/comments-list.php*", mock_comments_list)
        pg.route("**/api/comments-post.php", mock_comments_post)
        pg.route("**/api/comments-delete.php", mock_comments_delete)

        pg.goto(f"{BASE}/conteudos/{ARTICLE}.html", wait_until="networkidle")
        pg.wait_for_timeout(300)
        check("com googleClientId configurado, a seção de comentários aparece",
              pg.get_attribute("[data-comments]", "hidden") is None)
        check("sem estar logado, o formulário de comentário fica oculto",
              pg.get_attribute(".comments__form", "hidden") is not None)

        # Fake JWT (header.payload.assinatura) só pra exercitar a
        # decodificação client-side do payload (nome/foto pra exibir) — a
        # prova de identidade de verdade é sempre o backend revalidando
        # com o Google, nunca esse decode local.
        payload = base64.urlsafe_b64encode(json.dumps({
            "sub": "g-sub-teste", "name": "Fulano de Teste",
            "email": "fulano@example.com", "picture": "https://lh3.googleusercontent.com/fake",
        }).encode()).decode().rstrip("=")
        fake_jwt = f"eyJhbGciOiJSUzI1NiJ9.{payload}.assinatura-fake"
        pg.evaluate(f"() => window.__acropoleGsiCallback({{credential: {json.dumps(fake_jwt)}}})")
        pg.wait_for_timeout(200)
        check("depois do login (simulado), o formulário de comentário aparece",
              pg.get_attribute(".comments__form", "hidden") is None)
        check("depois do login, o nome da conta aparece", pg.text_content(".comments__username") == "Fulano de Teste")

        pg.fill(".comments__form textarea", "Ótimo artigo, muito claro!")
        pg.click(".comments__form .comments__submit")
        pg.wait_for_timeout(300)
        check("comentário enviado aparece na lista", pg.text_content(".comments__item-text") == "Ótimo artigo, muito claro!")
        check("nome do autor aparece junto do comentário", pg.text_content(".comments__item-name") == "Fulano de Teste")
        check("botão de excluir aparece (comentário é do próprio usuário logado)",
              pg.is_visible(".comments__item-delete"))

        pg.click(".comments__item-delete")
        pg.wait_for_timeout(300)
        check("depois de excluir, a lista volta a ficar vazia", pg.locator(".comments__item").count() == 0)
        check("mensagem de 'seja a primeira pessoa' volta a aparecer", pg.is_visible(".comments__empty"))

        pg.unroute("**/assets/js/config.js*")
        pg.unroute("https://accounts.google.com/gsi/client")
        pg.unroute("**/api/comments-list.php*")
        pg.unroute("**/api/comments-post.php")
        pg.unroute("**/api/comments-delete.php")

        ctx.close()

        # ----------------------------------------------------------- mobile
        print("\n[gaveta mobile]")
        ctx = br.new_context(viewport={"width": 390, "height": 844},
                             is_mobile=True, has_touch=True, locale="pt-BR")
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        check("gaveta começa fechada", pg.get_attribute(".drawer", "data-open") == "false")
        pg.click(".burger")
        pg.wait_for_timeout(600)
        check("gaveta abre", pg.get_attribute(".drawer", "data-open") == "true")
        check("body trava o scroll", pg.locator("body.is-locked").count() == 1)
        pg.locator("[data-drawer-toggle]").nth(0).click()
        pg.wait_for_timeout(300)
        check("submenu de soluções expande", pg.get_attribute("#drawer-sol", "data-open") == "true")
        check("submenu lista visão geral + 8 páginas",
              pg.locator("#drawer-sol a").count() == 9)
        pg.locator("[data-drawer-toggle]").nth(1).click()
        pg.wait_for_timeout(300)
        check("submenu de programas expande", pg.get_attribute("#drawer-prog", "data-open") == "true")
        check("submenu lista os 4 programas públicos",
              pg.locator("#drawer-prog a").count() == 4)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        check("Escape fecha a gaveta", pg.get_attribute(".drawer", "data-open") == "false")
        check("scroll é liberado", pg.locator("body.is-locked").count() == 0)

        print("\n[programas: imagem + texto no celular]")
        pg.goto(f"{BASE}/programas.html", wait_until="networkidle")
        check("no celular a imagem empilha ACIMA do texto (não lado a lado)",
              pg.eval_on_selector("#pronampe .mediarow__media", "el => el.getBoundingClientRect().top")
              < pg.eval_on_selector("#pronampe .mediarow__body", "el => el.getBoundingClientRect().top"))

        print("\n[popup de captação no celular]")
        pg.eval_on_selector(".rail[data-lead-modal]", "el => el.click()")
        pg.wait_for_timeout(400)
        check("NÃO foca campo algum ao abrir em toque (evita zoom travado no iOS)",
              pg.evaluate("() => document.activeElement.tagName") != "INPUT")
        check("popup inteiro não aceita nenhum gesto de zoom/arrasto (touch-action: none)",
              pg.eval_on_selector(".leadmodal", "el => getComputedStyle(el).touchAction") == "none")
        check("dialog só permite rolagem vertical (touch-action: pan-y) — sem pinça, sem arrasto lateral",
              pg.eval_on_selector(".leadmodal__dialog", "el => getComputedStyle(el).touchAction") == "pan-y")
        check("fundo escurecido não aceita gesto nenhum (touch-action: none)",
              pg.eval_on_selector(".leadmodal__overlay", "el => getComputedStyle(el).touchAction") == "none")
        check("dialog mantém canto arredondado (não fica de ponta a ponta)",
              pg.eval_on_selector(".leadmodal__dialog", "el => parseFloat(getComputedStyle(el).borderRadius)") > 0)
        pg.click("#lm-nome")
        pg.fill("#lm-nome", "Teste")
        check("o campo continua digitável ao toque manual",
              pg.input_value("#lm-nome") == "Teste")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(400)

        print("\n[tipografia de formulário no mobile]")
        pg.goto(f"{BASE}/contato.html", wait_until="networkidle")
        sizes = pg.evaluate("""() => [...document.querySelectorAll('input,select,textarea')]
            .map(e => parseFloat(getComputedStyle(e).fontSize))""")
        check("nenhum campo abaixo de 16px (evita zoom no iOS)",
              all(s >= 16 for s in sizes if s > 0), str(sorted(set(sizes))))

        print("\n[aviso de cookies]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.wait_for_timeout(300)
        check("aparece na 1ª visita", pg.get_attribute("#cookiebar", "data-show") == "true")
        check("é uma caixinha pequena no canto (não uma barra ocupando a linha inteira)",
              pg.eval_on_selector("#cookiebar", "el => el.getBoundingClientRect().width") < 350)
        pg.click("[data-cookie-accept]")
        pg.wait_for_timeout(400)
        check("some ao aceitar", pg.get_attribute("#cookiebar", "data-show") == "false")
        check("lembra a escolha (localStorage)",
              pg.evaluate("() => localStorage.getItem('cookieconsent:v1')") == "accepted")
        pg.reload(wait_until="networkidle")
        pg.wait_for_timeout(300)
        check("não aparece de novo depois de aceito",
              pg.get_attribute("#cookiebar", "data-show") == "false")
        pg.evaluate("() => localStorage.removeItem('cookieconsent:v1')")  # não vaza estado pros testes seguintes
        ctx.close()
        br.close()

        print("\n[erros de JavaScript]")
        check("nenhum erro de página", not errs, str(errs[:3]))

    print("\n" + ("TODOS OS TESTES PASSARAM" if not fails else f"{len(fails)} FALHAS: {fails}"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(run())
