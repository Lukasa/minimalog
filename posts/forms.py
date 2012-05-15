from django import forms

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=100)
