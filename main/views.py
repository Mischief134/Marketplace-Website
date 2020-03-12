from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404,render
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.views import generic

# class IndeView(generic.DetailView):
#     template_name = 'index.html'
#     # context_object_name = 'value'


def index(request):
    context = {'val': "HAw you are pidor"}
    return render(request, 'main/index.html', context)
