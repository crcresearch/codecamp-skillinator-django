from django.views.generic import *
from skillsmatrix.models import *

#View file for the homepage
class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()

        context['developer_count'] = Developer.objects.count()
        context['developerskills_count'] = DeveloperSkill.objects.count()
        context['extracredit_count'] = ExtraCredit.objects.count()

        return context
