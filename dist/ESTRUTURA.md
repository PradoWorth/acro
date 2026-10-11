# Estrutura do site Acrópole Capital

Autoria: Lucas Prado, Acrópole Capital. Versão 1.3.

Regra de ouro: a URL pública nunca muda por causa de organização de pastas.

## Raiz (só o que precisa estar na raiz)

- `index.html` e `404.html`: home e página de erro.
- `robots.txt`, `sitemap.xml`, `site.webmanifest`, `favicon.ico`: exigem a raiz.
- `.htaccess` (Hostinger), `vercel.json`, `_headers`, `_redirects` (Vercel): servidor e segurança.
- `CHANGELOG.md` e `ESTRUTURA.md`: documentação.

## Páginas

- Página única, sem filhas: arquivo na raiz. Ex.: `sobre.html` vira `/sobre`.
- Hub com páginas filhas: hub na raiz (`conteudos.html`) e filhas em `pg-conteudos/`. A URL pública é `/conteudos/nome-da-filha`.
- Seções existentes: cidades, comparativos, conteudos, credito-alto-valor, credito-com-garantia-de-imovel, credito-para-empresas, emprestimo-home-equity, finalidades, imoveis, patrimonio-imobiliario, programas, situacoes, solucoes.
- Nova página filha: criar em `pg-<hub>/`, com link `../assets/...`, e registrar no `sitemap.xml`.
- Nova página única: criar na raiz com link `assets/...` e registrar no `sitemap.xml`.
- Nova seção (hub novo): criar `<hub>.html`, a pasta `pg-<hub>/` e incluir o nome nas regras de `.htaccess` e `vercel.json`.

## assets

- `css/`: `site.css`, estilo único do site.
- `js/core/`: `site.js`, `sim-modal.js`, `globe.js`, `consent.js`, `form-guard.js`, `config.js`.
- `js/analytics/`: `analytics.js` (GA4), `seo-events.js` (eventos de clique e formulário), `simulador-gtm.js` (GTM do simulador).
- `js/simulador/`: `simulador.js`, `cidades.js`, `municipios.json`.
- `img/cabecalhos/`: imagens do topo de cada página (`*-pagehead`).
- `img/solucoes/`: uma imagem por solução (`solucao-*`).
- `img/publicos/`: quem atendemos (`quem-atendemos-*`).
- `img/programas/`: Pronampe, BNDES, Procred, PEAC-FGI e afins.
- `img/institucional/`: hero, esteira, parceiros, metodologia, posicionamento.
- `img/conteudos/`, `img/partners/`, `img/kanban/`, `img/rail/`, `img/simulador/`: pastas temáticas já existentes.
- `fonts/`, `icons/`, `art/`, `social/`: fontes, ícones, arte vetorial e imagem de compartilhamento.

## Imagens

Cada imagem tem versões `.avif`, `.webp` e `.jpg` (e tamanhos `-800`, `-1100`). Ao criar uma nova, salvar na pasta do tema e nunca na raiz de `img/`.

## Antes de publicar

1. Rodar o pós-processamento (versão de cache em CSS e JS).
2. Conferir o rodapé: "Versão 1.3".
3. Subir o ZIP na Hostinger, apagar a pasta antiga se houver sobras e limpar o cache.
