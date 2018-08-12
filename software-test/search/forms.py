# -*- coding: utf-8 -*-


from django import forms

class InputForm(forms.Form):
    Microorganism = forms.CharField()   
    Input = forms.CharField(required=False)
    Output = forms.CharField(required=False)
    MaxLength = forms.IntegerField()
    
class ScoreForm(forms.Form):
    Gibbs=forms.IntegerField()
    Internal_or_external=forms.IntegerField()
    posion=forms.IntegerField()
    conservation=forms.IntegerField()