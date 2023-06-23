from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(label=('Password'),widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=('Confirm Password'),widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['fullname','username','email','password1','password2','phone','address','profile_pix']
        # exclude = ['user']
        widgets = {
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'profile_pix': forms.FileInput(attrs={'class':'form-control'})
        }

class UpdateProfileForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email= forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['fullname','username','email','phone','address','profile_pix']
        # exclude = ['user']
        widgets = {
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'profile_pix': forms.FileInput(attrs={'class':'form-control'})
        }