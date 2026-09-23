<?php
/**
 * POST /api/comments-post.php
 * Body JSON: { "article": "<slug>", "body": "<texto>", "id_token": "<jwt do Google>" }
 *
 * Publica um comentário na hora (sem fila de moderação — decisão da
 * cliente). Exige um ID token do Google válido, revalidado aqui no
 * servidor a cada chamada (nunca confia em nome/e-mail que o navegador
 * mande solto, sempre deriva do token). Cadastra ou atualiza o usuário
 * (nome/foto podem mudar no Google) antes de inserir o comentário.
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

if (acropole_rate_limited('post', 8, 60)) {
    header('Retry-After: 60');
    acropole_fail(429, 'Muitos comentários em pouco tempo. Tente novamente em instantes.');
}

$raw = file_get_contents('php://input', false, null, 0, 65536);
$data = json_decode((string) $raw, true);
if (!is_array($data)) {
    acropole_fail(400, 'Corpo inválido.');
}

$article = is_string($data['article'] ?? null) ? $data['article'] : '';
if (!preg_match('/^[a-z0-9\-]{1,200}$/', $article)) {
    acropole_fail(400, 'Artigo inválido.');
}

$body = is_string($data['body'] ?? null) ? trim($data['body']) : '';
$body = mb_substr($body, 0, 2000);
if ($body === '') {
    acropole_fail(422, 'Escreva um comentário antes de publicar.');
}

$idToken = is_string($data['id_token'] ?? null) ? $data['id_token'] : '';
$user = acropole_verify_google_token($idToken);
if ($user === null) {
    acropole_fail(401, 'Sua sessão do Google expirou. Entre novamente pra comentar.');
}

try {
    $pdo = acropole_db();
} catch (Throwable $e) {
    acropole_fail(500, 'Serviço indisponível no momento.', $e->getMessage());
}

try {
    $pdo->beginTransaction();

    // Upsert do usuário: nome/foto do Google podem mudar entre uma visita
    // e outra, então atualiza em vez de só ignorar quando já existe.
    $stmt = $pdo->prepare('SELECT id FROM comment_users WHERE google_sub = :sub');
    $stmt->execute(['sub' => $user['sub']]);
    $existing = $stmt->fetch();

    if ($existing) {
        $userId = (int) $existing['id'];
        $upd = $pdo->prepare('UPDATE comment_users SET name = :name, email = :email, avatar_url = :avatar WHERE id = :id');
        $upd->execute(['name' => $user['name'], 'email' => $user['email'], 'avatar' => $user['picture'], 'id' => $userId]);
    } else {
        $ins = $pdo->prepare('INSERT INTO comment_users (google_sub, name, email, avatar_url) VALUES (:sub, :name, :email, :avatar)');
        $ins->execute(['sub' => $user['sub'], 'name' => $user['name'], 'email' => $user['email'], 'avatar' => $user['picture']]);
        $userId = (int) $pdo->lastInsertId();
    }

    $insC = $pdo->prepare('INSERT INTO comments (article_slug, user_id, body) VALUES (:article, :user_id, :body)');
    $insC->execute(['article' => $article, 'user_id' => $userId, 'body' => $body]);
    $commentId = (int) $pdo->lastInsertId();

    $pdo->commit();
} catch (Throwable $e) {
    $pdo->rollBack();
    acropole_fail(500, 'Não foi possível publicar agora. Tente novamente em instantes.', $e->getMessage());
}

echo json_encode(['ok' => true, 'comment' => [
    'id' => $commentId,
    'body' => $body,
    'created_at' => gmdate('Y-m-d\TH:i:s\Z'),
    'google_sub' => $user['sub'],
    'name' => $user['name'],
    'avatar_url' => $user['picture'],
]]);
