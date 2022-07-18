CREATE TABLE
  IF NOT EXISTS user_(
    user_id BIGINT NOT NULL,
    experience INTEGER NOT NULL DEFAULT 0,
    current_level INTEGER NOT NULL DEFAULT 1,
    max_experience INTEGER NOT NULL DEFAULT 100,
    guild_id BIGINT NOT NULL DEFAULT 0
  );

CREATE TABLE
  IF NOT EXISTS guild(guild_id BIGINT);

CREATE TABLE
  IF NOT EXISTS roles_level(
    guild_id BIGINT,
    role_id INTEGER NOT NULL DEFAULT 0,
    level_ INTEGER NOT NULL DEFAULT 0
  );

CREATE TABLE
  IF NOT EXISTS levels_background(guild_id BIGINT, background TEXT DEFAULT NULL);

CREATE TABLE
  IF NOT EXISTS font_colors(guild_id BIGINT, color TEXT DEFAULT '255,255,255');