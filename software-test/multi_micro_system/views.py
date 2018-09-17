from django.shortcuts import render_to_response
from multi_micro_system.forms import InputForm
from multi_micro_system.get_dynamic_graphy import main

#from software.compound_path import main

def multi_system(request):
    form=InputForm()
    #form1=ScoreForm()
    return render_to_response('multi_micro_system.html',{'form':form})

def multi_sysytem_results(request):
    if request.method=='GET':
        form =InputForm(request.GET)
        
        if form.is_valid():
            data=form.cleaned_data
            result=main(data)
            return render_to_response('multi_results.html',{'result':result})
    else:
        return render_to_response('main.html')