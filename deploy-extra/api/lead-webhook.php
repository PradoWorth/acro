<?php
/**
 * Proxy do webhook de leads (n8n).
 *
 * Por quê isso existe: o site é 100% estático (HTML/CSS/JS servido direto),
 * sem nenhum servidor próprio. Se o token secreto do n8n fosse colocado em
 * site.js/config.js, ele iria pro navegador de QUALQUER visitante — visível
 * em "Ver código-fonte" e na aba Network do DevTools. Não existe jeito de
 * "esconder" isso no lado do cliente, nem minificado.
 *
 * Este script roda no servidor (aqui, PHP na Hostinger) e é o único lugar
 * que conhece o token de verdade. O navegador chama ESTE arquivo, no
 * próprio domínio do site (sem token nenhum no meio) — é este script que
 * anexa o token e repassa a chamada pro n8n.
 *
 * CONFIGURAÇÃO OBRIGATÓRIA ANTES DE USAR:
 * Copie config.local.php.example pra config.local.php (mesma pasta) e
 * preencha os 3 valores. config.local.php NUNCA deve ir pro Git nem
 * aparecer em nenhum lugar público — o .htaccess da pasta raiz já bloqueia
 * o acesso via navegador a esse arquivo, mas ele também não deve ser
 * commitado (adicione ao .gitignore se este projeto usar Git na Hostinger).
 *
 * Depois de configurado, troque o endpoint em config.js do site de:
 *   endpoint: "https://n8n.../webhook-test/recebimento-de-leads"
 * para:
 *   endpoint: "/api/lead-webhook.php"
 * (caminho relativo, mesmo domínio — não precisa mexer em CSP connect-src
 * nem em nada além dessa linha, já que deixa de ser uma chamada de
 * terceiro do ponto de vista do navegador).
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

// --------------------------------------------------------------------
// Config (nunca hardcode o token aqui — vem de config.local.php ou de
// variável de ambiente, se o painel da hospedagem permitir configurar).
// --------------------------------------------------------------------
$configFile = __DIR__ . '/config.local.php';
if (is_file($configFile)) {
    require $configFile; // deve definir N8N_WEBHOOK_URL, N8N_WEBHOOK_TOKEN, N8N_WEBHOOK_HEADER
}
$webhookUrl    = defined('N8N_WEBHOOK_URL') ? N8N_WEBHOOK_URL : getenv('N8N_WEBHOOK_URL');
$webhookToken  = defined('N8N_WEBHOOK_TOKEN') ? N8N_WEBHOOK_TOKEN : getenv('N8N_WEBHOOK_TOKEN');
$webhookHeader = defined('N8N_WEBHOOK_HEADER') ? N8N_WEBHOOK_HEADER : (getenv('N8N_WEBHOOK_HEADER') ?: 'Authorization');

if (!$webhookUrl || !$webhookToken) {
    http_response_code(500);
    // Mensagem genérica pro cliente (item 15 da checklist de segurança:
    // nunca vazar detalhe interno) — o motivo real só vai pro log do servidor.
    error_log('lead-webhook.php: N8N_WEBHOOK_URL/N8N_WEBHOOK_TOKEN não configurados em config.local.php');
    echo json_encode(['ok' => false, 'error' => 'Serviço indisponível no momento.']);
    exit;
}

// --------------------------------------------------------------------
// Só aceita POST.
// --------------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    header('Allow: POST');
    echo json_encode(['ok' => false, 'error' => 'Método não permitido.']);
    exit;
}

// --------------------------------------------------------------------
// Checagem leve de mesma origem (defesa em profundidade — não é à prova
// de falhas, um script fora do navegador pode forjar esses headers, mas
// bloqueia o caso comum de outro site chamar este endpoint direto).
// Ajuste ALLOWED_HOSTS se o site responder por mais de um domínio.
// --------------------------------------------------------------------
$allowedHosts = defined('N8N_ALLOWED_HOSTS') ? N8N_ALLOWED_HOSTS : ['acropolecapital.com.br', 'www.acropolecapital.com.br'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
if ($origin !== '') {
    $originHost = parse_url($origin, PHP_URL_HOST);
    if ($originHost !== null && !in_array($originHost, $allowedHosts, true)) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'Origem não permitida.']);
        exit;
    }
}

// --------------------------------------------------------------------
// Rate limit simples por IP (best-effort num arquivo local — hospedagem
// compartilhada não tem Redis/Memcached disponível de regra). Limita a
// 10 envios por IP a cada 60 segundos. Se o diretório de cache não for
// gravável, falha em modo aberto (não bloqueia envio de lead de verdade
// por causa de uma limitação de infraestrutura).
// --------------------------------------------------------------------
function rateLimited(string $ip): bool
{
    $dir = sys_get_temp_dir() . '/acropole-lead-rl';
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
        return false; // não conseguiu preparar o diretório: não bloqueia
    }
    $file = $dir . '/' . md5($ip) . '.json';
    $now = time();
    $window = 60;
    $limit = 10;

    $fp = @fopen($file, 'c+');
    if (!$fp) {
        return false;
    }
    flock($fp, LOCK_EX);
    $raw = stream_get_contents($fp);
    $hits = $raw ? (json_decode($raw, true) ?: []) : [];
    $hits = array_values(array_filter($hits, fn($t) => $t > $now - $window));
    $blocked = count($hits) >= $limit;
    if (!$blocked) {
        $hits[] = $now;
        ftruncate($fp, 0);
        rewind($fp);
        fwrite($fp, json_encode($hits));
    }
    flock($fp, LOCK_UN);
    fclose($fp);
    return $blocked;
}

$clientIp = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'desconhecido';
$clientIp = trim(explode(',', $clientIp)[0]); // primeiro IP se vier via proxy/Cloudflare
if (rateLimited($clientIp)) {
    http_response_code(429);
    header('Retry-After: 60');
    echo json_encode(['ok' => false, 'error' => 'Muitas tentativas. Tente novamente em instantes.']);
    exit;
}

// --------------------------------------------------------------------
// Lê e valida o corpo. Limite de tamanho evita payload absurdo; campos
// obrigatórios batem com as 5 chaves canônicas que o n8n espera.
// --------------------------------------------------------------------
$raw = file_get_contents('php://input', false, null, 0, 65536); // até 64KB
$data = json_decode((string) $raw, true);

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Corpo inválido.']);
    exit;
}

$required = ['name', 'email', 'whatsapp', 'faturamento', 'tracking_params'];
$payload = [];
foreach ($required as $key) {
    $value = $data[$key] ?? '';
    if (!is_string($value)) {
        $value = is_scalar($value) ? (string) $value : '';
    }
    $payload[$key] = mb_substr(trim($value), 0, 4000); // limite de tamanho por campo
}
if ($payload['name'] === '' || $payload['email'] === '') {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Campos obrigatórios ausentes.']);
    exit;
}
// Repassa também "page", se vier, só como contexto (não é uma das 5 chaves obrigatórias).
if (isset($data['page']) && is_string($data['page'])) {
    $payload['page'] = mb_substr($data['page'], 0, 500);
}

// --------------------------------------------------------------------
// Encaminha pro n8n, com o token no header (nunca no corpo, nunca em
// query string — ver checklist de segurança item 1).
// --------------------------------------------------------------------
$ch = curl_init($webhookUrl);
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($payload),
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        $webhookHeader . ': ' . $webhookToken,
    ],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 10,
    CURLOPT_CONNECTTIMEOUT => 5,
]);
$response = curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($response === false || $status < 200 || $status >= 300) {
    // Log interno com detalhe; resposta ao navegador continua genérica.
    error_log('lead-webhook.php: falha ao repassar pro n8n — status ' . $status . ' — ' . $curlError);
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => 'Não foi possível registrar o envio agora. Tente novamente.']);
    exit;
}

http_response_code(200);
echo json_encode(['ok' => true]);
