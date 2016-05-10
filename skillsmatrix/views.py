from django.shortcuts import render, HttpResponse
import json
from skillsmatrix.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def SearchDeveloperSkill(request):
    if 'skill' not in request.GET:
        return HttpResponse(json.dumps({'ERROR': 'No skillset listed!'}))

    skill_keyword = request.GET['skill']
    skills = DeveloperSkill.objects.filter(skill__name__contains=skill_keyword).values('developer__user__username',
                                                                                       "developer__user__first_name",
                                                                                       "developer__user__last_name")\
        .order_by('developer__user__username')

    if len(skills) <= 0:
        return HttpResponse(json.dumps([]))

    return HttpResponse(json.dumps(list(skills)))

@login_required
def MySkills(request):
    dev_skills = DeveloperSkill.objects.filter(developer__user=request.user)
    skill_list = []
    for skill in dev_skills:
        skill_list.append(skill.skill.name)

    return HttpResponse(json.dumps(skill_list))


@login_required
def HomePage(request):
    if 'MSIE' in request.META['HTTP_USER_AGENT']:
        return HttpResponse('IE not supported')
    else:
        return render(request, 'home.html', {})