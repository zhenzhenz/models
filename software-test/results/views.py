from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

from results.compound_path import main
from search.forms import search_form
import json


def results(request):
    if request.method=='GET':
        form =search_form(request.GET)
        
        if form.is_valid():
            data=form.cleaned_data    
            #result=main(data,data1)
            #return render_to_response('results.html',{'result':result})
            return render_to_response('results.html',{'data':mark_safe(data)})
    else:
        return render_to_response('main.html')
    
@csrf_exempt    
def ajax_test(request):
    if request.method=='POST':
        data=json.dumps(request.POST)
        mydict=json.loads(data)
        result=main(mydict)
        
        output=''
        for item in result:
            path=''
            for row in item:
                path+=str(row)+'$$'
            output+=path[:-2]+'&&'
        output=output[:-2]
        return HttpResponse(output)