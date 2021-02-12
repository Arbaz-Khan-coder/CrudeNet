import django_filters 
from .models import *
from django_filters import DateFilter,CharFilter


class PostFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name = "date_posted", lookup_expr = "gte")
    end_date = DateFilter(field_name = "date_posted", lookup_expr = "lte")
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["date_posted","content"]