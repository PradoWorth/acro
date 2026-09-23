<?php
/**
 * GET /api/comments-list.php?article=<slug>
 * Lista os comentários publicados de um artigo, mais recentes por último
 * (ordem de leitura natural, mais antigo primeiro). Não exige login —
 * qualquer visitante pode ler os comentários, só publicar exige conta
 * Google.
 */

declare(strict_types=1);

require __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'GET') {
    header('Allow: GET');
    acropole_fail(405, 'Método não permitido.');
}

$article = $_GET['article'] ?? '';
if (!is_string($article) || !preg_match('/^[a-z0-9\-]{1,200}$/', $article)) {
    acropole_fail(400, 'Artigo inválido.');
}

try {
    $pdo = acropole_db();
} catch (Throwable $e) {
    acropole_fail(500, 'Serviço indisponível no momento.', $e->getMessage());
}

$stmt = $pdo->prepare(
    'SELECT c.id, c.body, c.created_at, u.google_sub, u.name, u.avatar_url
       FROM comments c
       JOIN comment_users u ON u.id = c.user_id
      WHERE c.article_slug = :article AND c.status = "published"
      ORDER BY c.created_at ASC
      LIMIT 500'
);
$stmt->execute(['article' => $article]);
$rows = $stmt->fetchAll();

$comments = array_map(function ($r) {
    return [
        'id' => (int) $r['id'],
        'body' => $r['body'],
        'created_at' => $r['created_at'],
        'google_sub' => $r['google_sub'],
        'name' => $r['name'],
        'avatar_url' => $r['avatar_url'],
    ];
}, $rows);

echo json_encode(['ok' => true, 'comments' => $comments]);
