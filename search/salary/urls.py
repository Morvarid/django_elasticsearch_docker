
from django.conf.urls import url

from search.salary import views

urlpatterns = [
    url(r'^v1/salary[/]?$', views.search_salary),
    url(r'^v1/upload[/]?$', views.excel_to_es_load)
]
