#!/bin/bash

rm -rf rareserverapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations rareserverapi
python manage.py migrate rareserverapi
python manage.py loaddata users.json
python manage.py loaddata rareusers.json
python manage.py loaddata categories.json
python manage.py loaddata reactions.json
python manage.py loaddata tags.json
python manage.py loaddata posts.json
python manage.py loaddata postreactions.json
python manage.py loaddata posttags.json
python manage.py loaddata comments.json
python manage.py loaddata subscriptions.json
python manage.py loaddata tokens.json