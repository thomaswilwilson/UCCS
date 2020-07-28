from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('<int:code>/', views.namepage, name='name'),
    path('<int:code>/<int:individual>/', views.prefs, name='pref'),
    path('<int:code>/final/', views.final, name = 'final'),
    path('<int:code>/wait/', views.wait, name = 'wait')
]
