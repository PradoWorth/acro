# Acrópole Capital: Design System

Etapa 6 do processo do Studio Responsivo, aplicada a um site que já existe.
Este documento não propõe um sistema novo: descreve o que está no ar, nomeia
o que estava solto e registra o que ficou pendente.

**Tipo diagnosticado (Etapa 0):** site institucional.
Sub-fluxo correspondente: arquitetura de informação → style guide → copy por
página → wireframe. Como o site está construído e publicável, o que se aplica
é o modo agente: QA, sistema de tokens e handoff.

---

## Ausência declarada

As skills `cores`, `tipografia`, `espacamento`, `componentes` e `layout`,
que seriam a fonte de verdade dos tokens, **não existem neste ambiente**.

Conforme a instrução para esse caso, o que está documentado abaixo é uma
escala provisória **derivada da marca do cliente**, não inventada: todos os
valores já vigoravam no site e foram extraídos de `src/static/assets/css/site.css`.
Quando as skills de token existirem, elas vencem, e este documento passa a ser
o mapa de migração, não a referência. Consta em Pendências.

---

## Cor

Acento institucional é o verde `--iris: #149d88`, e dele deriva o resto.
A escala não foi escolhida por gosto, foi construída a partir do que a marca
já tinha. O vermelho aparece só como feedback de erro (`--danger`), nunca
como cor de interface, seguindo o valor do Studio.

| Papel | Token | Valor |
|---|---|---|
| Acento primário | `--iris` / `--accent` | `#149d88` |
| Acento sobre fundo claro | `--accent-ink` | `#0c5e52` (7,67:1) |
| Acento sobre fundo escuro | `--iris-on-dark` | `#8acec4` (10,6:1) |
| Destaque secundário | `--cobalt` | `#317ae2` |
| Destaque secundário sobre claro | `--cobalt-ink` | `#255caa` (6,58:1) |
| Texto principal | `--ink` | `#262b31` |
| Texto secundário | `--slate` / `--slate-2` | `#596269` / `#6d757b` |
| Superfície escura | `--obsidian` | `#030b12` |
| Card sobre superfície escura | `--surface-ink` | `#1b2630` |
| Erro | `--danger` | `#b4231a` |
| Sucesso | `--ok` | `#009639` |

Cada par texto/fundo em uso foi medido: **zero ocorrências abaixo de WCAG AA**
em 46 páginas × desktop, tablet e mobile (`audit_visual.py`).

## Tipografia

Duas famílias, de propósito. Inter para texto corrido, UI, h3/h4 e o resto
do sistema — com fallback de sistema, escala em `--t-*` e *tracking*
negativo proporcional ao tamanho (`--track-*`): quanto maior o texto, mais
fechado, que é o que mantém o peso óptico constante. Manrope (negrito,
peso 700) para os títulos principais — h1 e h2 — usando o mesmo tracking
negativo do resto do sistema (`--track-h1`/`--track-h2`), já que é uma
sans grotesca como a Inter; ver seção 32 do README para o raciocínio
completo (essa fonte substituiu a Lora, usada antes nesse mesmo lugar —
ver seções 23 e 25 para o histórico).

`display 36 · h1 28 · h2 24 · h3/h4 18 · lead 18 · body 16 · sm/xs 14 · micro 12 · nano 11`

Medido: nenhum tamanho fora dessa escala em todo o site (`design_audit.py`).

## Espaçamento

Base 8px, oito degraus: `--sp-1` (.5rem) a `--sp-8` (10rem), mais `--gut` (24px)
e `--shell` (1200px) para a caixa de conteúdo.

Medido: nenhum espaçamento fora da grade (`design_audit.py`).

## Raio e elevação

`--r-input 6px · --r-card 16px · --r-button 40px · --r-tag 100px`
`--shadow-button · --shadow-card · --shadow-lg`

A escala de sombra existe só para o modo claro. As superfícies escuras do site
separam plano por **cor de superfície** (`--surface-ink` sobre `--obsidian`) e
por régua (`--rule-dark`), não por sombra: em fundo quase preto a sombra não
tem contraste para ler. Não é lacuna, é a decisão coerente com o fundo.

---

## As três camadas que faltavam

A skill pede, para institucional grande, estender o sistema com motion,
z-index, elevation e stroke. Elevation já existia. As outras três estavam
soltas no arquivo e agora têm nome. **Nenhum valor foi inventado**: todos
saíram do que já estava em uso.

### Movimento

Existia só `--dur` (.3s) e mais sete durações escritas à mão ao longo do
arquivo: `.2 .25 .28 .3 .35 .4 .45`. Três delas (.25, .28, .3) são
indistinguíveis a olho e existiam apenas por terem sido escritas em momentos
diferentes.

| Token | Valor | Uso |
|---|---|---|
| `--dur-instant` | .15s | realimentação imediata (foco) |
| `--dur-fast` | .2s | micro-estado (cor, borda) |
| `--dur-default` | .3s | hover e transição padrão |
| `--dur-slow` | .45s | mudança com deslocamento curto |
| `--ease` | `cubic-bezier(.22,.61,.36,1)` | padrão |
| `--ease-out` | `cubic-bezier(.16,1,.3,1)` | entrada (expo-out) |

38 declarações `transition` passaram a usar a escala.

**Fora da escala, de propósito:** durações de *percurso*, em que algo atravessa
uma distância em vez de só mudar de estado: a gaveta entrando (.5s), os
sublinhados varrendo a largura (.55s), a entrada dos blocos ao rolar (.62s).
E animação de cena, que não responde a gesto nenhum (o balanço de 1.9s dos
diagramas). Forçá-las na régua de hover deixaria o movimento pior, não mais
coerente: a duração que parece imediata num botão parece apressada quando o
elemento precisa cruzar a tela.

### Empilhamento

Havia 13 valores de z-index espalhados, de -1 a 210, sem ordem escrita em lugar
nenhum, o que torna qualquer sobreposição nova um chute. Hoje há uma escala, e
**zero literais** de z-index no CSS.

| Token | Valor | Camada |
|---|---|---|
| `--z-behind` | -1 | decoração atrás do texto |
| `--z-base` | 0 | arte de fundo da seção |
| `--z-art` | 1 | globo do hero |
| `--z-content` | 2 | conteúdo sobre a arte |
| `--z-dropdown` | 20 | menu do select customizado |
| `--z-float` | 80 | botão flutuante de contato |
| `--z-sticky` | 90 | cabeçalho |
| `--z-drawer` | 95 | gaveta mobile |
| `--z-skip` | 200 | atalho "pular para o conteúdo" |
| `--z-modal` | 210 | modal de lead |

Os valores são exatamente os que já vigoravam. Verificado por estilo computado
no navegador: a ordem visual não mudou. O modal fica acima do atalho de teclado
de propósito: com o modal aberto, o "pular para o conteúdo" não deve furar por
cima dele.

O quadro animado "Como trabalhamos" mantém uma pilha interna própria
(`jb__pop 6`, `jb__hand 30`, `jb__confetti 40`), abaixo do botão flutuante.
É contexto local de um componente fechado, documentado aqui e deliberadamente
não fundido à escala global.

### Traço

`--stroke-0: 0 · --stroke-1: 1px · --stroke-2: 2px`. 1px é a régua do site
(64 ocorrências); 2px aparece em ênfase.

---

## Handoff (Etapa 10.1)

`src/gerar_tokens.py` lê o `:root` de `site.css` e gera cinco formatos em
`tokens/`, na estrutura `primitive/` · `semantic/` · `components/`:

CSS Variables, SCSS, JSON Style Dictionary, TypeScript (`as const` mais type)
e config do Tailwind.

A fonte da verdade continua sendo o CSS do site: o script converte, em vez de
manter uma segunda lista à mão que descolaria da primeira. O Tailwind aponta
para as CSS Variables em vez de congelar valores, então o tema segue trocável
em runtime.

Validado: 96 tokens entram, 96 saem, zero faltando, zero sobrando, zero com
valor divergente; o TypeScript compila em modo estrito e o config do Tailwind
carrega no node.

---

## QA desta rodada

| Verificação | Resultado |
|---|---|
| Contraste WCAG AA | 0 ocorrências, 46 páginas × 3 larguras |
| Regra 1, travessão em copy | 0 ocorrências |
| Regra 3, dado volátil | 1 tratado (ver abaixo), 3 falsos positivos |
| Tokens órfãos | 0 reais; 6 eram parâmetros de runtime, 3 ganharam valor de reserva |
| Headlines (Etapa 7) | mediana 9-10 palavras; nenhum título de seção passa de 7 |
| Erros de JavaScript | 0 em 46 páginas × desktop e mobile |

**Regra 3 na prática.** O único dado de mercado volátil que alimenta um número
visível numa página de conversão é a Selic de referência do simulador de
programas públicos. Ele já estava declarado com data e com a ressalva de que a
taxa é pós-fixada. O que faltava era ele **avisar** quando envelhecesse: a data
virou `AAAA-MM` legível por máquina, o rótulo em português passou a ser derivado
dela (não pode mais divergir do valor), e `preflight.py` alerta a partir de
quatro meses, ou seja, duas ou três reuniões do Copom. Testado com data envelhecida:
o aviso aparece com o número de meses correto.

Os outros três achados foram examinados e descartados com justificativa:
"Selic vigente + 6% ao ano" é fórmula, não número que envelhece; e as
estatísticas de mercado nos artigos estão datadas e com fonte (Abecip),
que é prática editorial correta, não dado volátil apresentado como atual.

---

## Pendências

1. **Skills de token inexistentes.** `cores`, `tipografia`, `espacamento`,
   `componentes` e `layout` não existem neste ambiente. A escala acima é
   provisória e derivada da marca. Quando as skills existirem, migrar para os
   nomes delas e reduzir este documento a um mapa de migração.
2. **Duas headlines de hero acima de 12 palavras.** `agronegocio.html` (15) e
   `empresas.html` (14). Alternativas propostas abaixo, mas copy é voz do
   cliente: a decisão é do Leonel, não minha.
   - *Agronegócio*, hoje: "Safra tem calendário. Capital de giro rural precisa acompanhar esse calendário."
     → "Safra tem calendário. O capital de giro precisa acompanhar." (9)
     → "O crédito rural que respeita o calendário da safra." (9)
   - *Empresas*, hoje: "Uma empresa lucrativa pode ficar sem caixa. Isso tem nome, e tem solução."
     → "Empresa lucrativa também fica sem caixa. Isso tem solução." (9)
     → "Lucro no papel não paga fornecedor. Existe estrutura para isso." (10)
3. **H1 de artigo entre 13 e 15 palavras (6 casos).** Exceção declarada, não
   defeito: são títulos de SEO, onde o comprimento carrega a busca. Encurtar
   para a régua de headline de marketing custaria alcance. Fica registrado para
   que a decisão seja consciente e não pareça descuido.
4. **Sombra só no modo claro.** Decisão coerente com o fundo quase preto das
   faixas escuras, registrada para não ser lida como lacuna em auditoria futura.
5. **Selic de referência.** Confirmar a taxa vigente a cada atualização; o
   preflight avisa a partir de quatro meses.
6. **2 thumbnails de `/conteudos` fora do padrão fotográfico.**
   `marco-das-garantias-o-que-mudou.jpg` e `scd-sep-e-a-natureza-do-credor.jpg`
   são ilustração estilo cartoon gerada por IA, com o título do artigo
   desenhado dentro da própria imagem ("MARCO DAS GARANTIAS", "SCD SEP BANCO
   COOPERAT..."). As outras 18 capas de artigo são fotografia realista sem
   texto embutido, com o título vindo do HTML. Não corrigi porque não tenho
   como gerar fotografia real aqui, e reprocessar a ilustração existente para
   apagar o texto deixaria pior, não melhor — seria maquiar o problema, não
   resolvê-lo. Ação recomendada: substituir os 2 arquivos por fotografia no
   mesmo estilo das demais 18 (mesmo caminho em `static/assets/img/conteudos/`,
   nos formatos `.avif`/`.webp`/`.jpg` e a variante `-thumb`, ver `content/
   conteudos.py` linhas 124-125 e 161-162).
