#!/bin/bash
cd /home/django/barter_site/
python manage.py rebuild_index
y
cd /home/django/barter_site/barter_site/
chmod 777 whoosh_index