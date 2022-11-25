from django_filters import FilterSet, DateTimeFilter
from .models import *
from django import forms


class PostFilter(FilterSet):
    post_time = DateTimeFilter(label='Publication date', field_name='post_time', lookup_expr='date__gte',
                               widget=forms.DateInput(
                                  attrs={'type': 'date'}
                               )
                               )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'post_author': ['in'],
             }
