from rest_framework import serializers
from .models import Mealplan
from recipes.serializers import RecipeSerializer

class MealplanSerializer(serializers.ModelSerializer):
    # read-only list av recipes
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model  = Mealplan
        fields = ["id", "title", "recipes", "occasion"]

class AddRecipeSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()