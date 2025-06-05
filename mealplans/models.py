from django.db import models
from recipes.models import Recipe
from django.core.exceptions import ValidationError

class Mealplan(models.Model):
    title = models.CharField(max_length=255)
    recipes = models.ManyToManyField(Recipe, through="MealplanRecipe", related_name="mealplans")
    occasion = models.CharField(max_length=255, default="general")

    def __str__(self):
        return

    def add_recipe(self, recipe: Recipe):
        existing = self.recipes.all()

        # First recipe is always allowed
        if not existing.exists():
            self.recipes.add(recipe)
            return

        # a) categories must all be different
        used_categories = set(existing.values_list("category", flat=True))
        if recipe.category in used_categories:
            raise ValidationError(
                f"Category'{recipe.category}' already exists in this mealplan."
            )

        # b) flavor profile overlap with all existing recipe
        new_flavor_profiles= set(recipe.flavor_profiles)
        for other in existing:
            if not new_flavor_profiles.intersection(other.flavor_profiles):
                raise ValidationError(
                    f"No shared flavor profile with '{other.title}'. "
                    "Each pair must share at least one keyword."
                )

        self.recipes.add(recipe)

class MealplanRecipe(models.Model):
    """Through-table"""
    mealplan = models.ForeignKey(Mealplan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mealplan", "recipe")  # can’t add the same recipe twice