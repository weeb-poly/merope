FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.21 /uv /uvx /bin/

# Copy the project into the image
COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Run discord_reg_bot
CMD ["sh", "-c", "uv run --package discord-reg-bot setup_db && uv run --package discord-reg-bot bot"]
