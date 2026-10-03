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
uv run --package merope-discord-bot merope-discord-bot-setup-db
uv run --env-file .env --package merope-discord-bot merope-discord-bot
```

## Podman

```
podman build -f merope-discord-bot/Dockerfile -t merope-discord-bot .
podman run --rm --env-file .env -v ./users.db:/app/users.db merope-discord-bot
```
