FROM denoland/deno:latest AS base

# Build stage
FROM base AS builder

WORKDIR /app

# Copy the project into the image
COPY . /app

RUN --mount=type=cache,target=/deno-dir \
    deno ci --prod --skip-types

RUN --mount=type=cache,target=/deno-dir \
    deno bundle -o merope-matrix-bot.js ./merope-matrix-bot/index.ts

# Production stage
FROM base

COPY --from=builder /app/merope-matrix-bot.js .

CMD ["run", "-A", "merope-matrix-bot.js"]
