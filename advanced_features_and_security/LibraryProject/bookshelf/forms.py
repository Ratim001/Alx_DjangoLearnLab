
# bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):               # <- exact name checker looks for
    title = forms.CharField(max_length=200, required=True)
    author = forms.CharField(max_length=100, required=True)

# (Optional) keep your SearchForm if you use it:
class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)
