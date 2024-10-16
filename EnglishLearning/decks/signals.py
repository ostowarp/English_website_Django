from django.db.models.signals import post_save , pre_save , post_delete , pre_delete



def createcontent(sender , instance , created , **kwargs):
    if created:
        content = instance
        