# Agent of the King

### Setup
Requirements: docker, docker-compose, a [discord bot](https://discordapp.com/developers/docs/intro)

1. `cp .env.example .env`
2. Add your bot token to `.env`
3. `docker-compose up -d --build`

For local development, run `docker attach arkham_py` to attach to the container interactively, and respond to `pdb` statements
Run `docker-compose restart arkham_py` to restart bot to apply changes


### Commands

```
!refresh
```
Re-fetches the card pool from arkhamdb.

```
!card [text] [level]
```
Searches for a card. Note that cards with multiple words require spaces. For example, searching for "Prepared for the worst" would require `!card "prepared for the worst"`. If 3 or less results are found it will send all of them with pictures, if more than 3 it will just return card titles, if more than 10 it returns a message saying that it can't return that many.

```
!weakness *traits
```
Searches for a random basic weakness. Define any number of parameters. These are not additive - searching `!weakness madness pact` will not only allow weaknesses that are both madness AND pact, it will allow weaknesses that are madness AND/OR pact.

