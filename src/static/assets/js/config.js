/* Configuração pública do front-end.
   Nunca coloque chaves, tokens ou credenciais neste arquivo: ele é servido ao navegador.
   O endpoint abaixo deve apontar para uma função de servidor (serverless, API própria
   ou automação) que valide a origem, aplique rate limit e encaminhe o lead ao CRM. */
window.ACROPOLE_CONFIG = {
  // Ex.: "/api/lead" — vazio mantém o formulário em modo demonstração (nada é transmitido).
  endpoint: "",
  // Preparado para analytics. Nenhum script de terceiro é carregado sem preencher isto.
  analytics: { provider: "", id: "" }
};
