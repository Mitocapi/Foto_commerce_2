from django.db import models
from django.contrib.auth.models import User  # Import the User model from Django's built-in auth

class Foto(models.Model):
    COLOUR_CHOICES = [
        ("Black", "Black"),
        ("Dark Blue", "Dark Blue"),
        ("Green", "Green"),
        ("Grey", "Grey"),
        ("Light Blue", "Light Blue"),
        ("Orange", "Orange"),
        ("Pink", "Pink"),
        ("Purple", "Purple"),
        ("Red", "Red"),
        ("White", "White"),
        ("Yellow", "Yellow"),
    ]

    name = models.CharField(max_length=50)
    main_colour = models.CharField(max_length=20, choices=COLOUR_CHOICES)
    landscape = models.BooleanField()
    actual_photo = models.ImageField(upload_to='APPfoto/static')
    artist = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        if self.landscape:
            return f"Nome foto: {self.name}, scattata da: {self.artist}, colore principale: {self.main_colour}, ed è una foto landscape."
        else:
            return f"Nome foto: {self.name}, scattata da: {self.artist}, colore principale: {self.main_colour}, ed è una foto portrait."

