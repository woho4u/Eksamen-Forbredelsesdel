from django_filters.rest_framework import DjangoFilterBackend
from .filters import MealplanFilter
from rest_framework.filters import SearchFilter

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import Mealplan
from .serializers import MealplanSerializer, AddRecipeSerializer
from recipes.models import Recipe


class MealplanViewSet(viewsets.ModelViewSet):
    queryset = Mealplan.objects.all()
    serializer_class = MealplanSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MealplanFilter
    search_fields = ['title', 'occasion']

    @action(
        detail=True,
        methods=["post"],
        serializer_class=AddRecipeSerializer         # <-- serializer for input (recipe_id for add_recipe)
    )
    def add_recipe(self, request, pk=None):
        mealplan = self.get_object()

        # 1) Valider JSON/stringen med serializeren
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        recipe_id = input_serializer.validated_data["recipe_id"]

        # 2) hent oppskriften og kjør logikken
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            mealplan.add_recipe(recipe)
        except ValidationError as exc:
            return Response({"detail": str(exc)}, status=422)

        # 3) serialize the UPDATED mealplan with the normal serializer
        output_serializer = MealplanSerializer(
            mealplan, context=self.get_serializer_context()
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)
