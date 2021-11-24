from django import forms
from .models import NewUser, Profile
from food.models import Restaurant, Adress



class RegistrationForm(forms.Form):
    user_name = forms.CharField(label='Enter username', help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Email is required'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = NewUser.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError('User with this username already exists')
        return user_name

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if NewUser.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists')
        return email


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'})




class UserLoginForm(forms.Form):
    user_name = forms.CharField(label='Enter username', help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Email is required'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})



class RestaurantRegisterForm(forms.ModelForm):
    city = forms.ChoiceField(choices=Adress.CITIES, initial='Tashkent')
    district = forms.CharField(max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)
    class Meta:
        model = Restaurant
        fields = ('name', 'email', 'password', 'password2', 'open_at',  'close_at', 'day_off', 'contact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Name'})
        self.fields['open_at'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Open at'})
        self.fields['close_at'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Close at'})
        self.fields['day_off'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Day off'})
        self.fields['contact'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Phone number'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'City'})
        self.fields['district'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'District'})


    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['user_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

