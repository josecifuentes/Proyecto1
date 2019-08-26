from django import forms
from .models import Order,Type,Service,Job,Profile,Assign

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('Names', 'Last_names', 'Phone', 'Address', 'Reference', 'Description', 'Note')
        widgets = {
            'Names': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Put put names here'}),
            'Last_names': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put last names here'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put phone here'}),
            'Address': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put the Address'}),
            'Reference': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Write a Reference of the Address'}),
            'Description': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Describe the order'}),
            'Note': forms.TextInput(attrs={'class': 'form-control','placeholder': 'write a note'}),   
        }    

class TypeForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = ('Name', 'Descripcion')
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Put put name here'}),
            'Descripcion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put Descripcion here'}),
              
        }  
          
class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ('Description', 'Note')
        widgets = {
            'Description': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Describe the Service'}),
            'Note': forms.TextInput(attrs={'class': 'form-control','placeholder': 'write a note'}),
           
        }       