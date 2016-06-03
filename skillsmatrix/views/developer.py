# View file for developer pages
import datetime

from django.views.generic import *
from skillsmatrix.models import Developer, DeveloperSkill, ExtraCredit
from django.core.urlresolvers import reverse

class DeveloperList(ListView):

    model = Developer
    template_name = 'developer_list.html'

    def get_context_data(self, **kwargs):
        context = super(DeveloperList, self).get_context_data(**kwargs)
        return context

class DeveloperListByManager(DeveloperList):

    def get_queryset(self):
        q = super(DeveloperListByManager, self).get_queryset()
        return q.filter(manager = self.kwargs['manager'])

class DeveloperDetail(DetailView):
    model = Developer
    template_name = 'developer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DeveloperDetail, self).get_context_data(**kwargs)
        context['skills'] = DeveloperSkill.objects.filter(developer = self.object).order_by('-years_of_experience')
        return context

class DeveloperDetailMe(DeveloperDetail):

    def get_object(self):
        return Developer.objects.get(user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DeveloperDetail, self).get_context_data()
        context['skills'] = DeveloperSkill.objects.filter(developer = self.object)#.order_by('-years_of_experience')
        return context

class DeveloperUpdate(UpdateView):
    model = Developer
    template_name = 'developer_update.html'
    fields = ['title']

    def form_valid(self, form):
        return super(DeveloperUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('developer_detail', kwargs={'pk': self.object.id})

class ExtraCreditCreateView(CreateView):
    model = ExtraCredit
    template_name = 'extracredit_create.html'
    fields = ['recipient', 'skill', 'description']

    def form_valid(self, form):
        form.instance.sender = Developer.objects.get(user = self.request.user)
        form.instance.date_created = datetime.datetime.now()
        return super(ExtraCreditCreateView, self).form_valid(form)

    def get_success_url(self):
        obj = Developer.objects.get(user = self.request.user)
        obj.extra_credit_tokens -= 1
        obj.save()
        return reverse('developer_detail', kwargs={'pk': self.object.sender.id})


