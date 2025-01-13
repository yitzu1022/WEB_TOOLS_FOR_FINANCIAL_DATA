"""
URL configuration for NCKU project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from sum import views as sum_view
from HW1 import views as HW1_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sum/', sum_view.sum),
    path('HW1/', HW1_view.HW1),
    path('ajax_sum/', sum_view.ajax_sum),
    path('ajax_showStock/', HW1_view.ajax_showStock),
]
