from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect

from results.compound_path import main
from search.forms import InputForm,ScoreForm

def results(request):
    if request.method=='GET':
        form =InputForm(request.GET)
        form1 =ScoreForm(request.GET)
        if form.is_valid() and form1.is_valid():
            data=form.cleaned_data
            data1=form1.cleaned_data
            result=main(data,data1)
            return render_to_response('results.html',{'result':result})
    else:
        return render_to_response('main.html')