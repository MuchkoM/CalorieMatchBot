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

In [BotFather](https://t.me/botfather) add command description from [bot_description.txt](./bot_description.txt)

For installing dependencies use [reqirements.txt](reqirements.txt) or [Pipfile](Pipfile)