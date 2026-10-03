# Matrix Invite Bot

Our primary Matrix Space is Private with Federation. The goal was to allow people to reuse existing matrix accounts.
We create new matrix users on the home server for people who don't have an existing matrix account and probably won't use one outside of this.

tuwunel doesn't allow us to auto join or auto invite users to a private room / space, so this bot will invite users to join the primary space whenever a new member joins a public unfederated holding room (set using `auto_join_rooms`).

## Env

```
MATRIX_USER={{Matrix Bot User ID}}
MATRIX_PASSWORD={{Matrix Bot Password}}
MATRIX_SERVER={{Matrix Server / API endpoint}}
TEMP_ROOM={{Matrix Room ID}}
INVITE_ROOM={{Matrix Room ID}}
```

## Run

```
deno run --env-file ./merope-matrix-bot/index.ts
```

## Build

```
deno compile -A --env=.env --target x86_64-unknown-linux-gnu --output matrix-bot-build ./merope-matrix-bot/index.ts
```

## Podman

```
podman build -f merope-matrix-bot/Dockerfile -t merope-matrix-bot .
podman run --rm --env-file .env merope-matrix-bot
```
