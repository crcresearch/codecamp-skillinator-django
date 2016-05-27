from django.views.generic import TemplateView
from skillsmatrix.models import Developer, DeveloperSkill, ExtraCredit


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()

        context['developer_count'] = Developer.objects.count()
        context['developer_skills_count'] = DeveloperSkill.objects.count()
        context['extra_credit_count'] = ExtraCredit.objects.count()

        return context
