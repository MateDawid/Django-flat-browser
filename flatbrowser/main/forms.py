from django import forms

class SearchForm(forms.Form):
    city = forms.CharField(label='Miasto')
    min_price = forms.CharField(label='Minimalna cena', required=False)
    max_price = forms.CharField(label='Maksymalna cena', required=False)
    min_area = forms.CharField(label='Minimalna powierzchnia', required=False)
    max_area = forms.CharField(label='Maksymalna powierzchnia', required=False)
    days_from_publication = forms.CharField(label='Dni od dodania', required=False)

    def clean_min_price(self):
        min_price = self.cleaned_data['min_price']
        if min_price.isnumeric() or min_price == "":
            return min_price
        else:
            raise forms.ValidationError("Spróbuj wpisać liczbę!")
        

    def clean_max_price(self):
        max_price = self.cleaned_data['max_price']
        if max_price.isnumeric() or max_price == "":
            return max_price
        else:
            raise forms.ValidationError("Spróbuj wpisać liczbę!")

    def clean_min_area(self):
        min_area = self.cleaned_data['min_area']
        if min_area.isnumeric() or min_area == "":
            return min_area
        else:
            raise forms.ValidationError("Spróbuj wpisać liczbę!")

    def clean_max_area(self):
        max_area = self.cleaned_data['max_area']
        if max_area.isnumeric() or max_area == "":
            return max_area
        else:
            raise forms.ValidationError("Spróbuj wpisać liczbę!")

    def clean_days_from_publication(self):
        days_from_publication = self.cleaned_data['days_from_publication']
        if days_from_publication.isnumeric() or days_from_publication == "":
            return days_from_publication
        else:
            raise forms.ValidationError("Spróbuj wpisać liczbę!")

# class SignUp(forms.Form):
#     first_name = forms.CharField(initial = "First name")
#     last_name = forms.CharField(initial = "Last name")
#     email = forms.EmailField(help_text = "E-mail")
#     password = forms.CharField(widget = forms.PasswordInput, validators=[check_password_size])
#     re_password = forms.CharField(help_text = 'Repeat password', widget = forms.PasswordInput)

#     def clean_age(self):
#         age = self.cleaned_data['age']
#         if age < 18:
#             raise forms.ValidationError("You're not old enough!")
#         return age
    
#     def clean_first_name(self):
#         first_name = self.cleaned_data["first_name"]
#         if first_name[0].islower():
#             raise forms.ValidationError("You should use big char!")
#         return first_name
    
#     def clean_last_name(self):
#         last_name = self.cleaned_data["last_name"]
#         if last_name[0].islower():
#             raise forms.ValidationError("You should use big char!")
#         return last_name

#     def clean_re_password(self):
#         password = self.cleaned_data["password"]
#         re_password = self.cleaned_data["re_password"]
#         if password != re_password:
#            raise forms.ValidationError("Passwords are not the same!")
#         pass