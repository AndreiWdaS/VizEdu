from django.urls import path
from . import views

urlpatterns = [
    path('line_chart/', views.line_chart, name='line_chart'),
    path('bar-chart/', views.bar_chart, name='bar_chart'),
    path('scatter-chart/', views.scatter_chart, name='scatter_chart'),
    path('graph/', views.choropleth_map, name='graph'),
]
