from django.contrib.auth.models import User
from .models import Profile

# import signal method:
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete


# create and update user:
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
    else:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# delete User after delete Profile:
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)
