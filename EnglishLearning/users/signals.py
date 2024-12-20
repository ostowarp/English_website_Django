from django.contrib.auth.models import User
from .models import Profile

# import signal method:
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete


# create and update user:
def createProfile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
    else:
        profile = user.profile
        profile.name = user.first_name
        profile.username = user.username
        profile.email = user.email
        profile.save()


# delete User after delete Profile:
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


# update profile after update user:
def updateProfile(sender, instance, **kwargs):
    user = instance
    profile = user.profile
    profile.username = user.username
    profile.email = user.email
    profile.first_name = user.first_name
    profile.last_name = user.last_name
    profile.save()

# connect signals:
post_save.connect(createProfile, sender=User, dispatch_uid='create_profile')
post_delete.connect(deleteUser, sender=Profile, dispatch_uid='delete_user')
post_save.connect(updateProfile, sender=User, dispatch_uid='update_profile')
