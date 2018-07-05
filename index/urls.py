from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^score/$',views.score,name='score'),
    url(r'^add/$',views.add,name='add'),
    url(r'^mostgoal_difference/$',views.mostgoal_difference,name='mostgoal_difference'),
    url(r'^score_difference/$',views.score_difference,name='score_difference'),
    url(r'^promotion/$',views.promotion,name='promotion'),
]


