from django.urls import path

from .views import homePageView, transferView, confirmView, addView, mailView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('confirm/', confirmView, name='confirm'),
    path('add/', addView, name='add'),
    path('mail/', mailView, name='mail'),
]
