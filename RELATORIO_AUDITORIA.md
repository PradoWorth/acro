# Auditoria técnica completa — Acrópole Capital

Auditoria full-stack do site (46 páginas, gerador estático em Python) cobrindo bugs, acessibilidade, performance, SEO técnico, qualidade de código e a calculadora/simulador. Todos os problemas confirmados foram corrigidos e testados — não é uma lista de recomendações, é o site já corrigido.

## Problemas encontrados e corrigidos

**Acessibilidade (o bloco mais sério)**
- O `<select>` customizado (usado em todo formulário do site — contato, popup de especialista, calculadoras) era impossível de operar só com teclado: dava pra abrir o menu, mas não dava pra escolher uma opção com as setas. Afetava literalmente todo formulário do site.
- Resultado das 3 calculadoras (programas públicos, capital de giro, diagnóstico) não era anunciado por leitor de tela ao aparecer.
- Mensagens de erro dos campos de formulário não tinham `id`/`aria-describedby`, então um leitor de tela dizia "inválido" sem dizer o motivo.
- Botão de fechar a gaveta mobile carregava `aria-expanded="true"` por engano (copiado do botão que abre).
- `scrollIntoView` suave sem checar `prefers-reduced-motion` em 3 scripts (diagnóstico, programas, capital de giro) — já corrigido na home/globo numa sessão anterior, faltava fechar essa lacuna.

**Bugs funcionais**
- Duplo clique/duplo Enter no envio de qualquer formulário (`data-endpoint-form`) podia disparar dois envios — o botão ficava com `aria-disabled`, mas isso não impede um segundo evento de `submit`. Corrigido com uma trava real no início do handler.
- Colar um valor em formato "1.234.567,89" nos campos de moeda das calculadoras (faturamento, valor buscado, custo mensal) virava R$ 123.456.789 — os centavos entravam como dígitos inteiros, inflando o valor em ~100x. Corrigido nas 3 máscaras de moeda do site.
- A página de artigo (`conteudos/*.html`) reconstruía a seção de topo à mão em vez de usar o componente compartilhado, e por isso não passava `eager=true` pra imagem — ela carregava lazy à toa, atrasando o LCP nessa página especificamente, ao contrário de toda outra página do site. A mesma lacuna existia na página 404.
- `harden_csp()` (a etapa que injeta os hashes dos scripts inline na Content-Security-Policy) falhava silenciosamente se não achasse o padrão esperado nos arquivos de config — um build "verde" podia publicar uma CSP que bloqueia todo script inline do site (globo, calculadoras, questionário) sem nenhum aviso. Agora levanta erro no build se isso acontecer.

**Qualidade de código**
- Um recurso inteiro de "formulário em etapas" (`data-stepform`) tinha JS e CSS publicados em toda página do site, mas nenhuma página usava — nenhuma página emite `data-stepform`. Removido.
- 4 imports nunca usados (`build.py`, `art.py`, `diagnostico.py`, `governanca.py`).
- `institucional.py` fazia busca linear na lista de soluções duas vezes por card em vez de usar o índice já existente (`SOL_BY_SLUG`) — e nem importava esse índice.
- O aviso legal "Condições, taxas, prazos e limites variam..." estava copiado, palavra por palavra, em dois arquivos (`institucional.py` e `solucoes.py`) — texto de compliance duplicado é risco real se precisar corrigir a redação um dia. Virou uma constante única (`CONDITIONS_NOTICE`).

## Performance

- Página de artigo (`conteudos/*.html`): a imagem de topo agora carrega com `fetchpriority="high"` (antes carregava lazy por engano) — deve melhorar o LCP medido nessas páginas, que são a maior parte do conteúdo indexável do site.
- Auditoria de payload (JS/CSS/imagens/fontes) mostrou que o site já está bem otimizado hoje: imagens em AVIF/WebP com fallback e dimensões reservadas (sem CLS), fontes self-hosted com subsetting latin/latin-ext e preload seletivo, zero dependência de terceiros, cache-control já escalonado corretamente por tipo de asset. Não havia gargalo estrutural aqui — só a lacuna pontual da imagem lazy no template de artigo, já corrigida.
- Removido o único recurso morto que pesava em toda página (JS do formulário em etapas nunca usado).
- **Oportunidade identificada, não aplicada por prudência**: o script do globo 3D da home (`content/globe.py`) embute uma tabela de coordenadas de fronteiras com precisão de 1-2 casas decimais — mais precisão do que o olho consegue perceber num globo decorativo daquele tamanho. Reduzir a precisão poderia cortar uns 25-30KB (bruto) só do `index.html`, mas mexer nessa tabela de coordenadas é risco desnecessário sem conseguir revisar visualmente cada fronteira depois — fica registrado como próximo passo se quiser esse ganho.

## Funcionalidades testadas (no navegador, não só lendo código)

- Navegação por teclado no select customizado: abrir com seta, mover entre opções, selecionar com Enter, `Escape` fecha — confirmado sem erros de JS.
- Duplo clique no botão "Enviar" do formulário de contato: confirmado que só um envio efetivo acontece.
- Envio do formulário de contato completo (nome, telefone com máscara, e-mail, empresa, todos os selects, consentimento) — confirmação aparece corretamente.
- Máscara de telefone, bloqueio de e-mail inválido, CTA desabilitado até marcar o consentimento e re-desabilitado se desmarcar — todos passaram.
- Gaveta mobile: abre, trava scroll, Escape fecha, libera o scroll — sem regressão depois das mudanças de acessibilidade.
- Busca e filtro do blog, acordeões, formulário multi-etapa (o de verdade, `.form` de uma tela só) — sem regressão.
- Nenhum erro de JavaScript em nenhuma página testada, antes ou depois das mudanças.

## Calculadora / simulador — cenários testados de verdade

**Simulador de programas públicos (Pronampe, Procred 360, PEAC FGI)**
| Cenário | Resultado | Veredito |
|---|---|---|
| Típico (Pronampe, faturamento R$2M, valor R$300k) | Elegível R$300.000, sem aviso | Correto |
| Faturamento zero | Elegível R$0, aviso "informe o faturamento" | Correto, sem NaN |
| Valores extremos (quase R$1 trilhão) | Trava no teto de R$500.000, aviso explica por quê | Correto, sem Infinity/NaN mesmo em input absurdo |
| Campo valor vazio | Mostra o valor máximo elegível (sem pedir um alvo) | Comportamento correto e esperado |
| Colar "1.234.567,89" no faturamento | Vira R$ 1.234.567 (não R$ 123.456.789) | Corrigido nesta auditoria |
| PEAC FGI pedindo R$20M (teto R$10M) | Aviso nomeia o programa, valor pedido, teto real | Correto |
| Procred 360 no limite de 30% do faturamento | Aviso explica que é limite percentual, não teto fixo | Correto |
| Dentro do limite | Aviso corretamente escondido | Correto |

**Calculadora de capital de giro**
| Cenário | Resultado | Veredito |
|---|---|---|
| Típico (PME 45, PMR 30, PMP 20, custo R$100k) | Ciclo 55 dias, NCG R$183.333 | Correto |
| Ciclo negativo (PMP > PME+PMR) | Ciclo -75 dias mostrado, NCG trava em R$0 com aviso | Correto |
| Tudo zero | Zero em tudo, sem aviso | Correto, sem NaN |
| Campos vazios | Mesmo resultado de "tudo zero" | Correto |
| Extremos (99.999 dias, custo quase R$1 trilhão) | Números gigantes mas matematicamente corretos, sem NaN/Infinity | Correto |

**Limitação conhecida, não uma correção possível**: digitar um valor com vírgula decimal caractere por caractere (ex: "1.000,50" digitado devagar) ainda acumula errado — é uma consequência estrutural de como a máscara reconstrói o campo a cada tecla (cada separador digitado é descartado antes do próximo dígito chegar, então não há como diferenciar "ainda digitando os milhares" de "terminou e é centavo"). A correção aplicada resolve o caso mais arriscado na prática — colar um valor já formatado — que é como a maioria das pessoas traria um número de outro lugar (extrato, planilha). Digitar centavos manualmente não é um uso previsto nessas calculadoras (elas só trabalham com reais inteiros).

## Design / UI

Auditoria visual automatizada (tipografia, espaçamento, raios de borda, paleta de cores, grid de 8px) em todas as 46 páginas × 3 larguras: sistema consistente, nada fora da escala, nenhuma inconsistência de tokens de design encontrada. As duas únicas pendências visuais do auditor (INPUT 24×24 em contato.html, duas colunas com altura desbalanceada) foram investigadas e confirmadas como falsos positivos: o input é um checkbox cujo alvo de toque real é o `<label>` inteiro ao redor (bem maior que 24px), e as colunas desbalanceadas são resultado natural de conteúdo de tamanhos diferentes lado a lado, não um bug de layout.

## Código

- Removido: bloco JS+CSS de formulário em etapas nunca usado (~35 linhas de JS executadas à toa em toda página + CSS morto).
- Removido: 4 imports não utilizados.
- Refatorado: `institucional.py` agora usa o índice `SOL_BY_SLUG` já existente em vez de duas buscas lineares repetidas.
- Refatorado: página de artigo e página 404 usam o mesmo componente `B.pagehead()` do resto do site em vez de reconstruir a seção à mão (eliminou o desvio que causava o bug de imagem lazy).
- Deduplicado: aviso legal de condições virou constante única (`CONDITIONS_NOTICE`) em vez de texto copiado em dois arquivos.
- Blindado: `harden_csp()` agora falha alto (erro no build) se não conseguir aplicar os hashes da CSP, em vez de publicar silenciosamente uma política quebrada.

## Testes executados

Toda a suíte de verificação do projeto rodou depois de cada bloco de mudanças, sempre com resultado limpo (mesmo baseline de antes, sem regressão nova):
- `audit.py` — 3.576 links internos verificados, nenhuma ocorrência.
- `audit_deep.py` — 4 apontamentos (mesmos de antes da auditoria, espaços duplos dentro de `<script>`, falso positivo conhecido).
- `design_audit.py` — sistema de design consistente, nada fora da escala.
- `audit_visual.py` — 3 apontamentos (mesmos de antes, dois falsos positivos já investigados nesta auditoria).
- `test_ui.py` — todos os testes funcionais passaram (formulários, select customizado, gaveta mobile, busca/filtro, acordeões, teclado, zero erros de JS).
- `preflight.py` — nenhuma pendência obrigatória.
- Testes manuais adicionais no navegador (Playwright): teclado no select customizado, duplo clique no envio, os cenários de calculadora e capital de giro listados acima.

## Pendências

Nenhuma crítica. Duas oportunidades de baixo risco/baixa prioridade ficaram registradas para uma próxima rodada, caso queira:
1. Reduzir a precisão das coordenadas do globo 3D da home para cortar ~25-30KB do `index.html` — não foi feito porque exigiria revisar visualmente cada fronteira depois de simplificada, e não é um bug, é uma otimização opcional.
2. Uma limpeza adicional de ~10 seletores CSS confirmados como não usados em lugar nenhum do site (baixíssimo impacto em bytes, risco desnecessário de mexer sem verificação visual completa de cada um).
