from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryList.as_view(), name='category'),
    path('post/<str:slug>/', PostDetail.as_view(), name='detail'),
    path('tag/<str:slug>/', TagView.as_view(), name='tag'),
    path('search/', SearchView.as_view(), name='search')
    # path('', index, name='home'),
    # path('category/<str:title>/', category, name='category'),
]
