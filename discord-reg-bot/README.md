# Discord Registration Bot

This bot will help Discord users register on Matrix.

## Env

```
DISCORD_TOKEN={{Discord > Bot > Token}}
MATRIX_SERVER={{Synapse API Host}}
MATRIX_REG_SHARED_SECRET={{Tuwunel registration_shared_secret}}
```

## Run

```
uv run --package discord-reg-bot setup_db
uv run --env-file .env --package discord-reg-bot bot
```
