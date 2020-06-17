# Agent of the King

## Setup
Requirements: docker, docker-compose, a [discord bot](https://discordapp.com/developers/docs/intro)

1. `cp .env.example .env`
2. Add your bot token to `.env`
3. `docker-compose up -d --build`

For local development, run `docker attach arkham_py` to attach to the container interactively, and respond to `pdb` statements
Run `docker-compose restart arkham_py` to restart bot to apply changes


## Commands


### Arkham-related
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


```
!upgrade [card]
```
Searches for all matches for the card name that are not level 0, and returns a random version of it. For upgrading journey cards like archaic glyphs/strange solution.

```
!investigator [faction]

Chooses a random investigator, optionally for a given faction.
```

### Randomization

```
!cointoss
```
Returns heads or tails

```
!roll [dice: format XdY where X is quantity of dice, Y is sides on die]
```
Rolls dice and returns results.

```
pickone
```
Picks one from the space separated list of arguments


### Chaos Bag

The symbol tokens are `skull`, `cultist`, `tablet`, `elder-thing`, `auto-fail`, `elder-sign`.


```
!bag list
```
Lists the contents of the bag


```
!bag add [space separated tokens]
```
Adds tokens to the bag

```
!bag remove [space separated tokens]
```
Removes tokens from the bag

```
!bag draw X (optional)
```
Draws X tokens, default 1

```
!bag return
```
Returns revealed tokens to the bag


```
!bag revealed
```
Lists currently revealed tokens
