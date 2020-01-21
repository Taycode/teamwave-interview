from django import forms
from .choices import sort_choice, order_choice


class StackAPIConsumerForm(forms.Form):
    page = forms.IntegerField(required=False)
    todate = forms.DateField(required=False)
    max = forms.DateField(required=False)
    nottagged = forms.CharField(required=False)
    pagesize = forms.IntegerField(required=False)
    order = forms.ChoiceField(choices=order_choice)
    sort = forms.ChoiceField(choices=sort_choice)
    intitle = forms.CharField(required=False)
    fromdate = forms.DateField(required=False)
    min = forms.DateField(required=False)
    tagged = forms.CharField(required=False)



