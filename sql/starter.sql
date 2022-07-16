CREATE TABLE IF NOT EXISTS user_(
    user_id BIGSERIAL PRIMARY KEY,
    experience INTEGER,
    is_in_voice_channel BOOLEAN,
    when_in_voice_channel TIMESTAMP
);

CREATE TABLE IF NOT EXISTS guild(
    guild_id BIGSERIAL PRIMARY KEY,
    starboard_channel_id INTEGER
);