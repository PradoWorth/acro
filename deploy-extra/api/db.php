<?php
/**
 * Conexão PDO compartilhada pelos endpoints de comentários. Lê
 * db.local.php (nunca commitado, nunca acessível via navegador — ver
 * .htaccess da raiz) pra pegar host/nome/usuário/senha do banco.
 */

declare(strict_types=1);

$dbConfigFile = __DIR__ . '/db.local.php';
if (is_file($dbConfigFile)) {
    require $dbConfigFile;
}

function acropole_db(): PDO
{
    static $pdo = null;
    if ($pdo !== null) {
        return $pdo;
    }
    if (!defined('DB_HOST') || !defined('DB_NAME') || !defined('DB_USER') || !defined('DB_PASS')) {
        throw new RuntimeException('Banco não configurado (db.local.php ausente ou incompleto).');
    }
    $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
    $pdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
    return $pdo;
}

/**
 * Resposta de erro genérica e padronizada — nunca vaza detalhe interno
 * (mensagem de exceção, erro de SQL) pro navegador (checklist de
 * segurança, item 15). O detalhe real vai só pro error_log do servidor.
 */
function acropole_fail(int $status, string $publicMessage, string $logDetail = ''): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    if ($logDetail !== '') {
        error_log('comments api: ' . $logDetail);
    }
    echo json_encode(['ok' => false, 'error' => $publicMessage]);
    exit;
}

/**
 * Checagem leve de mesma origem — mesmo padrão do lead-webhook.php.
 * Defesa em profundidade, não é a única linha de proteção.
 */
function acropole_check_origin(): void
{
    $allowedHosts = defined('COMMENTS_ALLOWED_HOSTS')
        ? COMMENTS_ALLOWED_HOSTS
        : ['acropolecapital.com.br', 'www.acropolecapital.com.br'];
    $origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
    if ($origin === '') {
        return;
    }
    $originHost = parse_url($origin, PHP_URL_HOST);
    if ($originHost !== null && !in_array($originHost, $allowedHosts, true)) {
        acropole_fail(403, 'Origem não permitida.');
    }
}

/**
 * Rate limit simples por IP, num arquivo local (mesma técnica do
 * lead-webhook.php — hospedagem compartilhada não tem Redis). Falha em
 * modo aberto se o diretório de cache não puder ser preparado.
 */
function acropole_rate_limited(string $bucket, int $limit, int $windowSeconds): bool
{
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? 'desconhecido';
    $ip = trim(explode(',', $ip)[0]);
    $dir = sys_get_temp_dir() . '/acropole-comments-rl';
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
        return false;
    }
    $file = $dir . '/' . $bucket . '-' . md5($ip) . '.json';
    $now = time();
    $fp = @fopen($file, 'c+');
    if (!$fp) {
        return false;
    }
    flock($fp, LOCK_EX);
    $raw = stream_get_contents($fp);
    $hits = $raw ? (json_decode($raw, true) ?: []) : [];
    $hits = array_values(array_filter($hits, fn($t) => $t > $now - $windowSeconds));
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
