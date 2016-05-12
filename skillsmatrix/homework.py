from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
from skillsmatrix.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def ProblemOne(request):
    if request.method == 'POST':
        # then they're trying to give us some information!
        if 'name' in request.POST:
            return HttpResponse(json.dumps({'name': request.POST['name']}))
        else:
            return HttpResponse(json.dumps({'name': None}))

    # otherwise, they're wanting some information back
    developers = Developer.objects.filter(Q(user__last_name__contains=request.GET['name']) | Q(user__first_name__contains=request.GET['name']))

    # run through and create a custom dictionary
    dev_list = []
    for dev in developers:
        location = 'CRC'
        if dev.user.username == 'neo':
            location = 'The Matrix'
        dev_list.append({
            'first_name': dev.user.first_name,
            'last_name': dev.user.last_name,
            'location': location
        })

    return HttpResponse(json.dumps(dev_list))


@login_required
def ProblemTwo(request):
    if request.user.username == 'neo' and 'MSIE' in request.META['HTTP_USER_AGENT']:
        return HttpResponse("Neo wouldn't use Internet Explorer silly...")

    if request.user.username == 'neo' and 'MSIE' not in request.META['HTTP_USER_AGENT']:
        return HttpResponseRedirect('http://vignette2.wikia.nocookie.net/matrix/images/d/df/Thematrixincode99.jpg/revision/latest?cb=20140425045724')

    if request.user.username != 'neo':
        return HttpResponse('Operator...')


@login_required
def ProblemThree(request):
    return render(request, 'problemthree.html', {})