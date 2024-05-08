from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def setup_groups(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(Permission)
    admin_permission = Permission.objects.create(codename='admin', name='Manage DB and users', content_type=content_type)

    Group.objects.create(name='guests')
    admin_group = Group.objects.create(name='admins')
    admin_group.permissions.add(admin_permission)
