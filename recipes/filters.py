import django_filters
from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    # allow ?id_in=1,2,3 for multiple IDs
    id_in = django_filters.BaseInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = Recipe
        fields = ['id_in', 'category', 'title']