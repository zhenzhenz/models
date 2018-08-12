from django.shortcuts import render
from django.shortcuts import render_to_response
from search.forms import InputForm,ScoreForm

#from software.compound_path import main

def search(request):
    form=InputForm()
    form1=ScoreForm()
    return render_to_response('search_form.html',{'form':form,'form1':form1})