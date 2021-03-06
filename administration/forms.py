from django import forms
from .models import Order,Type,Service,Profile,Assign

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

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('Names', 'Last_names', 'IdPersonal', 'Phone', 'Address', 'Start_Work','Note')
        widgets = {
            'Names': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Put the name'}),
            'Last_names': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put last names here'}),
            'IdPersonal': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Put the id'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put phone here'}),
            'Address': forms.TextInput(attrs={'class': 'form-control','placeholder': 'put the Address'}),
            'Start_Work': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Put the date of start work','required':'readonly'}),
            'Note': forms.TextInput(attrs={'class': 'form-control','placeholder': 'write a note'}),
           
        } 