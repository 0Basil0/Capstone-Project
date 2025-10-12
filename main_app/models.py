from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

class Food(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Allergy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    food = models.ManyToManyField(Food, blank=True, related_name='allergies')
    def __str__(self):
        return f"{self.name} ({self.user.username})"


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    breakfast = models.ForeignKey(Food, related_name='breakfast_meals', on_delete=models.SET_NULL, null=True, blank=True)
    lunch = models.ForeignKey(Food, related_name='lunch_meals', on_delete=models.SET_NULL, null=True, blank=True)
    dinner = models.ForeignKey(Food, related_name='dinner_meals', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.day}"


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Session identifier to group multiple messages into a conversation..
    session_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def preview(self):
        # A short preview of the conversation entry.
        text = (self.user_message or '')
        if len(text) > 80:
            return text[:77] + '...'
        return text
class Profile(models.Model):
    # Simple profile to store extra user attributes like age.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
