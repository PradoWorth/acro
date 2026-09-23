<?php
/**
 * POST /api/comments-delete.php
 * Body JSON: { "id": <int>, "id_token": "<jwt do Google>" }
 *
 * Exclui um comentário — só o autor pode excluir o próprio (o servidor
 * confere o "sub" do token revalidado contra o dono do comentário no
 * banco, nunca confia em nada que o navegador declare sobre quem é o
 * autor). Exclusão de QUALQUER comentário por um administrador é um
 * endpoint separado (comments-admin-delete.php), de propósito — assim um
 * bug aqui nunca vira um jeito de apagar comentário alheio.
 */

declare(strict_types=1);

require __DIR__ . '/db.php';
require __DIR__ . '/google-verify.php';

header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    acropole_fail(405, 'Método não permitido.');
}

acropole_check_origin();

if (acropole_rate_limited('delete', 20, 60)) {
    header('Retry-After: 60');
    acropole_fail(429, 'Muitas tentativas. Tente novamente em instantes.');
}

$raw = file_get_contents('php://input', false, null, 0, 65536);
$data = json_decode((string) $raw, true);
if (!is_array($data)) {
    acropole_fail(400, 'Corpo inválido.');
}

$id = isset($data['id']) ? filter_var($data['id'], FILTER_VALIDATE_INT) : false;
if ($id === false || $id <= 0) {
    acropole_fail(400, 'Comentário inválido.');
}

$idToken = is_string($data['id_token'] ?? null) ? $data['id_token'] : '';
$user = acropole_verify_google_token($idToken);
if ($user === null) {
    acropole_fail(401, 'Sua sessão do Google expirou. Entre novamente.');
}

try {
    $pdo = acropole_db();
} catch (Throwable $e) {
    acropole_fail(500, 'Serviço indisponível no momento.', $e->getMessage());
}

$stmt = $pdo->prepare(
    'SELECT c.id FROM comments c
       JOIN comment_users u ON u.id = c.user_id
      WHERE c.id = :id AND u.google_sub = :sub'
);
$stmt->execute(['id' => $id, 'sub' => $user['sub']]);
if (!$stmt->fetch()) {
    // Mesma resposta esteja o comentário inexistente ou seja de outra
    // pessoa — não vaza qual dos dois é o caso.
    acropole_fail(404, 'Comentário não encontrado.');
}

$del = $pdo->prepare('DELETE FROM comments WHERE id = :id');
$del->execute(['id' => $id]);

echo json_encode(['ok' => true]);
