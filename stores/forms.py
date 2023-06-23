from django import forms
from . models import Order
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['cart','discount','subtotal','amount','order_status','ref','payment_complete']
        widgets = {
            'order_by':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'payment_method': forms.Select(attrs={'class':'form-control'})
        }


