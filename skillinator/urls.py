"""skillinator URL Configuration

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
from django.contrib import admin

from skillsmatrix.views import MySkills, HomePage
from skillsmatrix.homework import ProblemTwo, ProblemThree

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # For tutorial
    url(r'^myskills/', MySkills),
    url(r'^homepage/', HomePage),

    # URL for problem two
    url(r'^problem-two/', ProblemTwo, name='problem_two'),

    # Give access to some of the views for the testing/code coverage homework
    url(r'^problem-three/', ProblemThree, name='problem_three'),
]
