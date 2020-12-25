from django import forms
from .models import  *
class product_categoryForm(forms.ModelForm):
    class Meta:
        model = product_category
        fields = ['category_name', 'image']

class product_detailsForm(forms.ModelForm):
    class Meta:
        model=Product_details
        fields=['product_name','category_name','product_img1','product_img2','product_description','product_price','product_expirydate','product_manufecturingdate','quantity']
