from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^member/signup/$', views.signup, name='signup'),
    url(r'^member/login/$', views.login, name='login'),
    url(r'^member/logout/$', views.logout, name='logout'),

]