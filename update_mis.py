import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrla_hub.settings')
django.setup()

from django.contrib.auth.models import User

# Remove old BPO user
User.objects.filter(username='BPO').delete()

# Create new MIS Executive user
mis_user, created = User.objects.get_or_create(username='mis')
mis_user.set_password('MIS123')
mis_user.is_staff = True
mis_user.save()

from django.contrib.auth.models import Group
bpo_group = Group.objects.get(name='BPO Team')
mis_user.groups.set([bpo_group])
print("Created MIS Executive User: mis / MIS123")
