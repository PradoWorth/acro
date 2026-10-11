# Acrópole Capital: histórico de versões

Regra: a numeração só avança com autorização de Lucas Prado. Mudanças pequenas e correções: 1.0.x. Novas páginas ou funções: 1.x. Mudanças estruturais: 2.0.

## 1.2 (9 out 2026)
Auditoria completa: segurança, design system, responsividade, acessibilidade, performance, SEO e conteúdo. Nenhuma URL mudou.
- Segurança: pastas ocultas (.git) e PHP bloqueados; home protegida contra index.php de outra instalação (DirectoryIndex); HTML sempre revalidado e CSS/JS com cache de 1 ano por hash.
- Formulários: webhook de produção do n8n; sem "sucesso" quando o envio falha ou o endpoint não existe; erro com link direto para o WhatsApp; leads das páginas novas com a origem correta.
- Desempenho (TBT): o globo da home inicia logo após a primeira pintura (os demais, 2,5 s depois) e o aviso de cookies não força recálculo de layout na abertura.
- Rota do tema Home Equity mudou de /home-equity para /emprestimo-home-equity (15 páginas), com redirecionamento 301 das URLs antigas, para não conflitar com a pasta antiga da Hostinger.
- Auditoria completa: página 404 com caminhos absolutos (não perde o estilo em URLs profundas), máscara de moeda do simulador em reais inteiros (digitar 800000 vira R$ 800.000), foco no diálogo em telas de toque, landmarks de acessibilidade, favicon.svg leve, descrição do hub encurtada.
- Botão "Fazer a simulação" corrigido (rolagem suave não briga mais com o clique), bloco de simulação com contraste escuro, botão "Simular em 2 minutos" no topo das páginas, espaçamentos finos no celular.
- Desempenho: globo da home pausa quando sai da tela (antes o do topo animava o tempo todo) e começa a 30 fps em telas de toque.
- Google Analytics 4 (G-RZEN0FRQGB): carrega só após o aceite de cookies; eventos de WhatsApp, CTA e formulário enviados ao GA4; CSP e política de privacidade atualizadas.
- LGPD: aviso de cookies com Aceitar e Recusar, cookie de campanha só após aceite, Consent Mode v2 no GTM do simulador, "Preferências de cookies" no rodapé, política de privacidade atualizada, newsletter com finalidade explícita.
- Simulador: JS de 551 KB para 85 KB (cidades vindas do JSON local, fotos como arquivos), tokens do site (cores, Inter e Manrope, botões em pílula), contraste AA, Esc fecha a janela, textos sem promessa.
- Design e responsividade: card "Outros canais" (/contato), rodapé entre 900 e 1199 px, formulários em 320 px, e-mail cortado em 320 px, tabelas viram cartões no celular, índice fixo nos guias, uma foto por grupo de páginas, rótulos de botão padronizados.
- Acessibilidade: foco entra na gaveta do celular ao abrir; janela do simulador com foco preso; área de toque mínima de 24 px.
- SEO: títulos das páginas legais, links do logo e do "Início" nas páginas-pilar, imagem nos dados estruturados de artigo, títulos longos encurtados.
- Conteúdo: prazo de retorno com horário de atendimento, precisão sobre alienação fiduciária, endereço padronizado.
- Performance: globo da home 15% menor, sem perda visual.
- Ajustes finos: 36 páginas com `</div>` sobrando que fechava o artigo antes da hora (tabelas comparativas e quadro de adequação), âncora duplicada em taxas-juros-e-cet. Etapa 2 do quadro da home passou a "Diagnóstico". Telefone colado com +55 (formulários e simulador) agora vira o número certo em vez de cortar os últimos dígitos. Removido o bloco "Fontes e referências" de 122 páginas (366 links externos para planalto.gov.br e bcb.gov.br): o visitante não sai do site. Simulador: removida a "renda mínima recomendada" da tela de resultado, da mensagem do WhatsApp e do envio ao CRM. Prévia em HTML único: voltaram as estrelas do globo, a mãozinha do quadro, as animações de entrada e as calculadoras (scripts que o gerador da prévia descartava).; simulador: parcela "até 20 anos" e taxa "a partir de 1,19% a.m. mais IPCA" (linha Taxa no resultado, aviso e mensagem do WhatsApp); nova página principal de Home Equity (/home-equity-acropole) com menu próprio, simulador, formulário, dúvidas e guias, ligada pelo rodapé e pelo sitemap; cidades: removidas Uberaba, Uberlândia, Ribeirão Preto, São José do Rio Preto e interior de Minas; novas Rio de Janeiro, Curitiba, Porto Alegre, Florianópolis, Londrina, Maringá, Fortaleza e Balneário Camboriú (população IBGE Censo 2022); todos os formulários e o simulador enviam o campo `notas` (bloco de texto com todos os dados do lead) para o n8n; calculadora ou simulador (Home Equity, capital de giro ou programas públicos) em todas as páginas relevantes, 106 geradas, 24 artigos e 9 institucionais; página inteira de simulação (/simular-home-equity) com simulador embutido, e botões "Fazer a simulação" do site levando a ela

## 1.1 (9 out 2026)
- Simulador Home Equity integrado: página própria em /simulador-home-equity e botão que o abre em janela dentro de 10 páginas (valor, margem, passo a passo e faixas de crédito).
- Simulador: população dos municípios agora vem da base local (IBGE, Censo 2022), sem depender de APIs externas; fonte Manrope própria; WhatsApp abre na janela principal.
- Correção no simulador: a mensagem de erro do valor desejado vazio era a do valor do imóvel; agora fala do crédito desejado.
- CSP: página do simulador com política própria (servidor de tags da Acrópole e n8n); demais páginas passam a aceitar janela do mesmo domínio (frame-src 'self').

## 1.0 (8 out 2026)
Primeira versão numerada do site.
- 179 páginas: 57 anteriores e 122 novas (10 grupos de conteúdo sobre Home Equity e crédito com garantia de imóvel, com 2 páginas-hub).
- Verificador de cidade em /cidades, com lista oficial de municípios (IBGE, Censo 2022), formulário e envio para o WhatsApp.
- Ajustes de responsividade: colunas e tabelas não estouram mais a largura no celular; menu em modo compacto abaixo de 1000 px.
- Caixa "Fatos-chave" nas páginas novas, eventos de análise (dataLayer), proteção anti-robô nos formulários.
- Segurança: cabeçalhos, CSP por hash, bloqueio de arquivos sensíveis e de injeção por URL.
- Formularios: campos sozinhos na linha agora ocupam a largura toda (Pronampe e 24 paginas); removido bloco de simulacao duplicado logo apos o CTA em Pronampe, Agronegocio e Credito empresarial SP.
- Globo: contornos dos paises com todos os pontos (antes 1 a cada 4); custo de renderizacao medido igual.
- Cards 'Aprofunde' em artigos: 2 colunas no desktop (antes 3, apertado ao lado do indice).
- Simulador: cards de opcao atualizam so o estado ao selecionar (imagens nao sao recriadas), corrigindo o piscar no celular.
- Menu: item Simulador (desktop, painel Solucoes, gaveta) e bloco na home; menu desktop so a partir de 1120px.
- Simulador: retomar de onde parou (7 dias, sem dados de contato); lead parcial enviado ao informar o WhatsApp (etapa=parcial, leadId); aviso de consentimento; politica atualizada.
- Prova social (4,9, RA1000, 74+) em Contato, Pronampe e Simular Home Equity.
- Formularios: validacao ao vivo apos o primeiro blur, indicador de campo valido, autocomplete.
- Barra de cookies compacta no celular.
- CRM: simulador envia name/phone/valor formatado (R$ 2.000.000), valor_numerico, campos *Formatado e titulo pronto; campo valor das landings com mascara de moeda e valor_numerico no envio.
- Home: bloco do simulador Home Equity movido para logo apos a lista de Solucoes.
- Prova social centralizada.
- Botoes de simulacao Home Equity (home, simbands, topo das paginas, painel Solucoes) abrem o simulador em pop-up (data-sim-open), com link normal como fallback.
- Pop-up do simulador com fundo desfocado (igual ao modal de contato); clique fora fecha.
- Home: card avulso de Home Equity substituído por seção completa (#home-equity) com imagem, benefícios, 3 passos e CTA que abre o simulador em pop-up.
- Home: imagem do Home Equity fica acima do texto no mobile/tablet e à esquerda no desktop.
- Home: seção Home Equity com imagem no topo (mobile) e título/tag junto ao texto, padrão do bloco Simulador gratuito.
- Política de privacidade: CRM citado entre fornecedores, transferência internacional (Google, Vercel, WhatsApp) e dados de terceiros informados em formulários.
- Campos validos: destaque verde e check somem ao sair do campo, sem animacao.
- Pronampe: mais espaco entre a imagem e o texto na secao O custo invisivel.
- Faixa de anuncio fixa acima do menu em todas as paginas (pergunta curta no mobile, texto longo no desktop, botao Simular que abre o simulador em pop-up); como-funciona recebeu o item Simulador e o pop-up que faltavam.
- Faixa de anuncio: botao Simular em verde escuro discreto, para nao competir com o botao do menu.
- Faixa de anuncio: evento announcement_click no GA4, texto desktop com sem consulta a bureau de credito e, no celular, a faixa sobe suavemente ao chegar na secao dos bancos (ou apos a primeira tela nas demais paginas).
- Home: icones dos cards Objetivo, Estrutura, Patrimonio e garantias e Capacidade e risco redesenhados (traco 2, circulo verde claro, maiores), no padrao do Pronampe.
- Faixa de anuncio com texto minimo (desktop e mobile) e card Home Equity no menu lateral do celular, que abre o simulador em pop-up.
- Faixa no celular: animacao de subida com efeito elastico (transform, mola) e retorno suave; respeita reduzir movimento.
- Home, Posicionamento: enquadramento da foto ajustado para mostrar o rosto no tablet.
- Tipografia padronizada: escala reduzida (corpo 17, destaque 19, texto 15, meta 14, legenda 13, micro 12; titulos 28/24/19 no celular e 40/32/20 no desktop) e tamanhos soltos migrados para os tokens. Titulo do hero preservado.
- Menu lateral mobile: card sem o rotulo Home Equity e botao Simular em verde escuro, para nao competir com Solicitar analise.
- Menu lateral mobile: o card Home Equity alterna 4 mensagens (pergunta, taxa a partir de, prazo, sem bureau) com efeito de virar a caixinha a cada 3 segundos.
- Faixa de anuncio: 4 mensagens viram a cada 3 segundos (pergunta, taxa a partir de 1,19% + IPCA, prazo e uso do imovel, sem bureau), botao Simular fixo.
- Faixa e card do menu: troca de mensagens com deslize vertical e fade (no lugar da virada 3D), a cada 4 segundos, com pausa ao passar o mouse, focar ou tocar na faixa.
- Conversao: botao da faixa com preenchimento mais claro e seta; seo-events.js em todas as paginas (cta_click, form_start, generate_lead); evento simulator_open com a origem (faixa, menu, secao_home, etc.).
- Menu: linha fina na base do menu, no mesmo estilo da linha acima dos numeros do hero.
- Soluções (home): painel lateral fixo abaixo do menu com barra (top com --bar-h) e altura mínima estável ao passar o mouse.
- Menu mobile: card do simulador movido para o topo do painel, acima da logo, com o mesmo visual da barra de anúncio (fundo verde, texto branco, botão).
- Soluções (home): lista 01 a 08 em loop infinito com a roda do mouse (desktop); ao tirar o mouse da lista a página volta a rolar.
- Home (hero): altura fluida por viewport (svh) para que título, texto, botões e faixa de números caibam inteiros na primeira tela em desktop.
- Barras de rolagem (página, menu mobile e áreas internas) no padrão visual do site.
- Soluções (mobile): removida lacuna acima do painel (offset sticky aplicado só no desktop).
- Soluções (desktop): tela trava ao chegar na seção (alinha abaixo do menu), roda do mouse gira a lista em loop com animação contínua; mouse fora da seção libera a rolagem. Painel compacto em telas baixas.
- Soluções (desktop): diagrama preenche o quadro sem lacunas laterais; coluna do painel se ajusta à altura da janela.
- Soluções (desktop): trava volta a funcionar em todas as entradas, descendo ou subindo, quantas vezes a pessoa sair e voltar.
- Soluções (desktop): colunas equilibradas; diagrama do painel preenche o quadro (recorte leve) e o painel cabe na tela.
- Barra de anúncio: botão removido, ação 'Simular agora →' em texto e barra mais baixa (2,25rem), no card do menu mobile também.
