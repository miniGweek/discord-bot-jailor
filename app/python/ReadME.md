# Introduction

This is a companion discord bot for the quite popular bot called `counting`.

- `counting` bot website @ https://counting.duckgroup.xyz/
- `counting` bot top.gg listing @ https://top.gg/bot/510016054391734273

This bot will lock your `counting` channel if the guild saves fall below 1.

The bot requires the following permissions

- Manage channel
- Modify permissions
- Send message
- Read message

## Build Docker Image

Run the powershell script `build.ps` to build and push to the docker registry

```PowerShell
 app\python\scripts\build.ps1 -tag '0.4'
```

## Run Docker Image

### Environment Variables

- Set a local environment variable with the Bot's token `DISCORD_BOT_JAILOR_TOKEN`

### Launch container

The logs for the bot will be generated in the `bot_logs` folder in the current working directory.

```PowerShell
docker run --rm -d -e DISCORD_BOT_JAILOR_TOKEN -v $pwd/bot_logs`:/src/logs --name jailor minigweek/discord-bot-jailor:0.3
```

## Other info

The discord bot token environment file has to be stored inside /etc/profile.d/discord-bot-jailor.sh
in the format.
export ENV_VAR_KEY=VALUE

## Tests

You currently have 0/3 saves.

j!debug Guild Saves: **0.0/2**
j!debug Guild Saves: **0.4/2**
j!debug Guild Saves: **1.0/2**
j!debug Guild Saves: **1.4/2**
j!debug Guild Saves: **2.0/2**

j!debug There are **0.0/2** guild saves left.
j!debug There are **0.8/2** guild saves left.
j!debug There are **1.0/2** guild saves left.
j!debug There are **1.2/2** guild saves left.
j!debug There are **2.0/2** guild saves left.

j!debug for a total of `0.0/2` guild saves.
j!debug for a total of `0.8/2` guild saves.
j!debug for a total of `1.0/2` guild saves.
j!debug for a total of `1.4/2` guild saves.
j!debug for a total of `2.0/2` guild saves.
