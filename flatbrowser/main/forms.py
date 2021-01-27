from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Podaj nazwę użytkownika', min_length=3, max_length=150)
    email = forms.EmailField(label='Podaj e-mail')
    password1 = forms.CharField(label='Podaj hasło',min_length=8, max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło',min_length=8, max_length=30, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        username_search = User.objects.filter(username=username)
        if username_search.count():
            raise  ValidationError("Taka nazwa już została użyta!")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        email_search = User.objects.filter(email=email)
        if email_search.count():
            raise  ValidationError("Taki email już został użyty!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Podane hasła nie są takie same!")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika",min_length=3, max_length=150)
    password = forms.CharField(label="Hasło",widget=forms.PasswordInput())
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            return username
        except ObjectDoesNotExist:
            raise forms.ValidationError("Niepoprawna nazwa użytkownika!")        
    def clean_password(self):
        if self.cleaned_data.has_key('username'):
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                return password
            raise forms.ValidationError("Niepoprawne hasło!")                
        raise forms.ValidationError("Niepoprawna nazwa użytkownika!")