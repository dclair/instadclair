from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Follow(models.Model):
    """Model to handle user following relationships."""

    follower = models.ForeignKey(
        "UserProfile",
        on_delete=models.CASCADE,
        related_name="following_relationships",
        verbose_name="Seguidor",
    )
    following = models.ForeignKey(
        "UserProfile",
        on_delete=models.CASCADE,
        related_name="follower_relationships",
        verbose_name="Seguido",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Desde cuándo lo sigue"
    )

    class Meta:
        verbose_name = "Seguidor"
        verbose_name_plural = "Seguidores"
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        "Imagen del perfil", upload_to="profile_pictures/", blank=True, null=True
    )
    bio = models.TextField("Biografia", blank=True, null=True)
    birth_date = models.DateField("Fecha de nacimiento", blank=True, null=True)
    location = models.CharField("Ubicación", max_length=100, blank=True, null=True)
    website = models.URLField("Website", blank=True, null=True)

    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        through="Follow",
        blank=True,
        verbose_name="Seguidores",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def followers_count(self):
        return self.follower_relationships.count()

    def following_count(self):
        return self.following_relationships.count()

    def is_following(self, profile):
        """
        Verifica si este perfil está siguiendo al perfil dado
        """
        return self.following_relationships.filter(following=profile).exists()

    def is_followed_by(self, profile):
        """
        Devuelve True si el perfil recibido sigue a este perfil
        """
        if not profile:
            return False
        return self.follower_relationships.filter(follower=profile).exists()

    def follow(self, profile):
        if profile and profile != self:
            Follow.objects.get_or_create(follower=self, following=profile)

    def __str__(self):
        return self.user.username
