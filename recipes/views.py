from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
from rest_framework.filters import SearchFilter

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RecipeFilter
    search_fields = ['title', 'category', 'flavor_profiles']  # keep search for text if desired
