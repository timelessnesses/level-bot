# Levellable

A easy/configurable/lots of features for your need!  

## How to host this???

### Requirement

- Python 3.8 or higher
- poetry (`pip install poetry`)
- postgresql database

### Procedure

1. Setup your postgresql database

2. You can either make your own .env file and fill out these

```env
LEVEL_TOKEN=bot token
LEVEL_PREFIX=prefix 
LEVEL_DATABASE_HOST=database's ip or domain
LEVEL_DATABASE_PORT=database's port
LEVEL_DATABASE_USER=database's user
LEVEL_DATABASE_PASSWORD=database's password
LEVEL_DATABASE_NAME=database's name
LEVEL_DATABASE_SSL=connect database with ssl or not (0 or 1)
```

2.1 You can edit `config/config.py` to your own choice too

```py
from dotenv import load_dotenv

load_dotenv()
import os

from dotenv import load_dotenv

load_dotenv()
import os

token = "bot token"
prefix = "prefix"
database_host = "database's ip or domain"
database_port = "database's port"
database_name = "database's name"
database_user = "database's user"
database_password = "database's password"
database_ssl = True or False based on your need
database_url = "paste your entire postgresql connection string here if you don't want to fill each items above"

```

3. Do `poetry install`

4. Do `poetry shell` to activate the virtual environment

5. Run `python3 bot.py`

6. Enjoy~

## Features

- [x] Level system
- [x] Boost up your level by doing activities
- [x] Be able to set your own level requirement for something important like limiting new members to posting files or joining voice chat (by manage your own role)
