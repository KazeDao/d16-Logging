from django.urls import path, include
from .views import *

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='new'),
    path('news/create/', PostCreate.as_view(), name='create'),
    path('articles/create/', PostCreate.as_view(), name='create'),
    path('<int:pk>/edit', PostEdit.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
