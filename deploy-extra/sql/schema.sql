-- Esquema do banco de comentários (login com Google) dos artigos de
-- Conteúdos. Importar no banco MySQL/MariaDB criado no hPanel da Hostinger
-- (Bancos de Dados → MySQL → criar banco + usuário, depois usar o
-- phpMyAdmin do próprio hPanel pra rodar este arquivo, ou `mysql -u ... -p
-- nome_do_banco < schema.sql` se tiver acesso SSH).
--
-- Depois de criar o banco, preencha deploy-extra/api/db.local.php (copiado
-- de db.local.php.example) com host/nome/usuário/senha desse banco.

CREATE TABLE IF NOT EXISTS comment_users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  google_sub VARCHAR(64) NOT NULL,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(320) NOT NULL,
  avatar_url VARCHAR(500) DEFAULT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_google_sub (google_sub)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comments (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  article_slug VARCHAR(200) NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  body TEXT NOT NULL,
  status ENUM('published','hidden') NOT NULL DEFAULT 'published',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_article (article_slug, status, created_at),
  KEY idx_user (user_id),
  CONSTRAINT fk_comments_user FOREIGN KEY (user_id) REFERENCES comment_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
