<?php
/**
 * Verificação do ID token do Google Identity Services, do lado do
 * servidor. Em vez de implementar verificação de assinatura JWT (RS256)
 * na mão em PHP puro — sem depender do Composer, que hospedagem
 * compartilhada nem sempre libera —, usamos o endpoint público de
 * tokeninfo do próprio Google: ele já confere assinatura, expiração e
 * emissor, e devolve os dados do token em JSON. É exatamente o mesmo
 * princípio do endpoint oficial recomendado pelo Google pra validação
 * server-side simples (https://developers.google.com/identity/sign-in/web/backend-auth).
 *
 * O que AINDA conferimos aqui, que o tokeninfo não garante sozinho: que o
 * "aud" (audience) do token bate com o nosso GOOGLE_CLIENT_ID — sem essa
 * checagem, um token válido emitido pra outro site qualquer também
 * passaria.
 */

declare(strict_types=1);

function acropole_verify_google_token(string $idToken): ?array
{
    if ($idToken === '') {
        return null;
    }
    // A URL base só é trocável por variável de ambiente pra permitir teste
    // automatizado com um servidor local no lugar do Google de verdade
    // (ver test_ui.py / smoke test em deploy-extra) — em produção,
    // GOOGLE_TOKENINFO_URL nunca é definida, então sempre usa o endpoint
    // real do Google.
    $base = getenv('GOOGLE_TOKENINFO_URL') ?: 'https://oauth2.googleapis.com/tokeninfo';
    $ch = curl_init($base . '?id_token=' . urlencode($idToken));
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 6,
        CURLOPT_CONNECTTIMEOUT => 4,
    ]);
    $resp = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($resp === false || $status !== 200) {
        return null; // token inválido, expirado, ou o Google não respondeu
    }
    $data = json_decode($resp, true);
    if (!is_array($data)) {
        return null;
    }
    if (!defined('GOOGLE_CLIENT_ID') || ($data['aud'] ?? '') !== GOOGLE_CLIENT_ID) {
        return null;
    }
    if (($data['email_verified'] ?? 'false') !== 'true') {
        return null;
    }
    if (empty($data['sub']) || empty($data['email'])) {
        return null;
    }
    return [
        'sub' => (string) $data['sub'],
        'email' => (string) $data['email'],
        'name' => (string) ($data['name'] ?? $data['email']),
        'picture' => isset($data['picture']) ? (string) $data['picture'] : null,
    ];
}
