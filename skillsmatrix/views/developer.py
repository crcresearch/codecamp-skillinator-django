# View file for developer pages

from django.views.generic import *

class DeveloperList(ListView):
    pass


class DeveloperListByManager(DeveloperList):
    pass

class DeveloperDetail(DetailView):
    pass

class DeveloperDetailMe(DeveloperDetail):
    pass

class DeveloperUpdate(UpdateView):
    pass

class ExtraCreditCreateView(CreateView):
    pass


