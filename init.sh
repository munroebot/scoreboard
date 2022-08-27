#!/bin/bash

sqlite3 scoreboard.db < create.sql;
gunicorn --bind 0.0.0.0:8000 -D --pid /tmp/gunicorn.pid runserver:app