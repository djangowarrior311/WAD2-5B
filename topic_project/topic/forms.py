from django import forms
from django.contrib.auth.models import User
from topic_project.topic.models import Review




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

#class ReviewForm(forms.ModelForm):
#    rating = forms.IntegerField