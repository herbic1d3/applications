import os
import random
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
from django.conf import settings
from django.contrib.auth.management.commands.createsuperuser import get_user_model

django.setup()

# --------------------
# create superuser if not exist

User = get_user_model()
if User.objects.filter(email=os.environ.get('DJANGO_SU_EMAIL')).exists():
    print('Super user already exists. SKIPPING...')
else:
    print('Creating super user...')
    User.objects.create_superuser(
        os.environ.get('DJANGO_SU_EMAIL').split('@')[0],
        os.environ.get('DJANGO_SU_EMAIL'),
        os.environ.get('DJANGO_SU_PASSWORD'),
    )
    print('Super user created...')
