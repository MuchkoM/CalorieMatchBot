# CalorieMatchBot
Calculate calories every day
## Installing
Create .env.bot file and use format:

    TOKEN=<bot_token>.

bot_token must be got from [BotFather](https://t.me/botfather)

Create .env.db and use format:

    host = <host>
    port = <port>
    user = <db_login>
    password = <db_pass>
    database = <db_schema>

Bot support only MySql database

For installing dependencies use [requirements.txt](requirements.txt) or [Pipfile](Pipfile)

In [BotFather](https://t.me/botfather) add output of  **/help** command in **Edits Commands** menu without begin /