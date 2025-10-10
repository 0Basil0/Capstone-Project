from django.db import models
from django.contrib.auth.models import User


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
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
