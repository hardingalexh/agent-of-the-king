# Agent of the King

## Setup
Requirements: docker, docker-compose, a [discord bot](https://discordapp.com/developers/docs/intro)

1. `cp .env.example .env`
2. Add your bot token to `.env`
3. `docker-compose up -d --build`

For local development, run `docker attach arkham_py` to attach to the container interactively, and respond to `pdb` statements
Run `docker-compose restart arkham_py` to restart bot to apply changes


## Commands


### Arkhamdb-related

If a message includes a link to a deck on arkhamDB, it will be parsed and displayed. Additionally, any text included between double brackets will be treated as `!card` input. For example, `!card ward of protection` is the same as including `[[ward of protection]]` in a message.


```
!refresh
```
Re-fetches the card pool from arkhamdb.

```
!card [text] ([level])
```
Searches for a card. Optionally include a level in parentheses. For example, `!card ward of protection` will return all copies, `!card ward of protection (2)` will only return the level 2, and `!card ward of protection(u)` will return all upgraded copies.

```
!weakness *traits
```
Searches for a random basic weakness. Define any number of parameters. These are not additive - searching `!weakness madness pact` will not only allow weaknesses that are both madness AND pact, it will allow weaknesses that are madness AND/OR pact.

```
!weaknesses <quantity> [solo or multi, default multi]
```
Picks `<quantity>` random basic weaknesses, ignoring "campaign mode only" weaknesses. If "solo" is passed as the second argument, also ignores all "multiplayer only" weaknesses.

```
!shrewdanalysis [card]
```
Performs the random search function for [shrewd analysis](https://arkhamdb.com/card/04106). This function respects card quantities and pulls a sample of two cards without replacement from the collection.

```
!investigator [faction]

Chooses a random investigator, optionally for a given faction.
```
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

### Blob
State management for Arkham's "The Blob That Ate Everything" Secnario

```
!blob setup X
```
Sets up blob event for X number of investigators

```
!blob status
```
Prints the status of all current blob attributes (damage, supplies, clues)

```
!blob [param] [quantity]
```
Increments the various blob attributes and prints status. Valid params are `countermeasures`, `clues` and `damage`. Quantity can be negative. For example, `!blob countermeasures 2` adds two countermeasures, `!blob clues -10` spends 10 clues.


### Randomization and dice

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



### Funkoverse Strategy Game

```
funko [dice] [character=none]
```
Rolls dice for the funkoverse strategy game. Optional characters parameter for characters with special dice (like Ian Malcolm). 