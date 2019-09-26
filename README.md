# Agent of the King

### Setup
Requirements: docker, docker-compose, a [discord bot](https://discordapp.com/developers/docs/intro)

1. `cp .env.example .env`
2. Add your bot token to `.env`
3. `docker-compose up -d --build`

For local development, run `docker attach arkham_py` to attach to the container interactively, and respond to `pdb` statements
Run `docker-compose restart arkham_py` to restart bot to apply changes