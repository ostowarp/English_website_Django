from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from .models import  FlashCard , Profile ,DeckImage
import os



def delete_image(sender, instance, **kwargs):
    # حذف فایل تصویر از سیستم فایل
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)
post_delete.connect(delete_image , sender=DeckImage)


