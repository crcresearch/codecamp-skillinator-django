"""skillsmatrix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from skillsmatrix.views.home import *
from skillsmatrix.views.developer import *


urlpatterns = [
    url(r'^$', Home.as_view()),
    url(r'^developers/$', DeveloperList.as_view(), name="developer_list"),
    url(r'^developers/(?P<manager>\w+)/$', DeveloperListByManager.as_view()),
    url(r'^developer_detail/(?P<pk>\d+)/$', DeveloperDetail.as_view(), name="developer_detail"),
    url(r'^my_developer_details/$', DeveloperDetailMe.as_view(), name="my_developer_details"),
    url(r'^developer/(?P<pk>\d+)/update/$', DeveloperUpdate.as_view(), name="developer_update"),
    url(r'^extracredit/send/$', ExtraCreditCreateView.as_view(), name="send_extra_credit"),
]
