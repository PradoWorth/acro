# -*- coding: utf-8 -*-
"""Configuração institucional, navegação e registro de soluções."""

# =============================================================================
# PREENCHA AQUI ANTES DE PUBLICAR
# -----------------------------------------------------------------------------
# Tudo que estiver como None é dado que ainda não foi fornecido. O site trata
# None com elegância: a linha simplesmente não é publicada, em vez de mostrar
# um campo vazio ou um link quebrado.
#
# Depois de preencher:  python3 build.py && python3 preflight.py
# O preflight recusa a publicação enquanto faltar qualquer item obrigatório.
# =============================================================================

CONTATO = {
    # Obrigatórios para publicar
    "whatsapp":  "5543984321492",   # mesmo número do telefone informado (celular com 9º dígito)
    "email":     "contato@acropolecapital.com.br",

    # Opcionais: se ficarem None, a linha não aparece no site
    "telefone":  "+5543984321492",
    "endereco":  "Avenida Paulista, 91 - Conj 905, Edifício Paulista Tower",
    "horario":   "Segunda a sexta, 8h às 18h",
    "linkedin":  "https://www.linkedin.com/company/acropolecapital",
    "instagram": "https://instagram.com/acropolecapital",
    "youtube":   "https://youtube.com/@acropolecapital",
}

# Fotografia real (opcional, por página). Enquanto ficar None, a página usa a
# arte SVG institucional no lugar — nunca fica sem imagem, então não há
# pressa nem risco em publicar antes de ter as fotos.
#
# Para ativar uma foto: salve o arquivo em src/static/assets/img/ (o build
# copia essa pasta inteira para dist/assets/img/) e troque o None abaixo pelo
# caminho relativo, ex.: "assets/img/hero.jpg".
#
# Onde cada uma aparece e o que buscar (ver também README, seção "Briefing de
# fotografia"): evitar aperto de mão, gente sorrindo com dinheiro, calculadora,
# moeda, gráfico decorativo ou retrato de banco de imagem — a foto precisa
# comunicar patrimônio e estrutura, não simpatia.
# Placeholder temporário para os campos de foto ainda sem imagem própria —
# pedido do cliente, para já ter uma apresentação com "cara de site pronto"
# em vez de arte SVG em todo canto, enquanto as fotos reais não chegam.
# É a mesma foto do carro já usada no artigo "Auto equity: prazo e
# depreciação" (a única foto real que o projeto já tinha). Substituir campo
# a campo, um de cada vez, é só trocar o valor de None (ou desta mesma
# string) pelo caminho da foto definitiva — sem foto nenhuma, o campo volta
# a cair na arte SVG institucional normalmente.
_PLACEHOLDER_CARRO = "assets/img/conteudos/auto-equity-prazo-e-depreciacao.jpg"

IMAGES = {
    # ---- topos de página (pagehead), um por rota -------------------------
    "hero":                    None,  # home — hero agora é o globo 3D animado (ver content/globe.py), não usa mais foto
    "sobre":                   "assets/img/sobre-pagehead.jpg",  # /sobre — foto enviada pelo cliente (licença livre) — notebook, caderno de anotações e celular numa mesa de trabalho
    "como-funciona":           "assets/img/como-funciona-pagehead.jpg",  # /como-funciona — foto pesquisada (Unsplash, licença livre) — mãos revisando documentos numa mesa
    "empresas":                "assets/img/empresas-pagehead.jpg",  # /empresas — foto real enviada pelo cliente (equipe trabalhando num escritório) — comunica operação em funcionamento, coerente com "uma empresa lucrativa pode ficar sem caixa"
    "investidores":            "assets/img/investidores-pagehead.jpg",  # /investidores — foto real enviada pelo cliente (tela com gráfico de mercado, mão apontando um ponto de leitura) — comunica acompanhamento técnico da operação
    "agronegocio":             "assets/img/agronegocio-pagehead.jpg",  # /agronegocio — foto pesquisada (Pexels, licença livre) — silos de grãos, sem pessoas
    "solucoes":                "assets/img/solucoes-pagehead.jpg",  # /solucoes (hub) — foto pesquisada (Unsplash, licença livre) — skyline aéreo de arranha-céus
    "diagnostico":             "assets/img/diagnostico-pagehead.jpg",  # /diagnostico — foto pesquisada (Pexels, licença livre) — mãos apontando um contrato ao lado de notebook
    "conteudos":               "assets/img/conteudos-pagehead.jpg",  # /conteudos (hub do blog) — foto real enviada pelo cliente (lousa com anotações, lâmpada ao centro) — comunica ideia/estudo, coerente com "material técnico"
    "contato":                 "assets/img/contato-pagehead.jpg",  # /contato — foto real enviada pelo cliente (especialista num ambiente de análise, telas com dados ao fundo) — comunica leitura técnica, sem sorriso de banco de imagem
    "governanca":              "assets/img/governanca-pagehead.jpg",  # /governanca — foto pesquisada (Unsplash, licença livre) — pastas organizadas em prateleiras de escritório
    "legal":                   "assets/img/legal-pagehead.jpg",  # políticas, termos, avisos e 404 — foto pesquisada (Unsplash, licença livre) — pastas vermelhas em prateleira
    "consultoria":             "assets/img/consultoria-pagehead.jpg",  # /consultoria — foto pesquisada (Pexels, licença livre) — reunião de trabalho em escritório moderno
    "credito-empresarial-sp":  "assets/img/credito-empresarial-sp-pagehead.jpg",  # /credito-empresarial-sao-paulo — foto pesquisada (Unsplash, licença livre) — Avenida Paulista, São Paulo (geotag confirmado)
    "programas":               "assets/img/programas-pagehead.jpg",  # /programas — foto pesquisada (Pexels, licença livre) — profissionais revisando documentos em sala de reunião
    "calculadora-giro":        "assets/img/calculadora-giro-pagehead.jpg",  # /calculadora-capital-de-giro — foto pesquisada (Pexels, licença livre) — mão operando calculadora ao lado de documentos financeiros

    # ---- uma foto por solução (opcional — sem ela, fica o diagrama) ------
    "solucao-capital-de-giro":            "assets/img/solucao-capital-de-giro.jpg",  # foto pesquisada (Pexels, licença livre) — corredor de armazém com prateleiras de caixas
    "solucao-home-equity":                "assets/img/solucao-home-equity.jpg",  # foto pesquisada (Unsplash, licença livre) — casa contemporânea de alto padrão
    "solucao-auto-equity":                "assets/img/solucao-auto-equity.jpg",  # foto pesquisada (Pexels, licença livre) — traseira de carro esportivo, enquadramento completo (a pedido do cliente, sem o recorte fechado usado antes)
    "solucao-credito-pj":                 "assets/img/solucao-credito-pj.jpg",  # foto pesquisada (Pexels, licença livre) — fachada de prédio comercial de vidro
    "solucao-estruturacao-de-credito":    "assets/img/solucao-estruturacao-de-credito.jpg",  # foto pesquisada (Pexels, licença livre) — mãos revisando gráficos financeiros
    "solucao-financiamento":              "assets/img/solucao-financiamento.jpg",  # foto pesquisada (Pexels, licença livre) — mão assinando documento
    "solucao-aquisicao-e-construcao":     "assets/img/solucao-aquisicao-e-construcao.jpg",  # foto pesquisada (Pexels, licença livre) — prédio em construção com guindaste
    "solucao-mercado-de-capitais":        "assets/img/solucao-mercado-de-capitais.jpg",  # foto pesquisada (Pexels, licença livre) — gráfico de candlestick em tela, enquadramento completo (a pedido do cliente, sem o recorte usado antes)

    # ---- uma foto por programa público, na página isolada dele -----------
    # (opcional — sem ela, fica o diagrama). Pedido do cliente: cada programa
    # (BNDES, PEAC FGI, Pronampe, Procred 360) ganhou sua própria página
    # (/programas/<slug>), separada da página de visão geral com âncoras
    # (/programas), justamente para poder ter imagem e conteúdo próprios.
    "programa-bndes":       "assets/img/programa-bndes.jpg",  # foto enviada pelo cliente — fachada real da sede do BNDES no Rio de Janeiro (o próprio assunto da página, não é branding incidental de terceiro)
    "programa-peac-fgi":    "assets/img/programa-peac-fgi-2.jpg",  # substituição: a arte enviada era o logotipo oficial do BNDES (marca registrada de terceiro), diferente do banner genérico de bandeira usado em Pronampe/Procred 360 — usei o plano B já combinado na pesquisa original: a mesma foto do homem assinando contrato (ver README item 145)
    "programa-pronampe":    "assets/img/programa-pronampe.jpg",  # arte enviada pelo cliente — banner bandeira do Brasil + nome do programa (ver README item 145)
    "programa-procred-360": "assets/img/programa-procred-360.jpg",  # arte enviada pelo cliente — banner bandeira do Brasil + nome do programa (ver README item 145)

    # ---- segunda foto (complementar) na página isolada de cada programa --
    # Painel intermediário da página (mediarow, o mesmo formato usado no
    # bloco de crédito BNDES das páginas de produto de referência), abaixo
    # da tabela de dados — pedido do cliente, para não deixar a página só
    # com a foto do topo.
    "programa-bndes-2":       "assets/img/programa-bndes-2.jpg",  # foto enviada pelo cliente — outro ângulo da sede real do BNDES no Rio de Janeiro
    "programa-peac-fgi-2":    "assets/img/programa-peac-fgi-2.jpg",  # foto pesquisada (Pexels, licença livre) — homem de terno azul lendo/assinando contrato
    "programa-pronampe-2":    "assets/img/programa-pronampe-2.jpg",  # arte enviada pelo cliente — mesmo banner do programa (ver README item 145)
    "programa-procred-360-2": "assets/img/programa-procred-360-2.jpg",  # arte enviada pelo cliente — mesmo banner do programa (ver README item 145)

    # ---- uma foto por artigo do blog (opcional — sem ela, roda a arte SVG) --
    # A chave é sempre "artigo-" + o slug do artigo (o mesmo da URL). Os sete
    # artigos abaixo têm foto própria (a mesma já usada na miniatura e na
    # abertura do corpo do texto — ver content/conteudos.py, campo "image").
    # Os outros treze usam o mesmo placeholder genérico (_PLACEHOLDER_CARRO)
    # do resto do site, até o cliente enviar uma foto específica de cada um.
    "artigo-custo-real-da-divida-rotativo-e-garantia-real": "assets/img/conteudos/custo-real-da-divida-rotativo-e-garantia-real.jpg",
    "artigo-necessidade-de-capital-de-giro":                "assets/img/conteudos/necessidade-de-capital-de-giro.jpg",
    "artigo-auto-equity-prazo-e-depreciacao":               "assets/img/conteudos/auto-equity-prazo-e-depreciacao.jpg",
    "artigo-marco-das-garantias-o-que-mudou":               "assets/img/conteudos/marco-das-garantias-o-que-mudou.jpg",
    "artigo-scd-sep-e-a-natureza-do-credor":                "assets/img/conteudos/scd-sep-e-a-natureza-do-credor.jpg",
    "artigo-construcao-financiada-liberacao-por-medicao":   "assets/img/conteudos/construcao-financiada-liberacao-por-medicao.jpg",
    "artigo-comprar-a-vista-ou-financiar":                  "assets/img/conteudos/comprar-a-vista-ou-financiar.jpg",
    "artigo-como-conseguir-credito-para-a-empresa":                    "assets/img/conteudos/como-conseguir-credito-para-a-empresa.jpg",  # foto pesquisada (Pexels, licença livre) — fachada de banco moderna de vidro
    "artigo-como-calcular-necessidade-de-capital-de-giro":             "assets/img/conteudos/como-calcular-necessidade-de-capital-de-giro.jpg",  # foto pesquisada (Pexels, licença livre) — calculadora e caneta sobre gráfico financeiro
    "artigo-documentos-para-solicitar-credito-empresarial":            "assets/img/conteudos/documentos-para-solicitar-credito-empresarial.jpg",  # foto enviada pelo cliente — mão preenchendo documentos à mesa
    "artigo-pronampe-quem-pode-solicitar":                             "assets/img/conteudos/pronampe-quem-pode-solicitar.jpg",  # arte enviada pelo cliente — banner bandeira do Brasil + nome do programa (ver README item 145/146)
    "artigo-procred-360-publico-e-documentos":                         "assets/img/conteudos/procred-360-publico-e-documentos.jpg",  # arte enviada pelo cliente — banner bandeira do Brasil + nome do programa (ver README item 145/146)
    "artigo-garantia-para-credito-empresarial":                        "assets/img/conteudos/garantia-para-credito-empresarial.jpg",  # foto enviada pelo cliente — mão assinando documento com caneta-tinteiro
    "artigo-bndes-para-empresas-como-funciona":                        "assets/img/conteudos/bndes-para-empresas-como-funciona.jpg",  # foto enviada pelo cliente — sede real do BNDES no Rio de Janeiro
    "artigo-fgi-tradicional-x-fgi-peac":                               "assets/img/conteudos/fgi-tradicional-x-fgi-peac.jpg",  # foto enviada pelo cliente — gráficos impressos ao lado de notebook
    "artigo-capital-de-giro-pronampe-procred-360-ou-bndes":            "assets/img/conteudos/capital-de-giro-pronampe-procred-360-ou-bndes.jpg",  # arte enviada pelo cliente — banner bandeira do Brasil com os 3 programas (ver README item 146)
    "artigo-pedido-de-credito-negado-o-que-fazer":                     "assets/img/conteudos/pedido-de-credito-negado-o-que-fazer.jpg",  # foto enviada pelo cliente — homem preocupado ao notebook
    "artigo-como-comparar-credito-empresarial-pelo-cet":               "assets/img/conteudos/como-comparar-credito-empresarial-pelo-cet.jpg",  # foto enviada pelo cliente — lupa sobre gráficos financeiros impressos
    "artigo-linhas-bndes-capital-de-giro-finame-cartao":               "assets/img/conteudos/linhas-bndes-capital-de-giro-finame-cartao.jpg",  # arte enviada pelo cliente — cartão genérico com o nome "BNDES" (não é o logotipo oficial, ver README item 146)
    "artigo-como-funciona-o-compartilhamento-de-faturamento-no-e-cac": "assets/img/conteudos/como-funciona-o-compartilhamento-de-faturamento-no-e-cac.jpg",  # selo oficial do e-CAC/Receita Federal, autorizado pelo cliente (ver README item 147) — uso informativo, identifica o próprio sistema descrito no artigo

    # ---- cartões de público-alvo na home ("Quem atendemos") --------------
    "card-empresas":       "assets/img/quem-atendemos-empresas.jpg",  # foto real enviada pelo cliente (fachada espelhada, skyline de São Paulo refletido) — ambiente corporativo, sem clichê de aperto de mão
    "card-investidores":   "assets/img/quem-atendemos-investidores.jpg",  # foto real enviada pelo cliente (equipe montando armação de aço numa obra) — sem sorriso de banco de imagem, comunica execução em campo
    "card-patrimonio":     "assets/img/quem-atendemos-patrimonio.jpg",  # foto real enviada pelo cliente (fachada de casa residencial de padrão alto) — o próprio bem imobiliário, sem gente sorrindo com dinheiro
    "card-agro":           "assets/img/quem-atendemos-agro.jpg",  # foto real enviada pelo cliente (colheitadeira em lavoura de trigo) — comunica operação no campo, sem clichê de banco de imagem

    # ---- painéis de imagem + texto (opcional) -----------------------------
    "programas-publicos": "assets/img/programas-publicos.jpg",  # card do simulador na home — foto enviada pelo cliente (licença livre) — profissional analisando planilha no notebook e calculadora, com bandeira do Brasil na mesa

    # ---- imagens ao lado de texto na home (opcional) -----------------------
    # Cada uma amarrada a um trecho específico, não um respiro qualquer entre
    # seções: sem foto, cai para uma arte institucional no lugar, então a
    # home nunca fica com buraco vazio. Mesma regra do topo do arquivo:
    # nunca aperto de mão, gente sorrindo com dinheiro ou banco de imagem
    # genérico — o que comunica aqui é método e organização, não simpatia.
    "home-estrutura":    "assets/img/posicionamento-estrutura.jpg",  # ao lado do texto de "Posicionamento" — foto real enviada pelo cliente (reunião de trabalho, notebook aberto na mesa): a conversa técnica antes da estrutura
    "home-diagnostico":  "assets/img/metodologia-diagnostico.jpg",  # ao lado dos 4 passos de "Metodologia" — foto real enviada pelo cliente (reunião de trabalho lendo um fluxo de processo num flip chart, notebook em primeiro plano): comunica método e estrutura sem clichê de banco de imagem
}

# Vídeos do YouTube em /conteudos, sobre o mercado de crédito estruturado
# internacional (não conteúdo local, para trazer uma referência que o site
# ainda não tem). Vazio por padrão: enquanto ficar assim, a seção inteira não
# é publicada — nada de placeholder inventado no lugar de um vídeo real.
#
# Para adicionar um vídeo, copie o bloco abaixo e preencha:
#   "youtube_id": o código de 11 caracteres da URL do YouTube
#                  (em youtube.com/watch?v=XXXXXXXXXXX, é o XXXXXXXXXXX)
#   "titulo":      título do vídeo, como aparece no YouTube
#   "canal":       nome do canal
#   "assunto":     uma frase curta de contexto (por que vale assistir)
# A miniatura vem direto do YouTube (i.ytimg.com); o card só linka para o
# vídeo, sem player embutido — o site continua sem terceiros rodando nele.
#
# Ex.:
# VIDEOS = [
#     {"youtube_id": "dQw4w9WgXcQ",
#      "titulo": "How Working Capital Financing Actually Works",
#      "canal": "Corporate Finance Institute",
#      "assunto": "Panorama internacional sobre estruturas de capital de giro."},
# ]
VIDEOS = []

# Instituições citadas na faixa "Rede", na home, para dar concretude ao
# "mais de 74 instituições". Cada item com "logo" mostra a marca (arquivo em
# static/assets/img/partners/<logo>.webp, recortada e comprimida a partir do
# material oficial); sem "logo", entra só o nome em texto — caso das duas
# categorias genéricas, que não representam uma instituição específica.
# w/h são as dimensões REAIS do arquivo — importa manter batendo com o
# arquivo de verdade (é o que reserva o espaço certo no layout, ver
# partners()); os arquivos foram redimensionados para 64px de altura (a
# tela mostra a 28px, então ~2,3x já cobre retina com folga, sem carregar
# 140px de altura à toa — auditoria de performance apontou ~79KB
# desperdiçados nos 12 logos por causa disso).
PARTNERS = [
    {"name": "Banco do Brasil", "logo": "banco-do-brasil", "w": 64, "h": 64},
    {"name": "Caixa Econômica Federal", "logo": "caixa", "w": 92, "h": 64},
    {"name": "Itaú", "logo": "itau", "w": 64, "h": 64},
    {"name": "Bradesco", "logo": "bradesco", "w": 77, "h": 64},
    {"name": "Santander", "logo": "santander", "w": 368, "h": 64},
    {"name": "BTG Pactual", "logo": "btg-pactual", "w": 161, "h": 64},
    {"name": "Banco BV", "logo": "bv", "w": 92, "h": 64},
    {"name": "BNDES", "logo": "bndes", "w": 312, "h": 64},
    {"name": "BDMG", "logo": "bdmg", "w": 138, "h": 64},
    {"name": "Banco Daycoval", "logo": "banco-daycoval", "w": 417, "h": 64},
    {"name": "Sicoob", "logo": "sicoob", "w": 287, "h": 64},
    {"name": "Sicredi", "logo": "sicredi", "w": 272, "h": 64},
    {"name": "Fintechs"},
    {"name": "Fundos de investimento"},
]


def _fmt_phone(digits):
    """5531999998888 -> (31) 99999-8888"""
    if not digits:
        return None
    d = "".join(c for c in str(digits) if c.isdigit())
    if d.startswith("55") and len(d) > 11:
        d = d[2:]
    if len(d) == 11:
        return f"({d[:2]}) {d[2:7]}-{d[7:]}"
    if len(d) == 10:
        return f"({d[:2]}) {d[2:6]}-{d[6:]}"
    return str(digits)


_wa = CONTATO["whatsapp"]
_tel = CONTATO["telefone"]

# Mensagem enviada junto do redirecionamento ao WhatsApp logo após o envio
# dos formulários de captação (modal de lead e /contato). Ver `leadmodal()`
# e `contato.form()` em build.py / content/contato.py, e o handler
# `form[data-endpoint-form]` em site.js.
WHATSAPP_LEAD_MSG = ("Oi, estou buscando capital de giro para minha empresa e "
                      "quero entender como vocês podem ajudar.")

import urllib.parse as _urlparse

SITE = {
    "name": "Acrópole Capital",
    "domain": "https://www.acropolecapital.com.br",
    "cnpj": "67.311.470/0001-47",
    "tagline": "Estruturação de crédito e operações financeiras para empresas, patrimônio e projetos.",

    "whatsapp_label": _fmt_phone(_wa),
    "whatsapp_href": f"https://wa.me/{''.join(c for c in str(_wa) if c.isdigit())}" if _wa else None,
    "whatsapp_lead_href": (f"https://wa.me/{''.join(c for c in str(_wa) if c.isdigit())}"
                            f"?text={_urlparse.quote(WHATSAPP_LEAD_MSG)}") if _wa else None,
    "phone_label": _fmt_phone(_tel),
    "phone_href": f"tel:{_tel}" if _tel else None,
    "email": CONTATO["email"],
    "address": CONTATO["endereco"],
    "hours": CONTATO["horario"],
    "linkedin": CONTATO["linkedin"],
    "instagram": CONTATO["instagram"],
    "youtube": CONTATO["youtube"],
}

# Rótulo mostrado quando o dado ainda não foi preenchido.
PENDENTE = {
    "whatsapp_label": "WhatsApp a definir",
    "phone_label": "Telefone a definir",
    "email": "E-mail a definir",
    "address": "Endereço a definir",
    "hours": "Horário a definir",
}

# Opções dos formulários de contato (página /contato e popup de captação).
CARGOS = ["Sócio ou Fundador", "Presidente ou CEO", "Vice-presidente ou C-Level",
          "Diretor", "Gerente", "Coordenador", "Supervisor", "Analista"]

PORTES = ["MEI", "Microempresa (ME)", "Pequena empresa (EPP)", "Média empresa", "Grande empresa"]

FATURAMENTOS = [
    "Ainda não faturamos", "Até R$ 250 mil ao ano", "De R$ 250 mil a R$ 500 mil ao ano",
    "De R$ 500 mil a R$ 1 milhão ao ano", "De R$ 1 milhão a R$ 5 milhões ao ano",
    "De R$ 5 a R$ 10 milhões ao ano", "De R$ 10 a R$ 50 milhões ao ano",
    "De R$ 50 a R$ 500 milhões ao ano", "Acima de R$ 500 milhões",
]

# Perguntas de qualificação do lead, além dos dados de identificação e porte
# acima. Cada uma existe para triar a solicitação antes do primeiro contato,
# não para parecer formulário de banco — por isso ficam com poucas opções e
# sempre com uma saída de "não sei" quando cabe.
RESTRICAO = ["Não", "Sim", "Não sei dizer"]

VALORES_BUSCADOS = [
    "Até R$ 100 mil", "De R$ 100 mil a R$ 500 mil", "De R$ 500 mil a R$ 1 milhão",
    "De R$ 1 milhão a R$ 5 milhões", "Acima de R$ 5 milhões", "Ainda não sei dimensionar",
]

URGENCIAS = [
    "Em até 30 dias", "Nos próximos 3 meses", "Ainda em planejamento, sem prazo definido",
]

ORIGENS = [
    "Indicação", "Google ou busca", "LinkedIn", "Instagram", "Já era cliente ou contato próximo", "Outro",
]

# Fatos institucionais verificados a partir do material da empresa.
FACTS = [
    ("74+", "Instituições financeiras na rede, no Brasil e no exterior"),
    ("5 países", "Rede ativa fora do Brasil: Inglaterra, Portugal, Suíça, Estados Unidos e Emirados Árabes Unidos"),
    ("R$ 500 mil", "Ticket mínimo das operações corporativas estruturadas"),
    ("Braço próprio", "Estrutura financeira própria, além da rede de parceiros"),
]

SOLUTIONS = [
    {
        "slug": "capital-de-giro",
        "image": "assets/img/solucao-capital-de-giro.jpg",
        "title": "Capital de Giro",
        "kicker": "Crédito PJ",
        "menu": "Liquidez dimensionada pelo ciclo de caixa, não pela urgência.",
        "short": "Linha estruturada para financiar a distância entre pagar fornecedores e receber de clientes.",
        "chips": ["Recebíveis e garantias reais", "Pronampe · PEAC FGI", "Prazo aderente ao ciclo"],
        "art": "flux",
    },
    {
        "slug": "home-equity",
        "image": "assets/img/solucao-home-equity.jpg",
        "title": "Home Equity",
        "kicker": "Garantia de imóvel",
        "menu": "Liquidez com o imóvel que já é seu, mantendo posse e uso.",
        "short": "Crédito com garantia imobiliária, sob alienação fiduciária, para quem tem patrimônio parado.",
        "chips": ["Lei nº 9.514/1997", "LTV conservador", "Prazos longos"],
        "art": "elevation",
    },
    {
        "slug": "auto-equity",
        "image": "assets/img/solucao-auto-equity.jpg",
        "title": "Auto Equity",
        "kicker": "Garantia de veículo",
        "menu": "Liquidez rápida sobre um ativo que deprecia. Prazo é a variável crítica.",
        "short": "Crédito com garantia de veículo quitado ou com margem, avaliado contra a curva de depreciação.",
        "chips": ["Lei nº 4.728/1965", "Gravame no Detran", "Prazo curto e médio"],
        "art": "chassis",
    },
    {
        "slug": "credito-pj",
        "image": "assets/img/solucao-credito-pj.jpg",
        "title": "Crédito PJ",
        "kicker": "Pessoa jurídica",
        "menu": "A escolha do parceiro pesa tanto quanto a taxa anunciada.",
        "short": "Comparação estrutural entre instituições, naturezas jurídicas e mecanismos públicos de garantia.",
        "chips": ["SCD e SEP", "Procred 360", "Comparação por CET"],
        "art": "matrix",
    },
    {
        "slug": "estruturacao-de-credito",
        "image": "assets/img/solucao-estruturacao-de-credito.jpg",
        "title": "Estruturação de Crédito",
        "kicker": "Operações desenhadas",
        "menu": "Quando nenhuma linha de prateleira resolve, a operação é desenhada.",
        "short": "Desenho de operações sob medida: múltiplas fontes, garantias combinadas e cronograma próprio.",
        "chips": ["Rede de 74+ instituições", "Funding nacional e externo", "Garantias combinadas"],
        "art": "layers",
    },
    {
        "slug": "financiamento",
        "image": "assets/img/solucao-financiamento.jpg",
        "title": "Financiamento",
        "kicker": "Aquisição e obra",
        "menu": "Preservar caixa próprio em vez de imobilizá-lo por inteiro.",
        "short": "Financiamento habitacional e produtivo, com liberação vinculada a etapa e cronograma.",
        "chips": ["SFH e recursos de mercado", "Liberação por etapa", "Prazos longos"],
        "art": "grid",
    },
    {
        "slug": "aquisicao-e-construcao",
        "image": "assets/img/solucao-aquisicao-e-construcao.jpg",
        "title": "Aquisição e Construção",
        "kicker": "Imobiliário",
        "menu": "Terreno, obra e cronograma tratados como uma operação só.",
        "short": "Estruturação para aquisição de terreno, incorporação, obra e expansão de ativos produtivos.",
        "chips": ["Contrato único terreno + obra", "Cronograma físico-financeiro", "ART/RRT obrigatória"],
        "art": "plan",
    },
    {
        "slug": "mercado-de-capitais",
        "image": "assets/img/solucao-mercado-de-capitais.jpg",
        "title": "Recebíveis e Mercado de Capitais",
        "kicker": "Antecipação e emissão",
        "menu": "Recebível antecipado ou convertido em título, conforme o que a operação pede.",
        "short": "Antecipação de recebíveis, CRI, CRA e emissão de debêntures para acesso direto a investidores.",
        "chips": ["Antecipação de recebíveis", "CRI, CRA e debêntures", "Acesso a investidores institucionais"],
        "art": "securitize",
    },
]

SOL_BY_SLUG = {s["slug"]: s for s in SOLUTIONS}

# Os 4 programas públicos de content/programas.py (nome, âncora na página,
# descrição de uma linha para o painel do menu). Mantido aqui, e não
# importado de content/programas.py, porque programas.py já importa build.py
# — importar programas.py de volta em build.py criaria um ciclo. Se um
# programa for adicionado, renomeado ou tiver a âncora alterada em
# programas.py, replicar aqui.
PUBLIC_PROGRAMS = [
    {"slug": "bndes", "title": "BNDES", "menu": "Banco de fomento por trás de linhas de repasse como Finame, Finem e Cartão BNDES."},
    {"slug": "peac-fgi", "title": "PEAC FGI", "menu": "Fundo que garante parte da operação junto ao banco, reduzindo a exigência de garantia real."},
    {"slug": "pronampe", "title": "Pronampe", "menu": "Capital de giro com garantia do FGO, para empresas de faturamento menor."},
    {"slug": "procred-360", "title": "Procred 360", "menu": "Taxa entre as mais baixas dos programas públicos, com concessão apoiada em dados já declarados à Receita."},
]

# Navegação principal. Cada item aponta para uma página real. "mega" marca
# os itens que abrem um painel com mais opções ao passar o mouse (ou tocar,
# no menu mobile) — "solucoes" lista as 8 soluções, "programas" lista os 4
# programas públicos.
# Item 134: de volta a 6 itens (pedido do cliente) — os 4 essenciais mais
# "Como funciona" e "Sobre", as duas páginas do rodapé (coluna
# "Institucional") que ele considerou importantes o bastante para não
# ficar só lá embaixo. As demais da mesma coluna (Diagnóstico rápido,
# Calculadora de capital de giro, Para empresas, Para investidores, Para
# o agronegócio, Governança) continuam só no rodapé — critério do filtro:
# "Como funciona" resolve a maior objeção de quem chega desconfiado do
# processo, e "Sobre" é o item de credibilidade institucional que todo
# site financeiro sério tem no menu principal; o resto já é atendido
# pelos painéis de Soluções/Programas ou é específico demais de um
# público para entrar no primeiro nível. Nenhuma página saiu do site nem
# perdeu link interno, só mudou de onde é alcançável em um clique.
NAV = [
    {"label": "Soluções", "href": "solucoes.html", "mega": "solucoes"},
    {"label": "Programas", "href": "programas.html", "mega": "programas"},
    {"label": "Como funciona", "href": "como-funciona.html"},
    {"label": "Sobre", "href": "sobre.html"},
    {"label": "Conteúdos", "href": "conteudos.html"},
    {"label": "Contato", "href": "contato.html"},
]

CATEGORIES = [
    "Capital de Giro",
    "Home Equity",
    "Auto Equity",
    "Crédito PJ",
    "Imóveis",
    "Construção",
    "Estratégia Financeira",
    "Programas Públicos",
    "Garantias",
]

LEGAL_LINE = (
    "Acrópole Capital atua na assessoria e estruturação de operações de crédito. "
    "Não somos instituição financeira e não concedemos crédito diretamente. "
    "Toda operação está sujeita à análise, aos critérios e à decisão final da instituição financeira responsável. "
    "Nenhuma informação deste site constitui oferta, proposta firme, recomendação de investimento ou promessa de aprovação."
)

# Mesmo aviso, em dois pontos do site (página institucional "Empresas" e a
# página de solução Crédito PJ) — texto de compliance, então mantido como
# constante única em vez de copiado, pra uma correção de redação só precisar
# acontecer num lugar.
CONDITIONS_NOTICE = (
    "Condições, taxas, prazos e limites variam por instituição financeira e por perfil de crédito, "
    "e estão sujeitos a análise. Nenhuma informação desta página constitui oferta ou promessa de aprovação."
)
