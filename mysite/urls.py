"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kb_platform import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('index/', views.index),
    # path('user-profile/', views.user_profile),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),

    path('faq/', views.faq),
    path('contact/', views.contact),

    path('charts/', views.charts),
    path('total-accounts/', views.total_accounts),
    path('accounts/', views.accounts),
    path('alarms/', views.alarms),
    path('cards/', views.cards),
    path('transfer/', views.transfer),
    path('find_kb/', views.find_kb),
    path('cards_recom/', views.cards_recom),
    path('stock/', views.stock),
    path('stock_game/', views.stock_game),
    path('myAsset/', views.myAsset),
    path('myGold/', views.myGold),
    path('stock_charts/', views.stock_charts),
    path('attendance/', views.attendance),

    path('stock_account/', views.stock_account),
]
