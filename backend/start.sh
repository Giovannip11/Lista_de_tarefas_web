#!/usr/bin/env bash

gunicorn "app:create_app()" \
  --bind 0.0.0.0:$PORT
