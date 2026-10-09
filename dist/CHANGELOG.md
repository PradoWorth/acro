# Acrópole Capital: histórico de versões

Regra: a numeração só avança com autorização de Lucas Prado. Mudanças pequenas e correções: 1.0.x. Novas páginas ou funções: 1.x. Mudanças estruturais: 2.0.

## 1.2 (9 out 2026)
Auditoria completa: segurança, design system, responsividade, acessibilidade, performance, SEO e conteúdo. Nenhuma URL mudou.
- Segurança: pastas ocultas (.git) e PHP bloqueados; home protegida contra index.php de outra instalação (DirectoryIndex); HTML sempre revalidado e CSS/JS com cache de 1 ano por hash.
- Formulários: webhook de produção do n8n; sem "sucesso" quando o envio falha ou o endpoint não existe; erro com link direto para o WhatsApp; leads das páginas novas com a origem correta.
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
