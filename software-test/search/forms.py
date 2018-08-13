# -*- coding: utf-8 -*-


from django import forms

class InputForm(forms.Form):
    Microorganism = forms.CharField(initial='ECO')   
    Input = forms.CharField(required=False)
    Output = forms.CharField(required=False)
    MaxLength = forms.IntegerField()
    result_conservation = forms.IntegerField(initial=50)
    
class ScoreForm(forms.Form):
    Gibbs=forms.FloatField(initial=0.5)
    Toxicity=forms.FloatField(initial=0.5)
    conservation=forms.IntegerField(initial=1)
    requrired = forms.CharField(required=False)
    not_requrired = forms.CharField(required=False)