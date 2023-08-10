from django.db import models
from django.contrib.auth.models import User


# Signal imports
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_last = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    adress = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=20)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class UserGroup(models.Model):
    VISIBILITY_CHOICES = [('public', 'Public'), ('private', 'Private')]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='user_groups', blank=True)
    records = models.ManyToManyField(Record, related_name='group_records', blank=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, null=False, related_name='admin_groups', blank=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# I do not think this works
# @receiver(pre_save, sender=UserGroup)
# def set_admin_and_member(sender, instance, **kwargs):
#     if instance.admin is None:
#         instance.admin = instance.creator
#     if instance.creator not in instance.members.all():
#         instance.members.add(instance.creator)

"""
from django.contrib.auth.models import User
from website.models import Record, UserGroup

record = Record.objects.first()
person = User.objects.filter(username='admin')[0]

grp = UserGroup.objects.create(name='First Group', description='First group description', visibility='public')
grp.members.set([])
grp.save()
"""