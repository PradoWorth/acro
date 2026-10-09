(function () {
/* ===== js/config.js ===== */
/**
 * config.js
 * Configurações centrais da aplicação.
 * Nenhum valor sensível (API keys, tokens de CRM) deve ficar aqui.
 * Este arquivo fica no frontend, então só parâmetros de negócio não sensíveis.
 */

const CONFIG = {
  // Regra de qualificação por município.
  // Alterar este número muda a regra em toda a aplicação.
  MINIMUM_CITY_POPULATION: 50000,

  // Regra de qualificação por percentual de financiamento em aberto no
  // imóvel. Quitado ou com menos que este percentual em aberto: segue no
  // funil. Igual ou mais que este percentual em aberto: desqualificado.
  MAX_OPEN_FINANCING_PERCENTAGE: 0.30,

  // Faixa de LTV (Loan to Value) usada na estimativa inicial. Em vez de
  // um percentual fixo, cada simulação sorteia um valor dentro dessa
  // faixa (ver calculator.js) — fica mais parecido com uma análise real,
  // que varia caso a caso, em vez de sempre cravar no teto.
  MIN_LOAN_TO_VALUE: 0.40,
  MAX_LOAN_TO_VALUE: 0.60,

  // Valor mínimo aceito para o imóvel (evita simulações com valores irreais).
  MIN_PROPERTY_VALUE: 50000,
  MAX_PROPERTY_VALUE: 100000000,

  // Valor mínimo aceito para o crédito desejado.
  MIN_DESIRED_AMOUNT: 5000,

  // Valor mínimo aceito para a renda mensal informada.
  MIN_MONTHLY_INCOME: 1000,

  // Simulação de parcela (tela de resultado): taxa de juros mensal e prazo
  // usados para estimar a parcela do valor desejado pelo lead. Sistema de
  // amortização Price (parcelas fixas) — ver calculateInstallment em
  // calculator.js. A partir de 1,19% ao mês (mais IPCA) / até 240 meses (20 anos)
  // são os parâmetros de referência informados pela Acrópole; ajustar aqui muda a simulação em
  // toda a aplicação.
  MONTHLY_INTEREST_RATE: 0.0119,
  FINANCING_TERM_MONTHS: 240,

  // Percentual máximo da renda mensal que a parcela deve representar,
  // usado para calcular a "renda mínima recomendada" exibida ao lead
  // (renda mínima = parcela ÷ este percentual). Referência da Acrópole: 30%.
  MAX_INSTALLMENT_TO_INCOME_RATIO: 0.30,

  // Nome da aplicação / campanha, usado em analytics e no payload do lead.
  APP_NAME: 'Simulador Home Equity Acrópole',

  // Número de WhatsApp da equipe comercial (formato internacional, sem símbolos).
  // (43) 98432-1492
  WHATSAPP_NUMBER: '5543984321492',

  // Estrutura de integração com CRM. Preencher em tempo de deploy
  // (variável de ambiente / backend proxy), nunca com valores reais aqui.
  // O envio real deve passar por um backend/proxy, nunca direto do
  // frontend com token exposto — ver js/crmIntegration.js.
  CRM: {
    // Mesmo webhook (n8n) usado no Diagnóstico 360, o outro formulário da
    // Acrópole — recebe leads qualificados de várias origens.
    webhookUrl: 'https://n8n.srv1800205.hstgr.cloud/webhook/recebimento-de-leads',
    apiKey: '', // NÃO preencher no frontend em produção; usar backend proxy
    pipeline: 'home-equity',
    stage: 'novo-lead',
    campaignId: '',
  },

  // Endpoints de serviços externos.
  SERVICES: {
    // API SIDRA (Sistema IBGE de Recuperação Automática) — fonte primária
    // de população por município. Tabela 6579 (Estimativas de população),
    // variável 9324 (população estimada), nível territorial N6 (município).
    // Documentação: https://apisidra.ibge.gov.br/
    sidraApiBaseUrl: 'https://apisidra.ibge.gov.br/values/t/6579/v/9324/p/last/n6',

    // API de Agregados do IBGE (mesma tabela/variável do SIDRA, formato
    // JSON diferente) — usada como segunda tentativa se a API SIDRA
    // estiver indisponível.
    ibgePopulationApiBaseUrl: 'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/-1/variaveis/9324',
  },

  // Status possíveis do lead.
  LEAD_STATUS: {
    QUALIFIED: 'QUALIFICADO',
    DISQUALIFIED_LOCATION: 'DESQUALIFICADO — LOCALIZAÇÃO',
    DISQUALIFIED_FINANCING: 'DESQUALIFICADO — FINANCIAMENTO EM ABERTO',
  },
};


/* ===== js/analytics.js ===== */
/**
 * analytics.js
 * Camada única de disparo de eventos. Hoje envia para o console e para
 * window.dataLayer / gtag / fbq quando existirem, sem exigir nenhuma
 * dependência obrigatória. Basta plugar o script do GA4/Meta Pixel no
 * <head> e os eventos abaixo já vão fluir para eles.
 */

const EVENTS = {
  QUIZ_STARTED: 'quiz_started',
  PROPERTY_VALUE_COMPLETED: 'property_value_completed',
  CITY_SELECTED: 'city_selected',
  LOCATION_QUALIFIED: 'location_qualified',
  LOCATION_DISQUALIFIED: 'location_disqualified',
  PROPERTY_STATUS_COMPLETED: 'property_status_completed',
  FINANCING_DISQUALIFIED: 'financing_disqualified',
  INCOME_OWNERSHIP_COMPLETED: 'income_ownership_completed',
  PROPERTY_LOCATION_TYPE_COMPLETED: 'property_location_type_completed',
  QUIZ_COMPLETED: 'quiz_completed',
  LEAD_INFO_COMPLETED: 'lead_info_completed',
  SIMULATION_GENERATED: 'simulation_generated',
  LEAD_SUBMITTED: 'lead_submitted',
  WHATSAPP_CLICKED: 'whatsapp_clicked',
};

function dispatch(eventName, payload = {}) {
  const data = {
    event: eventName,
    timestamp: new Date().toISOString(),
    ...payload,
  };

  try {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(data);
  } catch (_) {
    /* dataLayer indisponível, ignora silenciosamente */
  }

  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, payload);
    }
  } catch (_) {}

  try {
    if (typeof window.fbq === 'function') {
      window.fbq('trackCustom', eventName, payload);
    }
  } catch (_) {}

  if (window.__HE_DEBUG__) {
    // eslint-disable-next-line no-console
    console.log('[analytics]', eventName, payload);
  }
}

const analytics = {
  EVENTS,
  track: dispatch,
  captureUtms() {
    const params = new URLSearchParams(window.location.search);
    const utms = {
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_content: params.get('utm_content') || '',
      utm_term: params.get('utm_term') || '',
    };
    try {
      const hasAny = Object.values(utms).some(Boolean);
      if (hasAny) {
        sessionStorage.setItem('he_utms', JSON.stringify(utms));
      }
      const stored = sessionStorage.getItem('he_utms');
      return stored ? JSON.parse(stored) : utms;
    } catch (_) {
      return utms;
    }
  },
};


/* ===== js/attribution.js ===== */
/**
 * attribution.js
 * Captura e persiste dados de atribuição de marketing (UTMs, cliques de
 * anúncio, cookies de pixel) num cookie de 30 dias, pra esses dados
 * seguirem o lead até o fim do funil — mesma lógica usada no formulário
 * "Diagnóstico 360" (outro formulário da Acrópole), portada pra cá.
 *
 * O valor guardado no cookie é acumulativo: se o visitante chegar com
 * UTMs numa primeira visita e voltar depois direto (sem UTM na URL), a
 * atribuição original da campanha não se perde.
 */

const COOKIE_NAME = 'app_attribution';
const COOKIE_DAYS = 30;
const TRACKED_KEYS = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_term',
  'utm_content',
  'gclid',
  'gbraid',
  'wbraid',
  'fbclid',
];

function getCookie(name) {
  try {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  } catch (_) {
    /* documento sem acesso a cookies (ex.: sandbox): segue sem atribuição */
  }
  return null;
}

function setCookie(name, value, days) {
  try {
    let expires = '';
    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = `; expires=${date.toUTCString()}`;
    }
    // "Secure" só é adicionado quando o site está em HTTPS: em http:// (ex.:
    // desenvolvimento local) o navegador simplesmente rejeitaria o cookie.
    const secureFlag = window.location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = `${name}=${value || ''}${expires}; path=/; SameSite=Lax${secureFlag}`;
  } catch (_) {}
}

function readStoredAttribution() {
  try {
    const existing = getCookie(COOKIE_NAME);
    return existing ? JSON.parse(decodeURIComponent(existing)) : {};
  } catch (_) {
    return {};
  }
}

function persist(data) {
  setCookie(COOKIE_NAME, encodeURIComponent(JSON.stringify(data)), COOKIE_DAYS);
}

/**
 * Mescla os parâmetros de tracking da URL atual com o que já estava
 * salvo, atualiza fbp/fbc (cookies do Meta Pixel, se já tiverem sido
 * criados) e persiste tudo de novo no cookie.
 * @returns {object} snapshot atual dos dados de atribuição
 */
function updateAttribution() {
  const data = readStoredAttribution();

  try {
    const params = new URLSearchParams(window.location.search);
    TRACKED_KEYS.forEach((key) => {
      const value = params.get(key);
      if (value) data[key] = value;
    });
  } catch (_) {}

  try {
    data.page_location = window.location.href;
    data.user_agent = navigator.userAgent;
  } catch (_) {}
  data.captured_at = new Date().toISOString();

  const fbp = getCookie('_fbp');
  const fbc = getCookie('_fbc');
  if (fbp) data.fbp = fbp;
  if (fbc) data.fbc = fbc;

  persist(data);
  return data;
}

let monitoringStarted = false;

/**
 * Chama updateAttribution() assim que a página carrega e, se o cookie
 * _fbp do Meta Pixel ainda não existir (o pixel pode demorar pra
 * carregar), tenta de novo a cada 500ms por até 5s — mesma janela de
 * tolerância do formulário de origem dessa lógica.
 */
function startAttributionCapture() {
  if (monitoringStarted) return;
  monitoringStarted = true;

  const data = updateAttribution();
  if (data.fbp) return;

  let attempts = 0;
  const interval = window.setInterval(() => {
    attempts += 1;
    const updated = updateAttribution();
    if (updated.fbp || attempts >= 10) {
      window.clearInterval(interval);
    }
  }, 500);
}

/**
 * JSON pronto pra ir no payload do lead (campo tracking_params).
 * Sempre relê/atualiza na hora, pra pegar fbp/fbc mesmo se o Pixel só
 * tiver carregado depois da primeira captura.
 */
function getAttributionJSON() {
  return JSON.stringify(updateAttribution());
}


/* ===== js/validation.js ===== */
/**
 * validation.js
 * Máscaras de campo e funções de validação. Sem dependências externas.
 */


// ---------- Máscaras ----------

/** Formata dígitos como moeda brasileira em reais inteiros (R$ 800.000) enquanto o usuário digita.
 *  Digitar 800000 vira R$ 800.000. Valores colados com centavos (800.000,00) perdem os centavos. */
function maskCurrencyInput(rawValue) {
  const digits = String(rawValue).replace(/,\d{1,2}\s*$/, '').replace(/\D/g, '');
  if (!digits) return '';
  const number = parseInt(digits, 10);
  return number.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
}

/** Converte string de moeda formatada em número (reais inteiros). */
function parseCurrencyToNumber(formatted) {
  if (!formatted) return 0;
  const digits = String(formatted).replace(/,\d{1,2}\s*$/, '').replace(/\D/g, '');
  if (!digits) return 0;
  return parseInt(digits, 10);
}

/** Formata telefone/WhatsApp brasileiro: (00) 00000-0000. */
function maskPhone(rawValue) {
  const all = rawValue.replace(/\D/g, '');
  const digits = (all.length > 11 && all.startsWith('55') ? all.slice(2) : all).slice(0, 11);
  if (digits.length <= 2) return digits;
  if (digits.length <= 6) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
  if (digits.length <= 10) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
  }
  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
}

// ---------- Validações ----------

function isValidPropertyValue(numberValue) {
  return (
    Number.isFinite(numberValue) &&
    numberValue >= CONFIG.MIN_PROPERTY_VALUE &&
    numberValue <= CONFIG.MAX_PROPERTY_VALUE
  );
}

function isValidDesiredAmount(numberValue) {
  return Number.isFinite(numberValue) && numberValue >= CONFIG.MIN_DESIRED_AMOUNT;
}

function isValidIncome(numberValue) {
  return Number.isFinite(numberValue) && numberValue >= CONFIG.MIN_MONTHLY_INCOME;
}

function isValidName(value) {
  const trimmed = (value || '').trim();
  return trimmed.length >= 3 && /[a-zA-ZÀ-ÿ]/.test(trimmed);
}

function isValidPhone(rawValue) {
  const digits = (rawValue || '').replace(/\D/g, '');
  return digits.length === 10 || digits.length === 11;
}

function isValidEmail(value) {
  const trimmed = (value || '').trim();
  if (!trimmed) return false; // e-mail é obrigatório
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
}

const FRIENDLY_ERRORS = {
  cityRequired: 'Selecione sua cidade na lista para continuar.',
  propertyValueEmpty: 'Informe o valor aproximado do seu imóvel.',
  propertyValueInvalid: 'Informe um valor válido para o seu imóvel.',
  desiredAmountEmpty: 'Informe o valor que você deseja de crédito.',
  desiredAmountInvalid: 'Informe um valor válido para o crédito desejado.',
  incomeEmpty: 'Informe sua renda mensal aproximada.',
  incomeInvalid: 'Informe um valor de renda válido.',
  ownershipRequired: 'Selecione se o imóvel está no CPF ou no CNPJ.',
  nameInvalid: 'Informe seu nome completo.',
  phoneInvalid: 'Informe um número de WhatsApp válido com DDD.',
  emailInvalid: 'Informe um e-mail válido.',
  emailRequired: 'Informe seu e-mail para continuar.',
  genericError: 'Algo não saiu como esperado. Tente novamente em alguns instantes.',
};


/* ===== js/citiesData.js ===== */
/**
 * citiesData.js
 * Base de municípios brasileiros (nome, UF, código IBGE) para o
 * autocomplete de cidade da etapa de localização. Fonte: base do IBGE
 * (5.571 municípios), redistribuída pelo pacote MIT 'municipios-brasil'
 * (https://www.npmjs.com/package/municipios-brasil). Formato compacto
 * [nome, uf, codigoIbge] para manter o arquivo leve.
 */



/* ===== js/citiesService.js ===== */
/**
 * citiesService.js
 * Busca de município por nome, ignorando acentos e maiúsculas/minúsculas,
 * para o autocomplete da etapa de localização. Usa a base local
 * (citiesData.js) e por isso responde a cada tecla digitada, sem
 * depender de rede.
 */


function normalize(value) {
  return value
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .trim();
}

// Base local de municípios (IBGE, Censo 2022): o mesmo arquivo atende o
// autocomplete de cidade e a consulta de população. Carregado uma única vez,
// em segundo plano, logo depois que o simulador abre.
let __munPromise = null;
function loadMunicipios() {
  if (!__munPromise) {
    __munPromise = fetch('assets/js/municipios.json', { credentials: 'same-origin' })
      .then((r) => { if (!r.ok) throw new Error('status ' + r.status); return r.json(); })
      .catch((e) => { __munPromise = null; throw e; });
  }
  return __munPromise;
}

let indexedCities = null;

function ensureCities() {
  return loadMunicipios().then((j) => {
    if (!indexedCities) {
      indexedCities = j.d.map((x) => ({ nome: x[0], uf: x[1], ibge: String(x[3]), norm: normalize(x[0]) }));
    }
    return indexedCities;
  });
}

function getIndexedCities() {
  return indexedCities || [];
}

/**
 * Busca municípios cujo nome combina com o termo digitado.
 * Prioriza nomes que começam com o termo sobre os que só contêm o termo.
 * @param {string} query
 * @param {number} limit
 * @returns {{ nome: string, uf: string, ibge: string }[]}
 */
function searchCities(query, limit = 8) {
  const q = normalize(query || '');
  if (q.length < 2) return [];

  const startsWith = [];
  const contains = [];

  for (const city of getIndexedCities()) {
    if (city.norm.startsWith(q)) {
      startsWith.push(city);
    } else if (city.norm.includes(q)) {
      contains.push(city);
    }
  }

  const byName = (a, b) => a.nome.localeCompare(b.nome, 'pt-BR');
  startsWith.sort(byName);
  contains.sort(byName);

  return [...startsWith, ...contains].slice(0, limit).map(({ nome, uf, ibge }) => ({ nome, uf, ibge }));
}


/* ===== js/populationService.js ===== */
/**
 * populationService.js
 * Camada de consulta de população municipal, isolada para poder ser
 * substituída facilmente por outra fonte (dataset próprio, outra API,
 * backend interno) sem alterar o restante da aplicação.
 *
 * Cadeia de tentativas, na ordem:
 *   1. API SIDRA (Sistema IBGE de Recuperação Automática) — apisidra.ibge.gov.br
 *      Fonte oficial primária. Tabela 6579 (Estimativas de população),
 *      variável 9324, consultada pelo código do município (IBGE) que o
 *      usuário seleciona na busca de cidade (ver citiesService.js).
 *   2. API de Agregados do IBGE (servicodados.ibge.gov.br) — mesma tabela/
 *      variável, formato de resposta diferente. Usada como segunda
 *      tentativa caso a API SIDRA esteja fora do ar.
 *   3. Dataset local de apoio (ver FALLBACK_KNOWN_CITIES), só com as
 *      capitais/grandes cidades mais comuns.
 *
 * Se nenhuma das três der um número, o resultado é "indeterminado" — a
 * aplicação trata isso deixando o lead seguir no funil (ver
 * qualification.js), para não descartar leads bons por instabilidade de
 * uma API externa.
 */

// Dataset de apoio para os casos mais comuns (capitais e grandes cidades),
// usado apenas se a API do IBGE falhar. Pode ser expandido livremente —
// é só um objeto { "Município|UF": populacao }.
// Timeout de rede pra cada tentativa de API do IBGE: sem isso, uma chamada
// que trava (sem responder e sem sequer dar erro) prende o lead
// indefinidamente no spinner "Verificando disponibilidade..." da etapa de
// cidade. Ao expirar, o fetch é abortado e tratado como falha comum, então
// a cadeia de fallback (ver getMunicipalityPopulation) segue normalmente.
const POPULATION_API_TIMEOUT_MS = 6000;

async function fetchWithTimeout(url, options) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), POPULATION_API_TIMEOUT_MS);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    window.clearTimeout(timeoutId);
  }
}

const FALLBACK_KNOWN_CITIES = {
  'São Paulo|SP': 11451245,
  'Rio de Janeiro|RJ': 6211423,
  'Brasília|DF': 3094325,
  'Salvador|BA': 2418005,
  'Fortaleza|CE': 2428708,
  'Belo Horizonte|MG': 2315560,
  'Manaus|AM': 2255903,
  'Curitiba|PR': 1948626,
  'Recife|PE': 1488920,
  'Goiânia|GO': 1536097,
  'Porto Alegre|RS': 1332570,
  'Belém|PA': 1303403,
};

/**
 * @param {string} ibgeCode código do município (7 dígitos)
 * @param {string} municipio nome do município (fallback)
 * @param {string} estado UF (fallback)
 * @returns {Promise<{ population: number|null, source: 'sidra-api'|'ibge-agregados-api'|'fallback-dataset'|'unavailable' }>}
 */
let __localPop=null;
async function tryLocalDataset(ibgeCode) {
  try {
    if (!__localPop) {
      const j = await loadMunicipios();
      __localPop = new Map(j.d.map((x) => [String(x[3]), x[2]]));
    }
    const v = __localPop.get(String(ibgeCode));
    return typeof v === 'number' ? v : null;
  } catch (_) { return null; }
}

async function getMunicipalityPopulation(ibgeCode, municipio, estado) {
  const fromLocal = await tryLocalDataset(ibgeCode);
  if (fromLocal !== null) {
    return { population: fromLocal, source: 'ibge-censo-2022-local' };
  }
  const fromFallback0 = tryFallbackDataset(municipio, estado);
  if (fromFallback0 !== null) {
    return { population: fromFallback0, source: 'fallback-dataset' };
  }
  return { population: null, source: 'unavailable' };
}

async function __unusedRemoteChain(ibgeCode, municipio, estado) {
  const fromSidra = await tryApiSidra(ibgeCode);
  if (fromSidra !== null) {
    return { population: fromSidra, source: 'sidra-api' };
  }

  const fromAgregados = await tryIbgeAgregadosApi(ibgeCode);
  if (fromAgregados !== null) {
    return { population: fromAgregados, source: 'ibge-agregados-api' };
  }

  const fromFallback = tryFallbackDataset(municipio, estado);
  if (fromFallback !== null) {
    return { population: fromFallback, source: 'fallback-dataset' };
  }

  return { population: null, source: 'unavailable' };
}

/**
 * API SIDRA (Sistema IBGE de Recuperação Automática) — fonte primária.
 * Doc: https://apisidra.ibge.gov.br/
 * Formato da resposta: array de objetos, o primeiro é o cabeçalho das
 * colunas e os seguintes são as linhas de dados. O valor consultado fica
 * na chave "V" da última linha (período mais recente, graças a "p/last").
 */
async function tryApiSidra(ibgeCode) {
  if (!ibgeCode) return null;
  try {
    /* CONFIG já está no escopo global do bundle */
    const url = `${CONFIG.SERVICES.sidraApiBaseUrl}/${ibgeCode}`;
    const response = await fetchWithTimeout(url, { headers: { Accept: 'application/json' } });
    if (!response.ok) return null;

    const data = await response.json();
    if (!Array.isArray(data) || data.length < 2) return null;

    const lastRow = data[data.length - 1];
    const raw = lastRow ? lastRow.V : null;
    if (raw === null || raw === undefined || raw === '...' || raw === '-' || raw === 'X') return null;

    const value = parseInt(String(raw).replace(/\D/g, ''), 10);
    return Number.isFinite(value) ? value : null;
  } catch (_) {
    return null;
  }
}

/**
 * API de Agregados do IBGE — segunda tentativa, mesma fonte de dados
 * (SIDRA por trás), formato de resposta diferente. Serve de rede de
 * segurança caso apisidra.ibge.gov.br esteja instável.
 */
async function tryIbgeAgregadosApi(ibgeCode) {
  if (!ibgeCode) return null;
  try {
    /* CONFIG já está no escopo global do bundle */
    const url = `${CONFIG.SERVICES.ibgePopulationApiBaseUrl}?localidades=N6[${ibgeCode}]`;
    const response = await fetchWithTimeout(url, { headers: { Accept: 'application/json' } });
    if (!response.ok) return null;

    const data = await response.json();
    // Formato: [{ resultados: [{ series: [{ localidade: {...}, serie: { "2024": "123456" } }] }] }]
    const serie = data?.[0]?.resultados?.[0]?.series?.[0]?.serie;
    if (!serie) return null;

    const years = Object.keys(serie).sort();
    const latestYear = years[years.length - 1];
    const value = parseInt(serie[latestYear], 10);
    return Number.isFinite(value) ? value : null;
  } catch (_) {
    return null;
  }
}

function tryFallbackDataset(municipio, estado) {
  if (!municipio || !estado) return null;
  const key = `${municipio}|${estado}`;
  return Object.prototype.hasOwnProperty.call(FALLBACK_KNOWN_CITIES, key)
    ? FALLBACK_KNOWN_CITIES[key]
    : null;
}


/* ===== js/calculator.js ===== */
/**
 * calculator.js
 * Cálculo da estimativa de crédito com base no valor do imóvel.
 */


/**
 * Sorteia um percentual de LTV dentro da faixa configurada
 * (CONFIG.MIN_LOAN_TO_VALUE a CONFIG.MAX_LOAN_TO_VALUE), arredondado pro
 * múltiplo de 5% mais próximo — fica com uma variação natural entre
 * simulações (40%, 45%, 50%...) em vez de sempre cravar no teto.
 * @returns {number} percentual entre 0 e 1 (ex.: 0.55 = 55%)
 */
function rollLoanToValue() {
  const { MIN_LOAN_TO_VALUE, MAX_LOAN_TO_VALUE } = CONFIG;
  const raw = MIN_LOAN_TO_VALUE + Math.random() * (MAX_LOAN_TO_VALUE - MIN_LOAN_TO_VALUE);
  const roundedToStep = Math.round(raw * 20) / 20; // múltiplos de 5% (0.05)
  return Math.min(MAX_LOAN_TO_VALUE, Math.max(MIN_LOAN_TO_VALUE, roundedToStep));
}

/**
 * @param {number} propertyValue valor do imóvel informado pelo usuário
 * @returns {{ propertyValue: number, ltvPercentage: number, estimatedCredit: number }}
 */
function calculateEstimatedCredit(propertyValue) {
  const ltv = rollLoanToValue();
  const estimatedCredit = Math.round(propertyValue * ltv);
  return {
    propertyValue,
    ltvPercentage: ltv,
    estimatedCredit,
  };
}

/**
 * Estima a parcela mensal fixa (sistema de amortização Price) de um
 * financiamento, para dar ao lead uma noção concreta do compromisso
 * mensal envolvido — não é uma proposta de crédito, só uma simulação
 * ilustrativa com taxa e prazo de referência (ver CONFIG).
 * @param {number} principal valor financiado (ex.: valor desejado pelo lead)
 * @param {number} monthlyRate taxa de juros mensal (ex.: 0.013 = 1,3%)
 * @param {number} months prazo em meses (ex.: 240 = 20 anos)
 * @returns {number} valor da parcela mensal
 */
function calculateInstallment(principal, monthlyRate, months) {
  if (!principal || principal <= 0 || !months || months <= 0) return 0;
  if (!monthlyRate) return Math.round(principal / months);

  const factor = Math.pow(1 + monthlyRate, months);
  const installment = principal * (monthlyRate * factor) / (factor - 1);
  return Math.round(installment);
}

/**
 * Renda mensal mínima recomendada para que a parcela não supere o
 * percentual de comprometimento de renda configurado.
 * @param {number} installment valor da parcela mensal
 * @param {number} ratio percentual máximo da renda (ex.: 0.30 = 30%)
 * @returns {number} renda mensal mínima recomendada
 */
function calculateMinimumIncomeForInstallment(installment, ratio) {
  if (!installment || !ratio) return 0;
  return Math.round(installment / ratio);
}

function formatCurrencyBRL(value) {
  return (value || 0).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  });
}


/* ===== js/qualification.js ===== */
/**
 * qualification.js
 * Regra de qualificação por localização (população do município).
 * Mantém a regra centralizada e configurável — nunca hardcode o número
 * de habitantes fora de config.js.
 */



/**
 * @param {{ municipio: string, estado: string, ibgeCode: string }} address
 * @returns {Promise<{
 *   qualified: boolean,
 *   population: number|null,
 *   populationSource: string,
 *   status: string,
 * }>}
 */
async function qualifyByLocation(address) {
  const { population, source } = await getMunicipalityPopulation(
    address.ibgeCode,
    address.municipio,
    address.estado
  );

  // Sem dado de população disponível: não penaliza o lead por instabilidade
  // de uma fonte externa. Segue qualificado, mas fica registrado para
  // conferência manual da equipe (ver campo populationSource no payload).
  if (population === null) {
    return {
      qualified: true,
      population: null,
      populationSource: source,
      status: CONFIG.LEAD_STATUS.QUALIFIED,
    };
  }

  const qualified = population >= CONFIG.MINIMUM_CITY_POPULATION;

  return {
    qualified,
    population,
    populationSource: source,
    status: qualified
      ? CONFIG.LEAD_STATUS.QUALIFIED
      : CONFIG.LEAD_STATUS.DISQUALIFIED_LOCATION,
  };
}


/* ===== js/leadStore.js ===== */
/**
 * leadStore.js
 * Estado central do lead durante o funil. Mantém em memória (e em
 * sessionStorage, só para sobreviver a um refresh acidental — nenhum
 * dado sensível fica em localStorage nem é persistido depois do envio).
 */



const STORAGE_KEY = 'he_lead_draft';

function emptyLead() {
  return {
    // Localização
    municipio: '',
    estado: '',
    ibgeCode: '',
    populacaoEstimada: null,
    populationSource: '',

    // Imóvel
    valorImovel: null,
    tipoImovel: [],
    situacaoImovel: '',
    titularidadeImovel: '',
    localizacaoCasa: '',
    localizacaoTerreno: '',

    // Perfil financeiro
    rendaMensal: null,

    // Operação
    valorDesejado: null,

    // Simulação
    percentualConsiderado: null,
    estimativaCredito: null,
    parcelaEstimada: null,

    // Contato
    nome: '',
    whatsapp: '',
    email: '',

    // Meta
    status: '',
    dataHoraSimulacao: '',
    origemCampanha: '',
    utmSource: '',
    utmMedium: '',
    utmCampaign: '',
    utmContent: '',
    utmTerm: '',
  };
}

let leadState = loadFromStorage() || emptyLead();

function loadFromStorage() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (_) {
    return null;
  }
}

function persist() {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(leadState));
  } catch (_) {
    /* sessionStorage indisponível: segue só em memória */
  }
}

const leadStore = {
  get() {
    return { ...leadState };
  },

  update(partial) {
    leadState = { ...leadState, ...partial };
    persist();
  },

  reset() {
    leadState = emptyLead();
    persist();
  },

  captureUtms() {
    const utms = analytics.captureUtms();
    leadState = {
      ...leadState,
      utmSource: utms.utm_source,
      utmMedium: utms.utm_medium,
      utmCampaign: utms.utm_campaign,
      utmContent: utms.utm_content,
      utmTerm: utms.utm_term,
      origemCampanha: utms.utm_campaign || utms.utm_source || '',
    };
    persist();
  },

  /** Payload final pronto para envio ao CRM. */
  toCrmPayload() {
    return {
      ...leadState,
      dataHoraSimulacao: new Date().toISOString(),
      // Recaptura na hora do envio (não usa um valor guardado antes) pra
      // pegar fbp/fbc mesmo se o Pixel só tiver terminado de carregar
      // depois que o lead já estava navegando pelo funil.
      tracking_params: getAttributionJSON(),
      notas: buildLeadNotes(leadState),
    };
  },
};

/** Bloco de notas com TODOS os dados do lead, para o campo de notas do CRM (via n8n). */
function buildLeadNotes(lead) {
  let resumo = [];
  try {
    resumo = buildWhatsappSummary(lead)
      .split('\n')
      .filter((l) => l && !l.startsWith('Olá!') && !l.startsWith('Gostaria de saber'));
  } catch (_) {
    resumo = [];
  }
  const extra = [];
  if (lead.whatsapp) extra.push(`WhatsApp: ${lead.whatsapp}`);
  if (lead.email) extra.push(`E-mail: ${lead.email}`);
  if (lead.populacaoEstimada) extra.push(`População (IBGE): ${lead.populacaoEstimada}`);
  if (lead.origemCampanha) extra.push(`Origem da campanha: ${lead.origemCampanha}`);
  const utm = [lead.utmSource, lead.utmMedium, lead.utmCampaign, lead.utmContent, lead.utmTerm].filter(Boolean);
  if (utm.length) extra.push(`UTM: ${utm.join(' / ')}`);
  let quando = '';
  try {
    quando = new Date().toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });
  } catch (_) {
    quando = new Date().toISOString();
  }
  return ['NOTAS DO LEAD (simulador Home Equity)', `Data e hora: ${quando}`, 'Página: /simulador-home-equity', ...resumo, ...extra].join('\n');
}


/* ===== js/leadScoring.js ===== */
/**
 * leadScoring.js
 * Pontuação interna do lead, para a equipe comercial priorizar quem
 * atender primeiro. Não é exibida ao usuário.
 *
 * Pontuação simples, 0 a 100 (25 + 20 + 15 + 15 + 15 + 10, ver cada
 * critério abaixo). Fácil de recalibrar depois com dados reais.
 */


function scoreLead(lead) {
  let score = 0;

  // Valor do imóvel: quanto maior, mais pontos (até um teto).
  if (lead.valorImovel >= 1500000) score += 25;
  else if (lead.valorImovel >= 800000) score += 20;
  else if (lead.valorImovel >= 400000) score += 15;
  else if (lead.valorImovel >= 200000) score += 8;
  else score += 3;

  // Relação entre valor desejado e estimativa de crédito: perto do teto
  // sinaliza operação bem dimensionada.
  if (lead.estimativaCredito && lead.valorDesejado) {
    const ratio = lead.valorDesejado / lead.estimativaCredito;
    if (ratio <= 1) score += 20;
    else if (ratio <= 1.3) score += 10;
    else score += 3;
  }

  // Situação do imóvel: quitado facilita a operação; financiamento baixo
  // (menos do limite configurado em aberto) ainda é uma operação boa.
  if (lead.situacaoImovel === 'quitado') score += 15;
  else if (lead.situacaoImovel === 'financiado_menos_30') score += 11;
  else score += 4;

  // Tipo de imóvel (múltipla escolha).
  const tipos = Array.isArray(lead.tipoImovel) ? lead.tipoImovel : [lead.tipoImovel].filter(Boolean);
  if (tipos.includes('casa') || tipos.includes('apartamento')) score += 15;
  else if (tipos.includes('terreno_condominio')) score += 12;
  else score += 6;

  // Renda mensal: quanto maior em relação ao piso configurado, maior a
  // capacidade de pagamento percebida pra operação.
  const rendaMinima = CONFIG.MIN_MONTHLY_INCOME || 1;
  const rendaRatio = lead.rendaMensal ? lead.rendaMensal / rendaMinima : 0;
  if (rendaRatio >= 10) score += 15;
  else if (rendaRatio >= 5) score += 12;
  else if (rendaRatio >= 2) score += 8;
  else if (rendaRatio > 0) score += 4;

  // Titularidade do imóvel: CNPJ costuma indicar operação empresarial,
  // com estrutura e urgência diferentes de uma pessoa física.
  if (lead.titularidadeImovel === 'cnpj') score += 10;
  else if (lead.titularidadeImovel === 'cpf') score += 7;

  return Math.min(100, score);
}


/* ===== js/crmIntegration.js ===== */
/**
 * crmIntegration.js
 * Envio de leads qualificados para o CRM.
 *
 * IMPORTANTE DE SEGURANÇA:
 * Nunca coloque a API key/token do CRM diretamente aqui ou em qualquer
 * arquivo do frontend. O valor certo é chamar um endpoint de backend
 * próprio (serverless function, backend da Acrópole, n8n etc.) que
 * guarda o token em variável de ambiente e repassa a chamada para o
 * CRM. Este módulo já está pronto para isso: basta configurar
 * CONFIG.CRM.webhookUrl apontando para esse backend.
 *
 * Enquanto webhookUrl não estiver configurado, o envio fica em modo
 * "dry run": os dados são apenas logados/guardados localmente, para não
 * quebrar a aplicação nem perder leads durante o desenvolvimento.
 */



const PENDING_KEY = 'he_leads_pending_sync';

// Se o webhook do CRM travar (sem responder, sem nem dar erro de rede), o
// fluxo não pode ficar esperando pra sempre: quem trava aqui é a tela de
// "calculando", e o lead nunca chegaria a ver o resultado. Esse timeout
// garante que, no pior caso, seguimos em frente tratando como falha comum.
const CRM_REQUEST_TIMEOUT_MS = 8000;

/**
 * @param {object} leadPayload payload vindo de leadStore.toCrmPayload()
 * @returns {Promise<{ sent: boolean, mode: 'live'|'dry-run', error?: string }>}
 */
async function sendLeadToCrm(leadPayload) {
  // Leads desqualificados (localização ou financiamento em aberto) nunca
  // vão para o CRM comercial.
  if (
    leadPayload.status === CONFIG.LEAD_STATUS.DISQUALIFIED_LOCATION ||
    leadPayload.status === CONFIG.LEAD_STATUS.DISQUALIFIED_FINANCING
  ) {
    return { sent: false, mode: 'skipped-disqualified' };
  }

  const enrichedPayload = {
    ...leadPayload,
    leadScore: scoreLead(leadPayload),
    appName: CONFIG.APP_NAME,
    pipeline: CONFIG.CRM.pipeline,
    stage: CONFIG.CRM.stage,
    campaignId: CONFIG.CRM.campaignId,
  };

  if (!CONFIG.CRM.webhookUrl) {
    storePendingLocally(enrichedPayload);
    return { sent: false, mode: 'dry-run' };
  }

  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), CRM_REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(CONFIG.CRM.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // O token de autenticação, se necessário, deve ser adicionado pelo
      // próprio backend/proxy identificado por webhookUrl — nunca aqui.
      body: JSON.stringify(enrichedPayload),
      signal: controller.signal,
    });

    if (!response.ok) {
      storePendingLocally(enrichedPayload);
      return { sent: false, mode: 'live', error: `HTTP ${response.status}` };
    }

    return { sent: true, mode: 'live' };
  } catch (error) {
    storePendingLocally(enrichedPayload);
    const isTimeout = error && error.name === 'AbortError';
    return { sent: false, mode: 'live', error: isTimeout ? 'timeout' : String(error) };
  } finally {
    window.clearTimeout(timeoutId);
  }
}

function storePendingLocally(payload) {
  try {
    const raw = localStorage.getItem(PENDING_KEY);
    const list = raw ? JSON.parse(raw) : [];
    list.push(payload);
    localStorage.setItem(PENDING_KEY, JSON.stringify(list));
  } catch (_) {
    /* localStorage indisponível: melhor esforço, não bloqueia o funil */
  }
}

/** Utilitário para reenviar leads que ficaram pendentes localmente. */
function getPendingLeads() {
  try {
    const raw = localStorage.getItem(PENDING_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (_) {
    return [];
  }
}

function clearPendingLeads() {
  try {
    localStorage.removeItem(PENDING_KEY);
  } catch (_) {}
}

/**
 * Tenta reenviar ao CRM os leads que ficaram pendentes localmente (porque o
 * webhook falhou, deu timeout, ou não estava configurado numa visita
 * anterior). Sem isso, getPendingLeads()/clearPendingLeads() nunca eram
 * chamadas por ninguém: um lead que falhasse ficava preso no localStorage
 * daquele navegador para sempre, sem nenhuma tentativa de reenvio — ou
 * seja, um problema temporário no CRM/n8n virava perda silenciosa e
 * definitiva do lead (o time comercial nunca saberia que ele existiu).
 * Chamada uma vez no início da aplicação (ver app.js), sem bloquear o
 * carregamento do funil: é "melhor esforço", roda em segundo plano.
 * @returns {Promise<void>}
 */
async function flushPendingLeads() {
  if (!CONFIG.CRM.webhookUrl) return;

  const pending = getPendingLeads();
  if (pending.length === 0) return;

  const stillPending = [];
  for (const payload of pending) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), CRM_REQUEST_TIMEOUT_MS);
    try {
      const response = await fetch(CONFIG.CRM.webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      if (!response.ok) stillPending.push(payload);
    } catch (_) {
      stillPending.push(payload);
    } finally {
      window.clearTimeout(timeoutId);
    }
  }

  try {
    if (stillPending.length > 0) {
      localStorage.setItem(PENDING_KEY, JSON.stringify(stillPending));
    } else {
      clearPendingLeads();
    }
  } catch (_) {
    /* localStorage indisponível: melhor esforço */
  }
}


/* ===== js/ui-components.js ===== */
/**
 * ui-components.js
 * Peças de interface reutilizáveis: máscaras de campo, barra de
 * progresso e cards de opção. Sem lógica de negócio aqui.
 */


function attachCurrencyMask(inputEl) {
  inputEl.setAttribute('inputmode', 'numeric');
  inputEl.addEventListener('input', () => {
    const caretWasAtEnd =
      inputEl.selectionStart === inputEl.value.length;
    inputEl.value = maskCurrencyInput(inputEl.value);
    if (caretWasAtEnd) {
      inputEl.selectionStart = inputEl.selectionEnd = inputEl.value.length;
    }
  });
}

function attachPhoneMask(inputEl) {
  inputEl.setAttribute('inputmode', 'numeric');
  inputEl.addEventListener('input', () => {
    inputEl.value = maskPhone(inputEl.value);
  });
}

/**
 * Atualiza a barra de progresso do quiz.
 * @param {HTMLElement} trackEl elemento .progress-fill
 * @param {HTMLElement} labelEl elemento .quiz-step-label
 * @param {number} currentStep 1-based
 * @param {number} totalSteps
 */
function updateProgress(fillEl, labelEl, currentStep, totalSteps) {
  const pct = Math.round((currentStep / totalSteps) * 100);
  fillEl.style.width = `${pct}%`;
  labelEl.textContent = `Etapa ${currentStep} de ${totalSteps}`;
}

/**
 * Renderiza um grupo de cards de seleção única.
 * @param {HTMLElement} containerEl
 * @param {{ value: string, label: string, icon?: string }[]} options
 * @param {string|null} selectedValue
 * @param {(value: string) => void} onSelect
 */
function renderOptionCards(containerEl, options, selectedValue, onSelect) {
  containerEl.innerHTML = '';
  options.forEach((opt) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'option-card' + (opt.value === selectedValue ? ' is-selected' : '');
    btn.setAttribute('data-value', opt.value);
    // aria-pressed avisa tecnologia assistiva que isto é um botão de
    // alternância com estado (selecionado ou não) — sem isso, um leitor de
    // tela só anuncia "botão", sem dizer se a opção já está marcada.
    btn.setAttribute('aria-pressed', String(opt.value === selectedValue));
    btn.innerHTML = `
      ${opt.icon ? `<span class="option-icon">${opt.icon}</span>` : ''}
      <span class="option-label">${opt.label}</span>
      <span class="option-check">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>
      </span>
    `;
    btn.addEventListener('click', () => onSelect(opt.value));
    containerEl.appendChild(btn);
  });
}

/**
 * Renderiza um grupo de cards de opção com "foto" ilustrada, usado quando
 * cada opção precisa de mais destaque visual (ex.: tipo do imóvel) e pode
 * estar marcada como não aceita (exibida esmaecida, sem poder ser
 * selecionada). Suporta múltipla escolha: `selectedValues` é sempre um
 * array com os valores marcados no momento.
 * @param {HTMLElement} containerEl
 * @param {{ value: string, label: string, media?: string, accepted?: boolean }[]} options
 * @param {string[]} selectedValues
 * @param {(value: string) => void} onSelect
 * @param {(opt: object) => void} [onBlockedSelect] chamado ao clicar numa opção não aceita
 * @param {{ showBadge?: boolean }} [config] showBadge:false omite o selo "Aceito/Não aceito"
 *   — usado em telas onde a opção é só informativa (ex.: rua ou condomínio),
 *   sem nenhuma noção de aceite/rejeição, pra não sugerir o contrário.
 */
function renderPhotoOptionCards(containerEl, options, selectedValues, onSelect, onBlockedSelect, config = {}) {
  const showBadge = config.showBadge !== false;
  containerEl.innerHTML = '';
  const selected = selectedValues || [];
  options.forEach((opt) => {
    const isBlocked = opt.accepted === false;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'option-photo-card' + (selected.includes(opt.value) ? ' is-selected' : '') + (isBlocked ? ' is-disabled' : '');
    btn.setAttribute('data-value', opt.value);
    if (isBlocked) btn.setAttribute('aria-disabled', 'true');
    // aria-pressed pelo mesmo motivo de renderOptionCards acima.
    btn.setAttribute('aria-pressed', String(selected.includes(opt.value)));
    btn.innerHTML = `
      <span class="option-photo-media">
        ${opt.media || ''}
        ${showBadge ? `<span class="option-photo-badge ${isBlocked ? 'is-no' : 'is-yes'}">${isBlocked ? 'Não aceito' : 'Aceito'}</span>` : ''}
        <span class="option-photo-check">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>
        </span>
      </span>
      <span class="option-photo-label">${opt.label}</span>
    `;
    btn.addEventListener('click', () => {
      if (isBlocked) {
        if (onBlockedSelect) onBlockedSelect(opt);
        return;
      }
      onSelect(opt.value);
    });
    containerEl.appendChild(btn);
  });
}

function setFieldError(fieldEl, errorEl, message) {
  // aria-invalid no <input> (quando existir dentro de fieldEl) avisa
  // tecnologia assistiva que o campo está em estado de erro; o texto em si
  // já é lido automaticamente porque errorEl tem role="alert" no HTML.
  const inputEl = fieldEl.querySelector('input');
  if (message) {
    fieldEl.classList.add('has-error');
    errorEl.textContent = message;
    if (inputEl) inputEl.setAttribute('aria-invalid', 'true');
  } else {
    fieldEl.classList.remove('has-error');
    errorEl.textContent = '';
    if (inputEl) inputEl.removeAttribute('aria-invalid');
  }
}

/**
 * Indicador de rolagem: injeta um degradê no topo e/ou no fundo de todo
 * container que pode rolar por dentro (.step-body e as telas finais),
 * para deixar claro que existe mais conteúdo abaixo/acima em vez de a
 * última linha simplesmente parecer cortada.
 */
const SCROLL_FADE_SELECTOR = '.step-body, .screen-inner.end-screen';

function initScrollFades() {
  document.querySelectorAll(SCROLL_FADE_SELECTOR).forEach((region) => {
    if (region.dataset.fadeInit) return;
    region.dataset.fadeInit = '1';

    const topFade = document.createElement('div');
    topFade.className = 'scroll-fade scroll-fade-top';
    const bottomFade = document.createElement('div');
    bottomFade.className = 'scroll-fade scroll-fade-bottom';
    region.appendChild(topFade);
    region.appendChild(bottomFade);

    region.addEventListener('scroll', () => updateScrollFade(region), { passive: true });
  });

  if (!window.__heScrollFadeResizeBound) {
    window.__heScrollFadeResizeBound = true;
    window.addEventListener('resize', updateAllScrollFades);
  }
}

function updateScrollFade(region) {
  if (!region) return;
  const hasMoreTop = region.scrollTop > 4;
  const hasMoreBottom = region.scrollTop + region.clientHeight < region.scrollHeight - 4;
  region.classList.toggle('has-fade-top', hasMoreTop);
  region.classList.toggle('has-fade-bottom', hasMoreBottom);
}

function updateAllScrollFades() {
  document.querySelectorAll(SCROLL_FADE_SELECTOR).forEach(updateScrollFade);
}


/* ===== js/quiz.js ===== */
/**
 * quiz.js
 * Máquina de estados do funil: navegação entre telas, validação de cada
 * passo, orquestração dos serviços (busca de cidade, população, cálculo, CRM).
 */











const QUESTION_STEPS = [
  'property-type',
  'property-value',
  'city',
  'property-status',
  'income-ownership',
  'desired-amount',
  'lead-name',
  'lead-whatsapp',
  'lead-email',
];

// Duração da tela "calculando" (ms) e mensagens que se alternam nela,
// para reforçar a sensação de que a simulação está sendo processada.
const CALCULATING_DURATION_MS = 4000;
const CALCULATING_MESSAGES = [
  'Validando suas informações...',
  'Consultando condições disponíveis...',
  'Calculando sua estimativa...',
];

// Fotos reais da Acrópole para as opções da etapa 3 (tipo do imóvel),
// embutidas em base64 para manter o arquivo único autocontido, sem
// depender de rede.
const CASA_PHOTO_DATA_URI = 'assets/img/simulador/casa.jpg';

const APARTAMENTO_PHOTO_DATA_URI = 'assets/img/simulador/apartamento.jpg';

const TERRENO_CONDOMINIO_PHOTO_DATA_URI = 'assets/img/simulador/terreno-condominio.jpg';

const GALPAO_PHOTO_DATA_URI = 'assets/img/simulador/galpao.jpg';

// Fotos reais da Acrópole para as 4 combinações de localização (etapa 1b:
// rua/condomínio, tanto pra casa quanto pra terreno). Mesmo padrão das
// constantes acima: base64 embutido, sem depender de rede.
const LOCATION_CASA_RUA_PHOTO_DATA_URI = 'assets/img/simulador/local-casa-rua.jpg';

const LOCATION_CASA_CONDOMINIO_PHOTO_DATA_URI = 'assets/img/simulador/local-casa-condominio.jpg';

const LOCATION_TERRENO_RUA_PHOTO_DATA_URI = 'assets/img/simulador/local-terreno-rua.jpg';

const LOCATION_TERRENO_CONDOMINIO_PHOTO_DATA_URI = 'assets/img/simulador/local-terreno-condominio.jpg';

const PROPERTY_SCENES = {
  // draggable="false" bloqueia arrastar/soltar (o menu de contexto por atributo inline foi removido: a CSP bloqueia) e o menu de
  // clique-direito "Salvar imagem como..."; o reforço para toque longo no
  // celular (que abre "Salvar imagem" sem clique-direito) fica no CSS,
  // via -webkit-touch-callout: none em .option-photo-media img.
  casa: `<img src="${CASA_PHOTO_DATA_URI}" alt="" width="360" height="252" draggable="false" decoding="async" loading="lazy" />`,
  apartamento: `<img src="${APARTAMENTO_PHOTO_DATA_URI}" alt="" width="360" height="252" draggable="false" decoding="async" loading="lazy" />`,
  terrenoCondominio: `<img src="${TERRENO_CONDOMINIO_PHOTO_DATA_URI}" alt="" width="360" height="252" draggable="false" decoding="async" loading="lazy" />`,
  galpao: `<img src="${GALPAO_PHOTO_DATA_URI}" alt="" width="360" height="252" draggable="false" decoding="async" loading="lazy" />`,
};

const PROPERTY_TYPE_OPTIONS = [
  { value: 'casa', label: 'Casa', media: PROPERTY_SCENES.casa, accepted: true },
  { value: 'apartamento', label: 'Apartamento', media: PROPERTY_SCENES.apartamento, accepted: true },
  { value: 'terreno_condominio', label: 'Terreno', media: PROPERTY_SCENES.terrenoCondominio, accepted: true },
  { value: 'galpao', label: 'Outros', media: PROPERTY_SCENES.galpao, accepted: false },
];

// Situação do financiamento do imóvel (etapa 4). A regra de negócio:
// quitado ou com menos de CONFIG.MAX_OPEN_FINANCING_PERCENTAGE em aberto
// segue no funil; com esse percentual ou mais em aberto, desqualifica.
const OPEN_FINANCING_THRESHOLD_PCT = Math.round(CONFIG.MAX_OPEN_FINANCING_PERCENTAGE * 100);
const PROPERTY_STATUS_OPTIONS = [
  { value: 'quitado', label: 'Sim, está quitado' },
  { value: 'financiado_menos_30', label: `Não, mas falta menos de ${OPEN_FINANCING_THRESHOLD_PCT}% de financiamento` },
  { value: 'financiado_mais_30', label: `Não, ainda falta mais de ${OPEN_FINANCING_THRESHOLD_PCT}% de financiamento` },
];

const DISQUALIFYING_PROPERTY_STATUS = 'financiado_mais_30';

// Titularidade do imóvel (nova etapa: renda + titularidade). Só define em
// nome de quem o imóvel está registrado, sem regra de desqualificação —
// informação usada mais adiante na análise/CRM.
const OWNERSHIP_OPTIONS = [
  { value: 'cpf', label: 'CPF (pessoa física)' },
  { value: 'cnpj', label: 'CNPJ (pessoa jurídica)' },
];


let el = {}; // cache de elementos DOM, populado em initQuiz()
let currentQuestionIndex = 0;
let selections = { tipoImovel: [], situacaoImovel: '', titularidadeImovel: '' };

// Subfluxo de localização (rua/condomínio), disparado depois da etapa 1
// quando "Casa" e/ou "Terreno" estiverem entre os tipos selecionados. Não
// desqualifica o lead em nenhuma resposta — é só um dado extra pra
// inteligência comercial. locationSubQueue guarda, na ordem, quais
// subtelas mostrar (0 a 2); locationSubIndex marca em qual delas o lead
// está agora, e -1 significa "fora do subfluxo".
const LOCATION_TYPE_OPTIONS = [
  { value: 'rua', label: 'Na rua' },
  { value: 'condominio', label: 'Em condomínio' },
];

// Fotos reais da Acrópole para as 4 combinações de localização (mesmo
// padrão de PROPERTY_SCENES: constantes "..._PHOTO_DATA_URI" em base64,
// ver acima).
const LOCATION_SCENES = {
  casaRua: `<img src="${LOCATION_CASA_RUA_PHOTO_DATA_URI}" alt="" width="480" height="336" draggable="false" decoding="async" loading="lazy" />`,
  casaCondominio: `<img src="${LOCATION_CASA_CONDOMINIO_PHOTO_DATA_URI}" alt="" width="480" height="336" draggable="false" decoding="async" loading="lazy" />`,
  terrenoRua: `<img src="${LOCATION_TERRENO_RUA_PHOTO_DATA_URI}" alt="" width="480" height="336" draggable="false" decoding="async" loading="lazy" />`,
  terrenoCondominio: `<img src="${LOCATION_TERRENO_CONDOMINIO_PHOTO_DATA_URI}" alt="" width="480" height="336" draggable="false" decoding="async" loading="lazy" />`,
};

const LOCATION_CASA_PHOTO_OPTIONS = [
  { value: 'rua', label: 'Na rua', media: LOCATION_SCENES.casaRua, accepted: true },
  { value: 'condominio', label: 'Em condomínio', media: LOCATION_SCENES.casaCondominio, accepted: true },
];
const LOCATION_TERRENO_PHOTO_OPTIONS = [
  { value: 'rua', label: 'Na rua', media: LOCATION_SCENES.terrenoRua, accepted: true },
  { value: 'condominio', label: 'Em condomínio', media: LOCATION_SCENES.terrenoCondominio, accepted: true },
];

let locationSubQueue = [];
let locationSubIndex = -1;

// Link do WhatsApp com o resumo do lead, calculado em setupWhatsappCta() e
// lido no clique do botão de resultado (bindResultScreen). Não existe mais
// uma tela de confirmação com um <a> pra guardar esse valor no DOM.
let whatsappCtaHref = '';

function initQuiz() {
  // Pré-carrega a base de municípios sem disputar com a primeira pintura.
  const __pre = () => { ensureCities().catch(() => {}); };
  if ('requestIdleCallback' in window) requestIdleCallback(__pre, { timeout: 3000 }); else setTimeout(__pre, 1500);
  // Embutido no site (?embed=1): Esc também fecha a janela, mesmo com o foco aqui dentro.
  if (/[?&]embed=1\b/.test(location.search) && window.parent !== window) {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { try { window.parent.postMessage({ type: 'acropole:sim-close' }, location.origin); } catch (_) {} }
    });
  }
  cacheElements();
  initScrollFades();
  bindLandingScreen();
  bindPropertyValueStep();
  bindCityStep();
  bindPropertyTypeStep();
  bindLocationCasaStep();
  bindLocationTerrenoStep();
  bindPropertyStatusStep();
  bindIncomeOwnershipStep();
  bindDesiredAmountStep();
  bindLeadNameStep();
  bindLeadWhatsappStep();
  bindLeadEmailStep();
  bindResultScreen();
  bindDisqualifiedScreen();

  leadStore.captureUtms();
  startAttributionCapture();
  goToScreen('screen-landing');
}

function cacheElements() {
  el = {
    header: document.getElementById('quiz-header'),
    progressFill: document.getElementById('progress-fill'),
    stepLabel: document.getElementById('quiz-step-label'),
    backBtn: document.getElementById('quiz-back-btn'),

    startBtn: document.getElementById('start-quiz-btn'),

    propertyValueInput: document.getElementById('input-property-value'),
    propertyValueField: document.getElementById('field-property-value'),
    propertyValueError: document.getElementById('error-property-value'),
    propertyValueNextBtn: document.getElementById('btn-property-value-next'),

    cityInput: document.getElementById('input-city'),
    cityField: document.getElementById('field-city'),
    cityError: document.getElementById('error-city'),
    cityResults: document.getElementById('city-results'),
    cityNextBtn: document.getElementById('btn-city-next'),
    citySelectedCard: document.getElementById('city-selected-card'),
    citySelectedName: document.getElementById('city-selected-name'),

    propertyTypeOptions: document.getElementById('options-property-type'),
    propertyTypeNextBtn: document.getElementById('btn-property-type-next'),

    locationCasaOptions: document.getElementById('options-location-casa'),
    locationCasaNextBtn: document.getElementById('btn-location-casa-next'),

    locationTerrenoOptions: document.getElementById('options-location-terreno'),
    locationTerrenoNextBtn: document.getElementById('btn-location-terreno-next'),

    propertyStatusOptions: document.getElementById('options-property-status'),
    propertyStatusNextBtn: document.getElementById('btn-property-status-next'),

    incomeInput: document.getElementById('input-income'),
    incomeField: document.getElementById('field-income'),
    incomeError: document.getElementById('error-income'),
    ownershipOptions: document.getElementById('options-ownership'),
    ownershipField: document.getElementById('field-ownership'),
    ownershipError: document.getElementById('error-ownership'),
    incomeOwnershipNextBtn: document.getElementById('btn-income-ownership-next'),

    desiredAmountInput: document.getElementById('input-desired-amount'),
    desiredAmountField: document.getElementById('field-desired-amount'),
    desiredAmountError: document.getElementById('error-desired-amount'),
    desiredAmountNextBtn: document.getElementById('btn-desired-amount-next'),

    resultPropertyValue: document.getElementById('result-property-value'),
    resultPercentage: document.getElementById('result-percentage'),
    resultEstimatedCredit: document.getElementById('result-estimated-credit'),
    resultDesiredAmount: document.getElementById('result-desired-amount'),
    resultInstallmentLabel: document.getElementById('result-installment-label'),
    resultInstallment: document.getElementById('result-installment'),
    resultDisclaimer: document.getElementById('result-disclaimer'),
    resultRate: document.getElementById('result-rate'),
    resultCtaBtn: document.getElementById('btn-result-cta'),

    leadNameInput: document.getElementById('input-lead-name'),
    leadNameField: document.getElementById('field-lead-name'),
    leadNameError: document.getElementById('error-lead-name'),
    leadNameNextBtn: document.getElementById('btn-lead-name-next'),

    leadWhatsappInput: document.getElementById('input-lead-whatsapp'),
    leadWhatsappField: document.getElementById('field-lead-whatsapp'),
    leadWhatsappError: document.getElementById('error-lead-whatsapp'),
    leadWhatsappNextBtn: document.getElementById('btn-lead-whatsapp-next'),

    leadEmailInput: document.getElementById('input-lead-email'),
    leadEmailField: document.getElementById('field-lead-email'),
    leadEmailError: document.getElementById('error-lead-email'),
    leadEmailNextBtn: document.getElementById('btn-lead-email-next'),
    leadSubmitError: document.getElementById('lead-submit-error'),

    calcRingProgress: document.getElementById('calc-ring-progress'),
    calcPercent: document.getElementById('calc-percent'),
    calcStatusText: document.getElementById('calc-status-text'),

    disqualifiedTitle: document.getElementById('disqualified-title'),
    disqualifiedText1: document.getElementById('disqualified-text-1'),
    disqualifiedText2: document.getElementById('disqualified-text-2'),
    disqualifiedText3: document.getElementById('disqualified-text-3'),
    disqualifiedCloseBtn: document.getElementById('btn-disqualified-close'),
  };
}

// ---------- Navegação entre telas ----------

function goToScreen(screenId) {
  document.querySelectorAll('.screen').forEach((s) => s.classList.remove('is-active'));
  const target = document.getElementById(screenId);
  target.classList.add('is-active');
  window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });

  // As subtelas de localização (rua/condomínio) não fazem parte de
  // QUESTION_STEPS (são condicionais, 0 a 2 conforme o tipo de imóvel
  // marcado), mas precisam do mesmo cabeçalho com botão de voltar.
  const isQuestionScreen =
    QUESTION_STEPS.some((s) => `screen-${s}` === screenId) ||
    screenId === 'screen-location-casa' ||
    screenId === 'screen-location-terreno';
  el.header.classList.toggle('hidden', !isQuestionScreen);

  // Reinicia a rolagem interna da tela (caso o usuário tenha rolado numa
  // visita anterior) e recalcula o degradê de "tem mais conteúdo" agora
  // que a tela está de fato visível e com altura mensurável.
  target.querySelectorAll('.step-body, .screen-inner.end-screen').forEach((region) => {
    region.scrollTop = 0;
  });
  window.requestAnimationFrame(updateAllScrollFades);
}

// Mensagens da tela de desqualificação, de acordo com o motivo. Mantém um
// único par de telas/markup para os dois motivos de desqualificação
// possíveis hoje (localização e financiamento em aberto), trocando só o
// texto — evita duplicar HTML/CSS para uma tela que é visualmente igual.
// text2 pode ser string fixa ou função(params) -> string, para permitir
// personalizar a mensagem com dados do lead (ex.: nome da cidade digitada).
const DISQUALIFIED_MESSAGES = {
  location: {
    title: 'Obrigado pelo seu interesse!',
    text1: 'Agradecemos muito o seu contato.',
    text2: (params) =>
      `No momento, infelizmente ainda não atendemos ${params.cityLabel || 'o seu município'}, por isso não conseguimos realizar uma simulação para a sua região.`,
    text3: 'Esperamos poder atender você em uma próxima oportunidade.',
  },
  financing: {
    title: 'Obrigado pelo seu interesse!',
    text1: 'Agradecemos muito o seu contato.',
    text2:
      'No momento, infelizmente não conseguimos prosseguir com simulações para imóveis com esse valor de financiamento em aberto.',
    text3: 'Esperamos poder atender você em uma próxima oportunidade.',
  },
};

function showDisqualifiedScreen(reason, params = {}) {
  const messages = DISQUALIFIED_MESSAGES[reason] || DISQUALIFIED_MESSAGES.location;
  const resolve = (value) => (typeof value === 'function' ? value(params) : value);
  el.disqualifiedTitle.textContent = resolve(messages.title);
  el.disqualifiedText1.textContent = resolve(messages.text1);
  el.disqualifiedText2.textContent = resolve(messages.text2);
  el.disqualifiedText3.textContent = resolve(messages.text3);
  goToScreen('screen-disqualified');
}

// A pessoa foi desqualificada e não tem mais nenhuma etapa a seguir, então
// oferecemos um botão explícito pra fechar a aba/janela. window.close() só
// funciona de fato em abas abertas via script (ex.: link de anúncio abrindo
// em nova aba); em uma aba aberta normalmente pelo navegador, ele é
// silenciosamente ignorado — não há erro, só não fecha nada.
function bindDisqualifiedScreen() {
  if (!el.disqualifiedCloseBtn) return;
  el.disqualifiedCloseBtn.addEventListener('click', () => {
    window.close();
  });
}

function showQuestionStep(index) {
  currentQuestionIndex = index;
  const stepName = QUESTION_STEPS[index];
  updateProgress(el.progressFill, el.stepLabel, index + 1, QUESTION_STEPS.length);
  goToScreen(`screen-${stepName}`);
}

function goBack() {
  if (currentQuestionIndex > 0) {
    showQuestionStep(currentQuestionIndex - 1);
  } else {
    goToScreen('screen-landing');
  }
}

// ---------- Subfluxo: localização (rua/condomínio) ----------

/** Monta a fila de subtelas com base nos tipos marcados e mostra a primeira,
 * ou pula direto pra próxima etapa principal se nenhuma se aplica. */
function startLocationSubflowOrContinue() {
  locationSubQueue = [];
  if (selections.tipoImovel.includes('casa')) locationSubQueue.push('location-casa');
  if (selections.tipoImovel.includes('terreno_condominio')) locationSubQueue.push('location-terreno');

  if (locationSubQueue.length === 0) {
    locationSubIndex = -1;
    showQuestionStep(currentQuestionIndex + 1);
    return;
  }

  locationSubIndex = 0;
  goToScreen(`screen-${locationSubQueue[locationSubIndex]}`);
}

/** Chamada ao confirmar uma subtela: avança pra próxima da fila, ou volta
 * pro fluxo principal quando a fila acaba. */
function advanceLocationSubflow() {
  locationSubIndex += 1;
  if (locationSubIndex < locationSubQueue.length) {
    goToScreen(`screen-${locationSubQueue[locationSubIndex]}`);
  } else {
    locationSubQueue = [];
    locationSubIndex = -1;
    showQuestionStep(currentQuestionIndex + 1);
  }
}

/** Botão "voltar" enquanto estiver dentro do subfluxo: volta pra subtela
 * anterior da fila, ou pra etapa "tipo do imóvel" se for a primeira. */
function goBackFromLocationSubflow() {
  if (locationSubIndex <= 0) {
    locationSubQueue = [];
    locationSubIndex = -1;
    showQuestionStep(currentQuestionIndex);
  } else {
    locationSubIndex -= 1;
    goToScreen(`screen-${locationSubQueue[locationSubIndex]}`);
  }
}

// ---------- Landing ----------

function bindLandingScreen() {
  el.startBtn.addEventListener('click', () => {
    analytics.track(analytics.EVENTS.QUIZ_STARTED);
    leadStore.reset();
    leadStore.captureUtms();
    currentQuestionIndex = 0;
    showQuestionStep(0);
  });

  el.backBtn.addEventListener('click', () => {
    if (locationSubIndex !== -1) {
      goBackFromLocationSubflow();
    } else {
      goBack();
    }
  });
}

// ---------- Passo 2: valor do imóvel ----------

function bindPropertyValueStep() {
  attachCurrencyMask(el.propertyValueInput);

  el.propertyValueNextBtn.addEventListener('click', () => {
    const value = parseCurrencyToNumber(el.propertyValueInput.value);

    if (!el.propertyValueInput.value) {
      setFieldError(el.propertyValueField, el.propertyValueError, FRIENDLY_ERRORS.propertyValueEmpty);
      return;
    }
    if (!isValidPropertyValue(value)) {
      setFieldError(el.propertyValueField, el.propertyValueError, FRIENDLY_ERRORS.propertyValueInvalid);
      return;
    }

    setFieldError(el.propertyValueField, el.propertyValueError, null);
    leadStore.update({ valorImovel: value });
    analytics.track(analytics.EVENTS.PROPERTY_VALUE_COMPLETED, { valor: value });
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 3: cidade ----------

function bindCityStep() {
  el.cityNextBtn.disabled = true;
  let selectedCity = null;

  const hideResults = () => {
    el.cityResults.innerHTML = '';
    el.cityResults.classList.add('hidden');
  };

  const selectCity = (city) => {
    selectedCity = city;
    hideResults();
    el.cityInput.value = `${city.nome} - ${city.uf}`;
    el.citySelectedName.textContent = `${city.nome}, ${city.uf}`;
    el.citySelectedCard.classList.remove('hidden');
    el.cityNextBtn.disabled = false;
    setFieldError(el.cityField, el.cityError, null);
    analytics.track(analytics.EVENTS.CITY_SELECTED, { municipio: city.nome, estado: city.uf });
  };

  const clearSelection = () => {
    selectedCity = null;
    el.citySelectedCard.classList.add('hidden');
    el.cityNextBtn.disabled = true;
  };

  el.cityInput.addEventListener('input', () => {
    clearSelection();
    setFieldError(el.cityField, el.cityError, null);

    if (!el.cityInput.value || el.cityInput.value.trim().length < 2) {
      hideResults();
      return;
    }

    if (!indexedCities) {
      el.cityResults.innerHTML = '<div class="city-results-empty">Carregando a lista de cidades...</div>';
      el.cityResults.classList.remove('hidden');
      ensureCities()
        .then(() => { if (el.cityInput.value.trim().length >= 2) el.cityInput.dispatchEvent(new Event('input')); })
        .catch(() => {
          el.cityResults.innerHTML = '<div class="city-results-empty">Não foi possível carregar a lista de cidades. Verifique a conexão e tente de novo.</div>';
        });
      return;
    }

    const results = searchCities(el.cityInput.value, 8);

    if (results.length === 0) {
      el.cityResults.innerHTML = '<div class="city-results-empty">Nenhuma cidade encontrada</div>';
      el.cityResults.classList.remove('hidden');
      return;
    }

    el.cityResults.innerHTML = '';
    results.forEach((city) => {
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'city-result-item';
      item.innerHTML = `<span class="city-result-name">${city.nome}</span><span class="city-result-uf">${city.uf}</span>`;
      item.addEventListener('click', () => selectCity(city));
      el.cityResults.appendChild(item);
    });
    el.cityResults.classList.remove('hidden');
  });

  el.cityInput.addEventListener('focus', () => {
    if (!selectedCity && el.cityInput.value.trim().length >= 2) {
      el.cityInput.dispatchEvent(new Event('input'));
    }
  });

  document.addEventListener('click', (event) => {
    if (!el.cityField.contains(event.target)) {
      hideResults();
    }
  });

  el.cityNextBtn.addEventListener('click', async () => {
    if (!selectedCity) return;

    leadStore.update({
      municipio: selectedCity.nome,
      estado: selectedCity.uf,
      ibgeCode: selectedCity.ibge,
    });

    el.cityNextBtn.disabled = true;
    const originalLabel = el.cityNextBtn.innerHTML;
    el.cityNextBtn.innerHTML = '<span class="spinner"></span> Verificando disponibilidade...';
    // Trava o botão de voltar durante a checagem assíncrona para evitar que o
    // lead saia da tela no meio da consulta (o que deixaria o próximo clique
    // em "avançar" reagindo a um resultado de uma cidade que não é mais a
    // exibida na tela).
    const backBtnWasDisabled = el.backBtn.disabled;
    el.backBtn.disabled = true;

    const qualification = await qualifyByLocation({
      municipio: selectedCity.nome,
      estado: selectedCity.uf,
      ibgeCode: selectedCity.ibge,
    });

    leadStore.update({
      populacaoEstimada: qualification.population,
      populationSource: qualification.populationSource,
      status: qualification.status,
    });

    el.cityNextBtn.innerHTML = originalLabel;
    el.cityNextBtn.disabled = false;
    el.backBtn.disabled = backBtnWasDisabled;

    if (!qualification.qualified) {
      analytics.track(analytics.EVENTS.LOCATION_DISQUALIFIED, {
        municipio: selectedCity.nome,
        estado: selectedCity.uf,
      });
      showDisqualifiedScreen('location', { cityLabel: `${selectedCity.nome} - ${selectedCity.uf}` });
      return;
    }

    analytics.track(analytics.EVENTS.LOCATION_QUALIFIED, {
      municipio: selectedCity.nome,
      estado: selectedCity.uf,
    });
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 1: tipo do imóvel ----------

function bindPropertyTypeStep() {
  el.propertyTypeNextBtn.disabled = true;

  const render = () => {
    renderPhotoOptionCards(
      el.propertyTypeOptions,
      PROPERTY_TYPE_OPTIONS,
      selections.tipoImovel,
      (value) => {
        // Seleção única: escolher uma opção sempre SUBSTITUI a anterior,
        // nunca acumula. selections.tipoImovel continua sendo um array (o
        // resto do código, incluindo o subfluxo de localização e o
        // resumo do WhatsApp, já espera um array) — só que agora com no
        // máximo 1 item.
        selections.tipoImovel = [value];
        el.propertyTypeNextBtn.disabled = false;
        render();
      }
      // Sem onBlockedSelect: clicar numa opção "Não aceito" simplesmente não
      // faz nada (o card já mostra o selo "Não aceito"), sem exibir nenhum
      // texto de aviso adicional na tela.
    );
  };
  render();

  el.propertyTypeNextBtn.addEventListener('click', () => {
    if (selections.tipoImovel.length === 0) return;
    leadStore.update({ tipoImovel: selections.tipoImovel });
    startLocationSubflowOrContinue();
  });
}

// ---------- Subetapas: localização da casa / do terreno (rua ou condomínio) ----------
// Nenhuma resposta aqui desqualifica o lead — é só um dado a mais pra
// inteligência comercial (ver comentário no topo do arquivo).

function bindLocationCasaStep() {
  el.locationCasaNextBtn.disabled = true;
  let value = '';

  const render = () => {
    renderPhotoOptionCards(
      el.locationCasaOptions,
      LOCATION_CASA_PHOTO_OPTIONS,
      [value],
      (v) => {
        value = v;
        el.locationCasaNextBtn.disabled = false;
        render();
      },
      null,
      { showBadge: false }
    );
  };
  render();

  el.locationCasaNextBtn.addEventListener('click', () => {
    if (!value) return;
    leadStore.update({ localizacaoCasa: value });
    analytics.track(analytics.EVENTS.PROPERTY_LOCATION_TYPE_COMPLETED, { tipo: 'casa', localizacao: value });
    advanceLocationSubflow();
  });
}

function bindLocationTerrenoStep() {
  el.locationTerrenoNextBtn.disabled = true;
  let value = '';

  const render = () => {
    renderPhotoOptionCards(
      el.locationTerrenoOptions,
      LOCATION_TERRENO_PHOTO_OPTIONS,
      [value],
      (v) => {
        value = v;
        el.locationTerrenoNextBtn.disabled = false;
        render();
      },
      null,
      { showBadge: false }
    );
  };
  render();

  el.locationTerrenoNextBtn.addEventListener('click', () => {
    if (!value) return;
    leadStore.update({ localizacaoTerreno: value });
    analytics.track(analytics.EVENTS.PROPERTY_LOCATION_TYPE_COMPLETED, { tipo: 'terreno', localizacao: value });
    advanceLocationSubflow();
  });
}

// ---------- Passo 4: situação do imóvel ----------

function bindPropertyStatusStep() {
  el.propertyStatusNextBtn.disabled = true;

  const render = (selected) => {
    renderOptionCards(el.propertyStatusOptions, PROPERTY_STATUS_OPTIONS, selected, (value) => {
      selections.situacaoImovel = value;
      el.propertyStatusNextBtn.disabled = false;
      render(value);
    });
  };
  render(null);

  el.propertyStatusNextBtn.addEventListener('click', () => {
    const status = selections.situacaoImovel;

    // Financiamento em aberto igual ou acima do limite: desqualifica.
    // Nunca vai para o CRM comercial (ver crmIntegration.js), assim como
    // a desqualificação por localização.
    if (status === DISQUALIFYING_PROPERTY_STATUS) {
      leadStore.update({
        situacaoImovel: status,
        status: CONFIG.LEAD_STATUS.DISQUALIFIED_FINANCING,
      });
      analytics.track(analytics.EVENTS.FINANCING_DISQUALIFIED, { situacaoImovel: status });
      showDisqualifiedScreen('financing');
      return;
    }

    leadStore.update({
      situacaoImovel: status,
      status: CONFIG.LEAD_STATUS.QUALIFIED,
    });
    analytics.track(analytics.EVENTS.PROPERTY_STATUS_COMPLETED, { situacaoImovel: status });
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 5: renda e titularidade do imóvel ----------

function bindIncomeOwnershipStep() {
  attachCurrencyMask(el.incomeInput);

  const renderOwnership = (selected) => {
    renderOptionCards(el.ownershipOptions, OWNERSHIP_OPTIONS, selected, (value) => {
      selections.titularidadeImovel = value;
      setFieldError(el.ownershipField, el.ownershipError, null);
      renderOwnership(value);
    });
  };
  renderOwnership(null);

  el.incomeOwnershipNextBtn.addEventListener('click', () => {
    const income = parseCurrencyToNumber(el.incomeInput.value);
    let hasError = false;

    if (!el.incomeInput.value) {
      setFieldError(el.incomeField, el.incomeError, FRIENDLY_ERRORS.incomeEmpty);
      hasError = true;
    } else if (!isValidIncome(income)) {
      setFieldError(el.incomeField, el.incomeError, FRIENDLY_ERRORS.incomeInvalid);
      hasError = true;
    } else {
      setFieldError(el.incomeField, el.incomeError, null);
    }

    if (!selections.titularidadeImovel) {
      setFieldError(el.ownershipField, el.ownershipError, FRIENDLY_ERRORS.ownershipRequired);
      hasError = true;
    } else {
      setFieldError(el.ownershipField, el.ownershipError, null);
    }

    if (hasError) return;

    leadStore.update({
      rendaMensal: income,
      titularidadeImovel: selections.titularidadeImovel,
    });
    analytics.track(analytics.EVENTS.INCOME_OWNERSHIP_COMPLETED, {
      titularidadeImovel: selections.titularidadeImovel,
    });
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 6: valor desejado ----------

function bindDesiredAmountStep() {
  attachCurrencyMask(el.desiredAmountInput);

  el.desiredAmountNextBtn.addEventListener('click', () => {
    const value = parseCurrencyToNumber(el.desiredAmountInput.value);

    if (!el.desiredAmountInput.value) {
      setFieldError(el.desiredAmountField, el.desiredAmountError, FRIENDLY_ERRORS.desiredAmountEmpty);
      return;
    }
    if (!isValidDesiredAmount(value)) {
      setFieldError(el.desiredAmountField, el.desiredAmountError, FRIENDLY_ERRORS.desiredAmountInvalid);
      return;
    }

    setFieldError(el.desiredAmountField, el.desiredAmountError, null);
    leadStore.update({ valorDesejado: value });
    analytics.track(analytics.EVENTS.QUIZ_COMPLETED);
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 7: nome ----------

function bindLeadNameStep() {
  el.leadNameNextBtn.addEventListener('click', () => {
    const name = el.leadNameInput.value;

    if (!isValidName(name)) {
      setFieldError(el.leadNameField, el.leadNameError, FRIENDLY_ERRORS.nameInvalid);
      return;
    }

    setFieldError(el.leadNameField, el.leadNameError, null);
    leadStore.update({ nome: name.trim() });
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 8: WhatsApp ----------

function bindLeadWhatsappStep() {
  attachPhoneMask(el.leadWhatsappInput);

  el.leadWhatsappNextBtn.addEventListener('click', () => {
    const whatsapp = el.leadWhatsappInput.value;

    if (!isValidPhone(whatsapp)) {
      setFieldError(el.leadWhatsappField, el.leadWhatsappError, FRIENDLY_ERRORS.phoneInvalid);
      return;
    }

    setFieldError(el.leadWhatsappField, el.leadWhatsappError, null);
    leadStore.update({ whatsapp });
    showQuestionStep(currentQuestionIndex + 1);
  });
}

// ---------- Passo 9: e-mail ----------

function bindLeadEmailStep() {
  el.leadEmailNextBtn.addEventListener('click', () => {
    const email = el.leadEmailInput.value;

    if (!email || !email.trim()) {
      setFieldError(el.leadEmailField, el.leadEmailError, FRIENDLY_ERRORS.emailRequired);
      return;
    }

    if (!isValidEmail(email)) {
      setFieldError(el.leadEmailField, el.leadEmailError, FRIENDLY_ERRORS.emailInvalid);
      return;
    }

    setFieldError(el.leadEmailField, el.leadEmailError, null);
    el.leadSubmitError.textContent = '';
    leadStore.update({
      email: email.trim(),
      status: CONFIG.LEAD_STATUS.QUALIFIED,
    });
    analytics.track(analytics.EVENTS.LEAD_INFO_COMPLETED);

    runCalculationAndShowResult();
  });
}

// ---------- Cálculo + resultado ----------

function animateCalculatingScreen(durationMs) {
  const circumference = 213.6;
  const startedAt = Date.now();
  let messageIndex = 0;

  el.calcRingProgress.style.strokeDashoffset = String(circumference);
  el.calcPercent.textContent = '0%';
  el.calcStatusText.textContent = CALCULATING_MESSAGES[0];

  const messageTimer = window.setInterval(() => {
    messageIndex = Math.min(messageIndex + 1, CALCULATING_MESSAGES.length - 1);
    el.calcStatusText.textContent = CALCULATING_MESSAGES[messageIndex];
  }, Math.round(durationMs / CALCULATING_MESSAGES.length));

  const progressTimer = window.setInterval(() => {
    const elapsed = Date.now() - startedAt;
    // Sobe até ~96% durante a espera e só fecha em 100% quando o
    // resultado estiver pronto, para nunca "travar" em 100% parado.
    const pct = Math.min(96, Math.round((elapsed / durationMs) * 96));
    el.calcPercent.textContent = `${pct}%`;
    el.calcRingProgress.style.strokeDashoffset = String(circumference * (1 - pct / 100));
  }, 40);

  return () => {
    window.clearInterval(messageTimer);
    window.clearInterval(progressTimer);
    el.calcPercent.textContent = '100%';
    el.calcRingProgress.style.strokeDashoffset = '0';
  };
}

function runCalculationAndShowResult() {
  goToScreen('screen-calculating');
  const stopAnimation = animateCalculatingScreen(CALCULATING_DURATION_MS);

  const lead = leadStore.get();
  // O percentual sorteado (rollLoanToValue, dentro de calculateEstimatedCredit)
  // continua alimentando o score interno do lead e o CRM — dá mais nuance
  // pra equipe comercial. Mas na TELA, em vez de mostrar esse valor sorteado
  // como se fosse único ("Até 55%"), sempre exibimos a faixa completa
  // configurada (40% a 60%), com os dois valores de crédito correspondentes
  // lado a lado — fica claro que é uma faixa, não uma média disfarçada de
  // número fechado.
  const { ltvPercentage, estimatedCredit } = calculateEstimatedCredit(lead.valorImovel);

  // Simulação de parcela: aplicada sobre o valor que o lead disse que
  // quer (valorDesejado), não sobre a estimativa de crédito — é a
  // pergunta real que ele fez ("quanto ficaria a parcela desse tanto que
  // eu quero"). Taxa e prazo de referência ficam centralizados em
  // CONFIG (ver comentário lá) para poder ajustar em um só lugar.
  const installment = calculateInstallment(
    lead.valorDesejado,
    CONFIG.MONTHLY_INTEREST_RATE,
    CONFIG.FINANCING_TERM_MONTHS
  );

  leadStore.update({
    percentualConsiderado: ltvPercentage,
    estimativaCredito: estimatedCredit,
    parcelaEstimada: installment,
  });

  const creditMin = Math.round(lead.valorImovel * CONFIG.MIN_LOAN_TO_VALUE);
  const creditMax = Math.round(lead.valorImovel * CONFIG.MAX_LOAN_TO_VALUE);
  const percentLabel = `${Math.round(CONFIG.MIN_LOAN_TO_VALUE * 100)}% a ${Math.round(CONFIG.MAX_LOAN_TO_VALUE * 100)}%`;

  const waitForAnimation = new Promise((resolve) => window.setTimeout(resolve, CALCULATING_DURATION_MS));
  const submitToCrm = sendLeadToCrm(leadStore.toCrmPayload());

  Promise.all([waitForAnimation, submitToCrm]).then(([, crmResult]) => {
    stopAnimation();

    el.resultPropertyValue.textContent = formatCurrencyBRL(lead.valorImovel);
    el.resultPercentage.textContent = percentLabel;
    el.resultEstimatedCredit.textContent = `${formatCurrencyBRL(creditMin)} a ${formatCurrencyBRL(creditMax)}`;
    if (el.resultDesiredAmount) {
      // Mostrado explicitamente aqui, na mesma seção da parcela, porque é
      // esse valor (e não o valor do imóvel nem a estimativa de crédito)
      // que serve de base para o cálculo da parcela logo abaixo — sem essa
      // linha, a parcela exibida parece não bater com o resto da tela.
      el.resultDesiredAmount.textContent = formatCurrencyBRL(lead.valorDesejado);
    }
    if (el.resultInstallment) {
      // Só o valor aqui (curto, uma linha só, igual às outras linhas do
      // resumo) — o prazo (240x/20 anos) fica no rótulo da linha, também
      // gerado a partir do CONFIG, pra nunca ficar dessincronizado se o
      // prazo de referência mudar.
      el.resultInstallment.textContent = `${formatCurrencyBRL(installment)}/mês`;
    }
    if (el.resultInstallmentLabel) {
      const termYears = Math.round(CONFIG.FINANCING_TERM_MONTHS / 12);
      el.resultInstallmentLabel.textContent = `Parcela estimada (até ${termYears} anos)`;
    }
    if (el.resultRate) {
      const rateLabel = (CONFIG.MONTHLY_INTEREST_RATE * 100).toLocaleString('pt-BR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      });
      el.resultRate.textContent = `a partir de ${rateLabel}% a.m. + IPCA`;
    }
    if (el.resultDisclaimer) {
      // Taxa e prazo de referência explícitos aqui (gerados a partir do
      // CONFIG, nunca hardcoded) — antes o texto só dizia "com taxa e prazo
      // de referência" sem dizer quais, o que não deixava claro que a
      // parcela acima já usa exatamente 1,3% ao mês / 240 meses.
      const ratePercentLabel = (CONFIG.MONTHLY_INTEREST_RATE * 100).toLocaleString('pt-BR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      });
      const termYears = Math.round(CONFIG.FINANCING_TERM_MONTHS / 12);
      el.resultDisclaimer.textContent =
        `Essa é uma estimativa inicial. A simulação de parcela considera taxa a partir de ` +
        `${ratePercentLabel}% ao mês mais IPCA e prazo de até ${termYears} anos (${CONFIG.FINANCING_TERM_MONTHS} meses). ` +
        `Se preferir um prazo menor, é possível. ` +
        `O valor final depende da análise do imóvel, documentação, perfil da operação e ` +
        `critérios da instituição financeira.`;
    }

    analytics.track(analytics.EVENTS.SIMULATION_GENERATED, { estimativa: estimatedCredit });
    if (crmResult && crmResult.sent !== false) {
      analytics.track(analytics.EVENTS.LEAD_SUBMITTED, { estimativa: estimatedCredit });
    }
    setupWhatsappCta();

    window.setTimeout(() => goToScreen('screen-result'), 150);
  });
}

function bindResultScreen() {
  el.resultCtaBtn.addEventListener('click', () => {
    // Direciona direto pro WhatsApp ao clicar, sem tela de confirmação
    // intermediária. Troca a página atual (em vez de abrir nova aba) porque
    // o pedido é justamente ser direcionado automaticamente para lá.
    if (whatsappCtaHref) {
      analytics.track(analytics.EVENTS.WHATSAPP_CLICKED);
      (window.top || window).location.href = whatsappCtaHref;
    }
  });
}

function optionLabel(options, value) {
  const found = options.find((opt) => opt.value === value);
  return found ? found.label : value;
}

/**
 * Monta a mensagem pré-preenchida do WhatsApp com um resumo de tudo que
 * o lead respondeu no formulário, pra equipe comercial já abrir a
 * conversa com contexto, sem precisar caçar o lead no CRM antes de
 * responder.
 */
function buildWhatsappSummary(lead) {
  const tipos = Array.isArray(lead.tipoImovel) ? lead.tipoImovel : [lead.tipoImovel].filter(Boolean);
  const tiposLabel = tipos.map((value) => optionLabel(PROPERTY_TYPE_OPTIONS, value)).join(', ') || '-';
  const situacaoLabel = lead.situacaoImovel ? optionLabel(PROPERTY_STATUS_OPTIONS, lead.situacaoImovel) : '-';
  const cidadeLabel = lead.municipio ? `${lead.municipio} - ${lead.estado}` : '-';
  const titularidadeLabel = lead.titularidadeImovel ? optionLabel(OWNERSHIP_OPTIONS, lead.titularidadeImovel) : '-';
  const rendaLabel = lead.rendaMensal ? formatCurrencyBRL(lead.rendaMensal) : '-';

  // Mesma faixa fixa (40% a 60%) exibida na tela de resultado, nunca o
  // valor sorteado internamente (esse fica só no score do CRM). Mostrar o
  // sorteio aqui quebraria a consistência com o que o lead viu na tela.
  const creditMin = Math.round(lead.valorImovel * CONFIG.MIN_LOAN_TO_VALUE);
  const creditMax = Math.round(lead.valorImovel * CONFIG.MAX_LOAN_TO_VALUE);
  const creditRangeLabel = `${formatCurrencyBRL(creditMin)} a ${formatCurrencyBRL(creditMax)}`;

  // Só inclui a localização (rua/condomínio) dos tipos que estão
  // efetivamente selecionados agora, evitando mostrar uma resposta de um
  // tipo de imóvel que o lead já desmarcou.
  const localizacaoLinhas = [];
  if (tipos.includes('casa') && lead.localizacaoCasa) {
    localizacaoLinhas.push(`Localização da casa: ${optionLabel(LOCATION_TYPE_OPTIONS, lead.localizacaoCasa)}`);
  }
  if (tipos.includes('terreno_condominio') && lead.localizacaoTerreno) {
    localizacaoLinhas.push(`Localização do terreno: ${optionLabel(LOCATION_TYPE_OPTIONS, lead.localizacaoTerreno)}`);
  }

  const linhas = [
    `Olá! Acabei de fazer uma simulação de Home Equity no site da Acrópole. Aqui está um resumo:`,
    ``,
    `Nome: ${lead.nome || '-'}`,
    `Cidade: ${cidadeLabel}`,
    `Tipo de imóvel: ${tiposLabel}`,
    ...localizacaoLinhas,
    `Situação do financiamento: ${situacaoLabel}`,
    `Imóvel no: ${titularidadeLabel}`,
    `Valor do imóvel: ${formatCurrencyBRL(lead.valorImovel)}`,
    `Renda mensal: ${rendaLabel}`,
    `Valor desejado: ${formatCurrencyBRL(lead.valorDesejado)}`,
    `Estimativa de crédito: ${creditRangeLabel}`,
    `Parcela estimada: ${formatCurrencyBRL(lead.parcelaEstimada)}/mês, em até ${Math.round(CONFIG.FINANCING_TERM_MONTHS / 12)} anos (taxa a partir de ${(CONFIG.MONTHLY_INTEREST_RATE * 100).toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 2 })}% ao mês mais IPCA)`,
    ``,
    `Gostaria de saber mais sobre minha possibilidade de crédito.`,
  ];

  return linhas.join('\n');
}

function setupWhatsappCta() {
  const lead = leadStore.get();
  const message = encodeURIComponent(buildWhatsappSummary(lead));
  // Guardado numa variável do módulo (em vez de um link no DOM) porque não
  // existe mais uma tela de confirmação com esse link — o clique no botão
  // de resultado já lê essa variável direto (ver bindResultScreen).
  whatsappCtaHref = `https://wa.me/${CONFIG.WHATSAPP_NUMBER}?text=${message}`;
}


/* ===== bootstrap ===== */
document.addEventListener('DOMContentLoaded', () => { initQuiz(); flushPendingLeads(); });

})();