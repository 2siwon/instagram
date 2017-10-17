from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password = forms.PasswordInput()