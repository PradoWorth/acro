/* Configuração pública do front-end.
   Nunca coloque chaves, tokens ou credenciais neste arquivo: ele é servido ao navegador.
   O endpoint abaixo deve apontar para uma função de servidor (serverless, API própria
   ou automação) que valide a origem, aplique rate limit e encaminhe o lead ao CRM. */
window.ACROPOLE_CONFIG = {
  // Webhook de TESTE (n8n) fornecido pela cliente — recebe o payload de
  // todo formulário do site (contato, popup de captação, Pronampe), com as
  // chaves obrigatórias name/email/whatsapp/faturamento/tracking_params
  // (ver "chaves canônicas" em site.js). Trocar por "/webhook/..." (sem o
  // "-test") quando o fluxo no n8n estiver validado e pronto pra produção.
  endpoint: "https://n8n.srv1800205.hstgr.cloud/webhook-test/recebimento-de-leads",
  // Preparado para analytics. Nenhum script de terceiro é carregado sem preencher isto.
  analytics: { provider: "", id: "" }
};
