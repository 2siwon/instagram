from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authemticate실행
    성공시 login(request)메서드를 사용할 수 있음
    """

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
                'class': 'form-control',
            }
        ),
    )

    # LoginForm 객체가 생기는 순간 self.user=None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    # 모든 필드에 대한 검증이 끝난 후 실행된다.
    # 그 때 이미 검증이 끝난데서 데이터를 가져다 쓰는게 확실하다.
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        # 해당하는 User가 있는지 인증
        # 인증에 성공하면 self.user변수에 User객체가 할당, 실패시 None
        self.user = authenticate(
            username=username,
            password=password
        )

        if not self.user:
            raise forms.ValidationError(
                'Invalid login credentials!'
            )
        # is_valid()를 통과해서 self.user가 있는 경우에만 로그인 메서드 생성
        else:
            # login이란 이름으로 함수를 호출하고 싶을 때(동적으로 어떤 오브젝트의 속성을 넣고싶을 때)
            setattr(self, 'login', self._login)

    def _login(self, request):
        """
        django.contrib.auth.login(request)를 실행

        :param request: django.contrib.auth.login()에 주어질 HttpRequest객체
        :return:
        """
        django_login(request, self.user)


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
