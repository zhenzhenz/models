"""software_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from search.views import search,main
from results.views import results,ajax_test
from micro_recommendation.views import recommendation,recommendation_results
from multi_micro_system.views import multi_system,multi_sysytem_results

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^search/$',search),
    url(r'^results/$',results),
    url(r'^recommendation/$',recommendation),
    url(r'^recom_results/$',recommendation_results),
    url(r'^multi_sysytem/$',multi_system),
    url(r'^multi_sysytem_results/$',multi_sysytem_results),
    url(r'^Alpha ant/$',main),
    url(r'^test_ajax/$',ajax_test),
    url(r'^admin/', admin.site.urls,name='admin')
]
