#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

cd smartcampus
python manage.py collectstatic --no-input
python manage.py migrate

# Seed data: load initial data if database is empty
# We check if there are any blocks, if not, we load the fixture
python manage.py shell -c "
from navigator.models import Block
from django.core.management import call_command

if Block.objects.count() == 0:
    print('Seeding database with initial data...')
    import os; call_command('loaddata', os.path.join(os.getcwd(), 'seed_data.json'))
    print('Database seeded!')
else:
    print('Database already has data, skipping seed.')
"
