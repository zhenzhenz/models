from django.shortcuts import render
from django.shortcuts import render_to_response
from search.forms import search_form
#from software.compound_path import main

def search(request):
    form=search_form()
    return render_to_response('search_form.html',{'form':form})

def main(request):
    return render_to_response('main.html')