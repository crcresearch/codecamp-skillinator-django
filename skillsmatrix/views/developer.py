from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from skillsmatrix.models import Developer, DeveloperSkill, ExtraCredit


class DeveloperList(ListView):
    """
    DeveloperList - a ListView that lists all of the developers by using the developer_list.html template
    """
    model = Developer
    template_name = 'developer_list.html'


class DeveloperListByManager(DeveloperList):
    """
    DeveloperListByManager - a ListView that inherits from DeveloperList but uses a url parameter to only show the list
    of developers that have the manager passed in on the url
    (Hint: use the skillsmatrix/urls.py file to gain some clues!)
    """
    model = Developer
    template_name = 'developer_list.html'

    def get_queryset(self):
        query_set = super(DeveloperListByManager, self).get_queryset()

        return query_set.filter(manager=self.kwargs['manager'])


class DeveloperDetail(DetailView):
    """
    DeveloperDetail - a DetailView of a single developer, determined by id passed in the urls.py file. This view uses
    the developer_detail.html template and must load an extra list into the context to get the page to display
    correctly. (Hint: Look at the template file itself to see what the context variable should be called).
    This extra list should be sorted in descending order by years of experience.
    """
    model = Developer
    template_name = 'developer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DeveloperDetail, self).get_context_data()
        context['skills'] = DeveloperSkill.objects.filter(developer=kwargs['object'].id)\
            .order_by('-years_of_experience')

        return context


class DeveloperDetailMe(DeveloperDetail):
    """
    DeveloperDetailMe - a DetailView that inherits from DeveloperDetail, but instead of getting a pk from the URL,
    always show the detail page of the currently logged in user/developer.
    """

    def get_object(self, queryset=None):
        return Developer.objects.get(user=self.request.user.id)


class DeveloperUpdate(UpdateView):
    """
    DeveloperUpdate - an UpdateView that uses the developer_update.html template to update a developer's title.
    After completing the update, this view should redirect back to the developer detail page of the user that was just
    edited.
    """
    template_name = 'developer_update.html'
    model = Developer
    fields = ['title']

    def get_success_url(self):
        return reverse('developer_detail', kwargs={'pk': self.object.id})


class ExtraCreditCreateView(CreateView):
    """
    ExtraCreditCreateView - a CreateView that allows the logged in user to send extra credit to another developer.
    The form does not ask for the sender because it should always be based on the developer of the logged in user.
    After successfully creating the extra credit object, this view should return the user back to their own developer
    detail page.
    (Extra Credit: Make this view also decrement the extra credit tokens if the extra credit form is valid, and not
    allowing the user to give extra credit if they don't have any tokens)
    """
    template_name = 'extra_credit_create.html'
    model = ExtraCredit
    fields = ['recipient', 'skill', 'description', ]

    def get_success_url(self):
        return reverse('developer_detail', kwargs={'pk': Developer.objects.get(user=self.request.user).id})

    def form_valid(self, form):
        developer = Developer.objects.get(user=self.request.user)
        form.instance.sender = developer
        developer.extra_credit_tokens -= 1
        developer.save()

        return super(ExtraCreditCreateView, self).form_valid(form)
