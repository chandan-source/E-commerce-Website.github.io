from django import forms
from .models import *
class OrderForm(forms.ModelForm):
    class Meta:
        model=order_product
        exclude=['order_id','payment_id','payment_status','amount','usr',"order_date"]
        widgets={
                "fullname":forms.TextInput(attrs={"placeholder":"fullname","class":"form-control"}),
                "house_no":forms.TextInput(attrs={"placeholder":"house-no","class":"form-control"}),
                "area_name":forms.TextInput(attrs={"placeholder":"area-name","class":"form-control"}),
                "city_state":forms.TextInput(attrs={"placeholder":"city/state","class":"form-control"}),
                "landmark":forms.TextInput(attrs={"placeholder":"landmark","class":"form-control"}),
                "pincode":forms.TextInput(attrs={"placeholder":"pincode","class":"form-control"}),
                "mobile1":forms.TextInput(attrs={"placeholder":"mobile no","class":"form-control"}),
                "mobile2":forms.TextInput(attrs={"placeholder":"alternative mobile no.","class":"form-control"})
        }
class add_product_form(forms.ModelForm):
    class Meta:
        model=product
        fields='__all__'

        widgets={
                "subcat":forms.Select(attrs={"class":"form-control"}),
                "name":forms.TextInput(attrs={"placeholder":"product-name","class":"form-control"}),
                "price":forms.NumberInput(attrs={"placeholder":"product-price","class":"form-control"}),
                "stock":forms.NumberInput(attrs={"placeholder":"product_stock","class":"form-control"}),
                "img1":forms.FileInput(attrs={"class":"form-control"}),
                "img2":forms.FileInput(attrs={"class":"form-control"}),
                "img3":forms.FileInput(attrs={"class":"form-control"}),
                "des":forms.Textarea(attrs={"placeholder":"product_description.","class":"form-control"}),
                "size": forms.TextInput(attrs={"placeholder": "size(if required)", "class": "form-control"}),
        }

class add_category_form(forms.ModelForm):
    class Meta:
        model=category
        fields='__all__'

        widgets={
                "name":forms.TextInput(attrs={"class":"form-control"}),

        }


class add_subcategory_form(forms.ModelForm):
    class Meta:
        model = subcategory
        fields = '__all__'

        widgets = {
            "cat": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),

        }