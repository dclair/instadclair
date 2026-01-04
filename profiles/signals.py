from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserProfile

User = get_user_model()


def should_create_profile(user):
    """
    Determina si se debe crear un perfil para el usuario.
    No creamos perfiles para superusuarios o personal administrativo.
    """
    return not (user.is_superuser or user.is_staff)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the user profile for non-admin users
    """
    # Solo crear/actualizar perfiles para usuarios regulares
    if not should_create_profile(instance):
        return

    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)
