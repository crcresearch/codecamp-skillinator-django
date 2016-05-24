# View file for developer pages

from django.views.generic import *
from skillsmatrix.models import *

class DeveloperList(ListView):
    template_name = 'developer_list.html'
    model = Developer


class DeveloperListByManager(DeveloperList):
    def get_queryset(self):
        qs = super(DeveloperList, self).get_queryset()
        return qs.filter(manager=self.kwargs['manager'])

class DeveloperDetail(DetailView):
    model = Developer
    template_name = 'developer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DeveloperDetail, self).get_context_data(**kwargs)
        context['skills'] = DeveloperSkill.objects.filter(developer_id=self.kwargs['pk']).order_by('-years_of_experience')
        return context


class DeveloperDetailMe(DeveloperDetail):
    def get_object(self):
        return Developer.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DeveloperDetail, self).get_context_data(**kwargs)
        context['skills'] = DeveloperSkill.objects.filter(developer=kwargs['object'])
        return context


class DeveloperUpdate(UpdateView):
    model = Developer
    fields = ['manager']
    template_name = 'developer_update.html'

    def get_success_url(self):
        return '/my_developer_details/'


class ExtraCreditCreateView(CreateView):
    model = ExtraCredit
    template_name = 'extracredit_create.html'
    fields = ['recipient', 'skill', 'description']

    def form_valid(self, form):
        form.instance.sender = Developer.objects.get(user=self.request.user)
        return super(ExtraCreditCreateView, self).form_valid(form)


    def get_success_url(self):
        return '/my_developer_details/'
