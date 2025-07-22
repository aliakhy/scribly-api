from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete
from .models import Article
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(pre_save)
def del_old_image(sender,instance, **kwargs):
    if sender == Article:
        image_field_name='image'
    elif sender== User :
        image_field_name='avatar'
    else:
        return
    if not instance.pk :
        return
    try :
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist :
        return
    old_image= getattr(old_instance,image_field_name)
    new_image = getattr(instance,image_field_name)
    if old_image and old_image.name != new_image.name:
        try:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
        except Exception :
            pass


@receiver(post_delete)
def delete_image_on_delete(sender, instance,  **kwargs):
    if sender == Article:
        image_field_name='image'
    elif sender== User :
        image_field_name='avatar'
    else:
        return
    image= getattr(instance,image_field_name)
    if image:
        try :
            os.remove(image.path)
        except :
            pass


