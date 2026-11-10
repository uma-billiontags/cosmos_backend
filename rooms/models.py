import uuid
from django.db import models
from django.conf import settings

class Space(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='spaces')
    admin_access = models.BooleanField(default=True)
    is_free = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

class SpaceMember(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='space_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('space', 'user')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.name} ({self.role}) in {self.space.name}"

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('permanent', 'Permanent'),
        ('temporary', 'Temporary'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='temporary')
    capacity = models.PositiveIntegerField(default=20)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type}) - Cap: {self.capacity}"
