from django.conf.urls import url
from . import views

app_name = "appointments"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_task$', views.add_task, name='add_task'),
    url(r'^edit_task$', views.edit_task, name='edit_task'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name='destroy'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^errors$', views.errors, name='errors')
]
