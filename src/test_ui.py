# -*- coding: utf-8 -*-
"""Testes de interação: navegação, gaveta, acordeão, índice de soluções,
busca do blog, etapas e validação do formulário, teclado e foco."""
import http.server
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
        check("CTA começa desabilitado antes do consentimento",
              pg.eval_on_selector("[data-step-submit]", "el => el.disabled") is True)

        pg.check('input[name="consentimento"]')
        check("CTA libera assim que o consentimento é marcado",
              pg.eval_on_selector("[data-step-submit]", "el => el.disabled") is False)

        pg.click("[data-step-submit]")
        pg.wait_for_timeout(250)
        check("bloqueia envio com campos vazios", pg.locator('[data-invalid="true"]').count() > 0)

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

        pg.uncheck('input[name="consentimento"]')
        check("desmarcar o consentimento desabilita o CTA de novo",
              pg.eval_on_selector("[data-step-submit]", "el => el.disabled") is True)
        pg.check('input[name="consentimento"]')

        pg.fill("#email", "contato@empresa.com.br")
        pg.click("[data-step-submit]")
        pg.wait_for_timeout(1400)
        check("envio válido mostra confirmação", pg.is_visible(".formstate--ok"))

        print("\n[teclado e foco]")
        pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        pg.keyboard.press("Tab")
        check("primeiro Tab chega ao atalho de conteúdo",
              pg.evaluate("() => document.activeElement.className") == "skip")

        pg.eval_on_selector(".rail[data-lead-modal]", "el => el.click()")
        pg.wait_for_timeout(400)
        check("popup de captação foca o 1º campo no desktop (teclado físico)",
              pg.evaluate("() => document.activeElement.id") == "lm-nome")
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
