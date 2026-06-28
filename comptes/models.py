from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('cooperative', 'Coopérative'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    # Redéfinition pour éviter les conflits avec auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='comptes_user_groups',
        related_query_name='comptes_user',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='comptes_user_permissions',
        related_query_name='comptes_user',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    adresse = models.TextField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profil client de {self.user.username}"


class CooperativeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cooperative_profile')
    nom_cooperative = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    est_validee = models.BooleanField(default=False)

    def __str__(self):
        return f"Coopérative {self.nom_cooperative}"