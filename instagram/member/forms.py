from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    # clean_<field_name>
    def clean_username(self):
        data = self.cleaned_data['username']
        # 유저가 존재하면 faorms.ValidationError를 발생
        # 아니면 data를 리턴
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already exists!')
        return data
