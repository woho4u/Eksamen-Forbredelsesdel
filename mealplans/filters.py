import django_filters
from .models import Mealplan

class MealplanFilter(django_filters.FilterSet):
    # allow ?id_in=1,2,3 for multiple IDs
    id_in = django_filters.BaseInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = Mealplan
        fields = ['id_in', 'title', 'occasion']