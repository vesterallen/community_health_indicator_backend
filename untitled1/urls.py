"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from community_health_ind import views
from community_health_ind.views import sample
from community_health_ind.views import findCounty
from community_health_ind.views import findCountyList
from community_health_ind.views import findDiseaseList

urlpatterns = [
    url(r'^authenticate/(?P<username>.+)/(?P<pwd>.+)/', sample, name='sample'),
    url(r'^county/(?P<countyName>.+)/', findCounty, name='findCountyInfo'),
    url(r'^admin/', admin.site.urls),
    url(r'^disease/(?P<disease_name>.+)/', findCountyList),
    url(r'^disease/(?P<disease_name>.+)/(?P<limit>.+)/', findCountyList),
    url(r'^countyname/(?P<cnty_name>.+)/', findDiseaseList),
    url(r'^login/(?P<usrname>.+)/(?P<password>.+)/', views.login, name='login')
]
