# View file for developer pages

from django.views.generic import *
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from skillsmatrix.models import *


class DeveloperList(ListView):
    template_name = 'developer_list.html'
    model = Developer


class DeveloperListByManager(DeveloperList):
    template_name = 'developer_list.html'

    def get_queryset(self):
        queryset = super(DeveloperListByManager, self).get_queryset()
        return queryset.filter(manager=self.kwargs['manager'])


class DeveloperDetail(DetailView):
    template_name = 'developer_detail.html'
    model = Developer

    def get_context_data(self, **kwargs):
        context = super(DeveloperDetail, self).get_context_data(**kwargs)
        context['skills'] = DeveloperSkill.objects.filter(developer_id=self.kwargs['pk'])\
            .order_by('-years_of_experience')

        return context


class DeveloperDetailMe(DeveloperDetail):
    def get_object(self, queryset=None):
        developer = get_object_or_404(Developer, user_id=self.request.user.id)
        self.kwargs['pk'] = str(developer.pk)

        return developer


class DeveloperUpdate(UpdateView):
    model = Developer
    template_name = 'developer_update.html'

    def get_success_url(self):
        return reverse_lazy('developer_detail', kwargs={'pk': self.kwargs.get('pk', '')})

    fields = ['title']


# Because you shouldn't be able to give yourself extracredit
class ExtraCreditForm(forms.ModelForm):
    class Meta:
        model = ExtraCredit
        exclude = ['id', 'sender', 'date_credited']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExtraCreditForm, self).__init__(*args, **kwargs)

        self.fields['recipient'].queryset = self.fields['recipient'].queryset.exclude(user_id=user.id)
        self.fields['description'].help_text = "Why does this user deserve extra credit?"


class ExtraCreditCreateView(CreateView):
    template_name = 'extracredit_create.html'
    form_class = ExtraCreditForm

    def get_form_kwargs(self):
        kwargs = super(ExtraCreditCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('my_developer_details')

    def form_valid(self, form):
        form.save(commit=False)
        sender = get_object_or_404(Developer, user_id=self.request.user.id)
        extra_credit_tokens = Developer.objects.get(user_id=sender.user_id).extra_credit_tokens

        if extra_credit_tokens:
            Developer.objects.filter(user_id=sender.user_id).update(extra_credit_tokens=extra_credit_tokens-1)

            form.instance.sender = sender
            form.save()

            return super(ExtraCreditCreateView, self).form_valid(form)
        else:
            raise forms.ValidationError("The user does not have enough tokens")
