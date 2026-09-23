# -*- coding: utf-8 -*-
"""Páginas legais e página de erro."""

from content.site import SITE, LEGAL_LINE
import build as B


def _legal_page(path, eyebrow, h1, lead, sections, note, title=None):
    trail = [("Início", "index.html"), (eyebrow, None)]
    body = B.pagehead(path, trail, "Institucional", h1, lead,
                      meta=[("Documento", eyebrow),
                            ("Última atualização", "2026"),
                            ("Responsável", f"Acrópole Capital, CNPJ {SITE['cnpj']}")],
                      variant=2, image_slot="legal")

    prose = ""
    for i, (title, paras) in enumerate(sections, 1):
        prose += f'<h2 id="s{i}">{i}. {title}</h2>'
        for p in paras:
            if isinstance(p, list):
                prose += "<ul>" + "".join(f"<li>{x}</li>" for x in p) + "</ul>"
            else:
                prose += f"<p>{p}</p>"

    toc = "".join(f'<li><a href="#s{i}">{t}</a></li>' for i, (t, _) in enumerate(sections, 1))

    body += f"""<section class="band">
  <div class="shell">
    <div class="cols cols--4-8 cols--sticky">
      <aside>
        <nav class="toc" aria-label="Seções do documento">
          <p class="tag mb-2">Seções</p><ol>{toc}</ol>
        </nav>
      </aside>
      <article class="prose">
        {prose}
        <div class="notice mt-4">{note}</div>
      </article>
    </div>
  </div>
</section>"""

    return {
        "path": path, "nav_key": None, "over": True,
        "title": title or f"{h1} | Acrópole Capital",
        "desc": lead[:188],
        "body": body,
        "schema": [B.breadcrumb_schema(trail)],
    }


def privacidade():
    return _legal_page(
        "politica-de-privacidade.html", "Política de Privacidade",
        "Política de Privacidade",
        "Como a Acrópole Capital trata os dados fornecidos neste site, em conformidade com a "
        "Lei Geral de Proteção de Dados (Lei nº 13.709/2018).",
        [
            ("Dados coletados", [
                "Coletamos os dados que você fornece voluntariamente por meio dos formulários deste site: nome, empresa, telefone ou WhatsApp, e-mail, CPF ou CNPJ, perfil, solução de interesse, valor aproximado da operação, ativos disponíveis para lastro, faixa de faturamento, prazo pretendido, cidade e estado, e a descrição do objetivo.",
                "Coletamos também dados de navegação por meio de ferramentas de análise, quando ativas, como páginas visitadas, origem do acesso e informações técnicas do dispositivo.",
            ]),
            ("Finalidade do tratamento", [
                "Os dados são utilizados exclusivamente para:",
                ["responder à solicitação de análise;",
                 "estruturar e simular operações compatíveis com o perfil informado;",
                 "manter o contato durante o processo de estruturação;",
                 "cumprir obrigações legais e regulatórias aplicáveis."],
            ]),
            ("Base legal", [
                "O tratamento se fundamenta no consentimento fornecido no envio do formulário e, quando aplicável, na execução de procedimentos preliminares a contrato, solicitados pelo próprio titular dos dados.",
            ]),
            ("Compartilhamento de dados", [
                "Dados podem ser compartilhados com instituições financeiras parceiras estritamente para viabilizar a análise solicitada, sempre com o seu conhecimento prévio e no volume mínimo necessário para aquela finalidade.",
                "Não vendemos, alugamos ou cedemos dados pessoais a terceiros para finalidades publicitárias.",
            ]),
            ("Consulta a bureau de crédito", [
                "Nenhuma consulta a bureau de crédito é realizada a partir do simples envio de um formulário deste site. Quando a consulta for necessária para a análise, ela ocorrerá apenas mediante autorização expressa e específica do titular.",
            ]),
            ("Cookies e ferramentas de medição", [
                "Este site pode utilizar cookies e ferramentas de análise para entender o uso das páginas e melhorar a experiência de navegação. Você pode gerenciar cookies diretamente nas configurações do seu navegador.",
            ]),
            ("Comentários e login com Google", [
                "Nos artigos da seção Conteúdos, é possível comentar após entrar com uma conta Google. Ao fazer login, coletamos o nome, o e-mail e a foto de perfil associados à sua conta Google, além do texto do comentário que você publicar.",
                "Esses dados são usados para identificar o autor de cada comentário e permitir que ele gerencie a própria participação, incluindo a exclusão do próprio comentário a qualquer momento, diretamente na página do artigo.",
                "Comentários publicados ficam visíveis publicamente para qualquer visitante do site. Podemos remover comentários que violem a lei, os Termos de Uso ou direitos de terceiros.",
                "Os dados de comentário são mantidos enquanto o comentário permanecer publicado, e eliminados quando você o excluir ou quando solicitar sua remoção pelos canais de contato informados nesta política.",
            ]),
            ("Retenção", [
                "Os dados são mantidos pelo prazo necessário ao atendimento da solicitação e ao cumprimento de obrigações legais e regulatórias, sendo eliminados ou anonimizados quando cessarem essas finalidades.",
            ]),
            ("Segurança", [
                "Adotamos medidas técnicas e organizacionais razoáveis para proteger os dados coletados contra acesso não autorizado, perda ou alteração indevida, incluindo validação de formulários, controle de acesso e proteção contra envios automatizados.",
            ]),
            ("Direitos do titular", [
                "Você pode solicitar, a qualquer momento, confirmação de tratamento, acesso, correção, anonimização, portabilidade, informação sobre compartilhamento, revogação de consentimento ou eliminação dos seus dados, conforme os direitos previstos na LGPD.",
                f"As solicitações podem ser feitas pelos canais de contato informados neste site, incluindo o e-mail {SITE['email']}.",
            ]),
            ("Atualizações desta política", [
                "Esta política pode ser atualizada periodicamente. A versão vigente estará sempre disponível nesta página, com a data da última revisão indicada no topo.",
            ]),
        ],
        "Este documento acompanha os Termos de Uso e os Avisos legais.")


def termos():
    return _legal_page(
        "termos-de-uso.html", "Termos de Uso",
        "Termos de Uso",
        ("Condições de acesso e uso deste site e dos canais de contato da Acrópole Capital, "
         "incluindo a natureza da atividade de assessoria e as regras de responsabilidade."),
        [
            ("Aceitação", [
                "Ao navegar neste site, você concorda com estes Termos de Uso e com a Política de Privacidade. Caso não concorde com qualquer disposição, recomendamos interromper a navegação.",
            ]),
            ("Natureza da atividade", [
                "A Acrópole Capital atua na assessoria e na estruturação de operações de crédito. Não é instituição financeira, não capta recursos do público e não concede crédito diretamente.",
                "A concessão, as condições e a decisão final de qualquer operação são de competência exclusiva da instituição financeira responsável, sujeitas às políticas e aos critérios dela.",
            ]),
            ("Caráter informativo do conteúdo", [
                "As informações, simulações, comparativos, artigos e materiais publicados neste site têm finalidade informativa. Não constituem oferta, proposta firme, recomendação de investimento, consultoria jurídica ou tributária, nem promessa de aprovação de crédito.",
                "Valores, taxas, prazos, limites e percentuais eventualmente mencionados são referências de mercado obtidas em fontes públicas identificadas, variam por instituição e por perfil, e estão sujeitos a alteração sem aviso prévio.",
            ]),
            ("Uso do site", [
                "Você se compromete a utilizar este site de forma lícita, sem tentar obter acesso não autorizado a sistemas, sem enviar dados falsos ou de terceiros sem autorização, e sem praticar atos que comprometam a segurança ou a disponibilidade do serviço.",
            ]),
            ("Propriedade intelectual", [
                "Textos, marcas, identidade visual, layout, diagramas e demais elementos deste site pertencem à Acrópole Capital ou a seus licenciantes, e não podem ser reproduzidos sem autorização prévia por escrito.",
                "Menções a instituições financeiras identificam relacionamento operacional e não implicam exclusividade ou preferência comercial.",
            ]),
            ("Limitação de responsabilidade", [
                "Empregamos esforços razoáveis para manter as informações corretas e atualizadas, mas não garantimos disponibilidade ininterrupta nem ausência total de erros. Decisões financeiras tomadas com base exclusivamente no conteúdo deste site são de responsabilidade do usuário.",
            ]),
            ("Alterações", [
                "Estes Termos podem ser alterados a qualquer momento. A versão vigente é sempre a publicada nesta página.",
            ]),
            ("Foro e legislação aplicável", [
                "Estes Termos são regidos pela legislação brasileira. Fica eleito o foro da comarca de São Paulo/SP, sede da empresa, para dirimir eventuais controvérsias, com renúncia a qualquer outro.",
            ]),
        ],
        "Este documento acompanha a Política de Privacidade e os Avisos legais.",
        title="Termos de Uso do Site | Acrópole Capital")


def avisos():
    return _legal_page(
        "avisos-legais.html", "Avisos legais",
        "Avisos legais",
        "Esclarecimentos sobre o que este site comunica, o que ele não comunica e como interpretar "
        "os números apresentados.",
        [
            ("Não somos instituição financeira", [
                LEGAL_LINE,
            ]),
            ("Nenhuma promessa de aprovação, taxa ou prazo", [
                "A Acrópole Capital não promete aprovação de crédito, taxa mínima, valor liberado, percentual de garantia ou prazo de liberação. Toda condição depende de análise e da política interna da instituição financeira, e pode mudar entre a simulação e a formalização.",
                "Expressões como “mediante análise”, “conforme perfil e critérios da operação” e “condições sujeitas à análise” devem ser lidas literalmente em todo o site.",
            ]),
            ("Sobre os dados de mercado citados", [
                "Os números apresentados em páginas institucionais e em conteúdos provêm de fontes públicas, entre elas o Banco Central do Brasil, a Abecip, a CBIC, a B3, a Serasa Experian e a legislação federal.",
                "Séries de concessão de crédito são medidas de fluxo mensal e sofrem sazonalidade relevante. Variações entre meses não devem ser lidas isoladamente como tendência estrutural. Médias de taxa são ponderadas e não representam a condição disponível a um tomador específico.",
                "As datas de referência acompanham cada número. Fontes revisam séries periodicamente, e um dado citado pode ter sido atualizado após a publicação.",
            ]),
            ("Canal para correções", [
                f"Se você identificar qualquer informação incorreta, desatualizada ou passível de induzir a erro neste site, escreva para {SITE['email']}. Corrigimos e registramos a data da revisão.",
            ]),
        ],
        "Este documento acompanha a Política de Privacidade e os Termos de Uso.",
        title="Avisos Legais e Regulatórios | Acrópole Capital")


def erro404():
    path = "404.html"
    body = f"""<section class="pagehead">
  <div class="pagehead__grid">
    <div class="pagehead__inner">
      <span class="tag" style="display:block;color:var(--iris-on-dark)">Erro 404</span>
      <h1>Esta página não existe, ou mudou de endereço.</h1>
      <p class="lead">O conteúdo pode ter sido movido durante uma reorganização do site. Os caminhos abaixo cobrem quase tudo o que existe aqui.</p>
    </div>
    <div class="pagehead__media" aria-hidden="true">{B.photo_or_art(path, "legal", "pagehead-2", eager=True)}</div>
  </div>
</section>
<section class="band">
  <div class="shell">
    <h2 class="sr">Caminhos principais do site</h2>
    <div class="rows rows--3">
      <div><h3>Soluções</h3><p class="small muted">As 8 estruturas, com aplicações, benefícios e cuidados.</p><div class="mt-1">{B.tlink("Ver soluções", "solucoes.html", path)}</div></div>
      <div><h3>Como funciona</h3><p class="small muted">O processo completo, da primeira conversa à liberação.</p><div class="mt-1">{B.tlink("Ver o processo", "como-funciona.html", path)}</div></div>
      <div><h3>Conteúdos</h3><p class="small muted">Artigos técnicos com fontes públicas identificadas.</p><div class="mt-1">{B.tlink("Ver conteúdos", "conteudos.html", path)}</div></div>
    </div>
    <div class="mt-4">{B.btn("Voltar para o início", "index.html", path)}</div>
  </div>
</section>"""
    return {
        "path": path, "nav_key": None, "over": True, "noindex": True,
        "title": "Página não encontrada | Acrópole Capital",
        "desc": ("A página solicitada não existe ou mudou de endereço. Use os caminhos abaixo para "
                 "encontrar soluções, processo e conteúdos da Acrópole Capital."),
        "body": body, "schema": [],
    }


def pages():
    return [privacidade(), termos(), avisos(), erro404()]
