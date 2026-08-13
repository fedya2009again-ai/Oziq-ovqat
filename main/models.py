from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=200)

    description = models.TextField()

    ingredients = models.TextField()

    category = models.CharField(max_length=100)

    servings = models.PositiveIntegerField(
        help_text="Necha kishiga"
    )

    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )

    step_number = models.PositiveIntegerField()

    title = models.CharField(max_length=200)

    description = models.TextField()

    time_minutes = models.PositiveIntegerField(
        help_text="Bu qadam necha daqiqa davom etadi?"
    )

    def __str__(self):
        return f"{self.recipe.name} - {self.step_number}-qadam"