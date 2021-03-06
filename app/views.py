from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader

from .models import Email, User
import datetime

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def search(request):
    if request.method == 'POST':
        print(request.POST)

    if "sender" in request.POST:
        emails = Email.objects.filter(senderId=request.POST["sender"])
    elif "recipient" in request.POST:
        emails = Email.objects.filter(
                    recipientIds__contains=request.POST["recipient"]
                 )
    elif "fromDate" in request.POST and "toDate" in request.POST:
        fromDate = request.POST["fromDate"]
        toDate = request.POST["toDate"]

        fromDate = datetime.datetime.strptime(fromDate, '%d/%m/%Y').date()
        toDate = datetime.datetime.strptime(toDate, '%d/%m/%Y').date()
        print(fromDate)
        print(toDate)

        emails = Email.objects.filter(
                timeSent__range=[fromDate, toDate]
        )

    context = {
            'emails': emails,
    }

    return render(request, 'app/search.html', context)

def detail(request, email_id):
    email = Email.objects.get(pk=email_id)
    print(email.senderId)

    context = {
            'email': email,
    }

    try:
        sender = User.objects.get(pk=email.senderId)
        context["sender"] = sender
    except User.DoesNotExist:
        pass

    return render(request, 'app/detail.html', context)
