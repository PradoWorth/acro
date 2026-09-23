<?php
/**
 * POST /api/comments-admin-delete.php
 * Body JSON: { "id": <int>, "token": "<COMMENTS_ADMIN_TOKEN>" }
 *
 * Válvula de segurança manual: já que a publicação de comentário é
 * automática, sem fila de moderação (decisão da cliente), este é o jeito
 * de remover um comentário problemático (spam, ofensa, etc.) sem precisar
 * mexer direto no banco de dados pelo phpMyAdmin. Protegido só por um
 * token fixo (COMMENTS_ADMIN_TOKEN em db.local.php) — não é um painel de
 * administração de verdade, é deliberadamente simples. Não existe link
 * nenhum pra isso no site; use com uma chamada direta (ex.: um comando
 * curl) só quando precisar.
 *
 * Exemplo de uso (troque SEU_TOKEN e o id do comentário):
 *   curl -X POST https://acropolecapital.com.br/api/comments-admin-delete.php \
 *        -H "Content-Type: application/json" \
 *        -d '{"id": 123, "token": "SEU_TOKEN"}'
 */

declare(strict_types=1);

require __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    acropole_fail(405, 'Método não permitido.');
}

if (acropole_rate_limited('admin-delete', 10, 60)) {
    header('Retry-After: 60');
    acropole_fail(429, 'Muitas tentativas. Tente novamente em instantes.');
}

$raw = file_get_contents('php://input', false, null, 0, 65536);
$data = json_decode((string) $raw, true);
if (!is_array($data)) {
    acropole_fail(400, 'Corpo inválido.');
}

$token = is_string($data['token'] ?? null) ? $data['token'] : '';
if (!defined('COMMENTS_ADMIN_TOKEN') || COMMENTS_ADMIN_TOKEN === '' || !hash_equals(COMMENTS_ADMIN_TOKEN, $token)) {
    // Mesma resposta genérica quer o token esteja errado, quer não
    // configurado — nunca revela qual dos dois é o caso.
    acropole_fail(403, 'Não autorizado.');
}

$id = isset($data['id']) ? filter_var($data['id'], FILTER_VALIDATE_INT) : false;
if ($id === false || $id <= 0) {
    acropole_fail(400, 'Comentário inválido.');
}

try {
    $pdo = acropole_db();
} catch (Throwable $e) {
    acropole_fail(500, 'Serviço indisponível no momento.', $e->getMessage());
}

$del = $pdo->prepare('DELETE FROM comments WHERE id = :id');
$del->execute(['id' => $id]);

echo json_encode(['ok' => true, 'deleted' => $del->rowCount() > 0]);
