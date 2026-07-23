#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed initial database
python manage.py seed_data

# Collect static files
python manage.py collectstatic --no-input
