from django import forms
from .models import LearningTool, Review, Tag
from django.contrib.auth.models import User


class ToolForm(forms.ModelForm):
    # what the user actually sees and fills out
    name = forms.CharField(max_length=128, help_text="what is the tool called")
    link = forms.URLField(max_length=200, help_text="paste the website link here")
    description = forms.CharField(widget=forms.Textarea, help_text="tell us about it")
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all())
    
    # hidden stuff we handle in the background
    score = forms.FloatField(widget=forms.HiddenInput(), initial=0.0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = LearningTool
        fields = ('name', 'description', 'link', 'tags')

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(required=True)
    review_content = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = Review
        exclude = ('user', 'tool')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

#class ReviewForm(forms.ModelForm):
#    rating = forms.IntegerField
