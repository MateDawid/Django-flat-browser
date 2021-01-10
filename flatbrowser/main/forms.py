from django import forms

class SearchForm(forms.Form):
    city = forms.CharField(label='City')
    min_price = forms.CharField(label='Minimum price', required=False)
    max_price = forms.CharField(label='Maximum price', required=False)
    min_area = forms.CharField(label='Minimum area', required=False)
    max_area = forms.CharField(label='Maximum area', required=False)
    days_from_publication = forms.CharField(label='Days available', required=False)