from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

from .forms import SignupForm, LoginForm

User = get_user_model()  # helper 함수


def login(request):
    # POST 요청 (Form submit)의 경우
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # LoginForm 내부에서 setattr로 동적인 속성(login)만듬
            form.login(request)
            return redirect('post_list')
        else:
            return HttpResponse('Login credentials invalid')
    else:
        return render(request, 'member/login.html')


def signup(request):
    if request.method == 'POST':
        # 데이터가 binding 된 SignupForm 인스턴스를 생성
        form = SignupForm(request.POST)
        # 해당 form 이 자신의 필드에 유효한 데이터를 가지고 있는지 유효성 검사
        if form.is_valid():
            # 통과한 경우 정제된 데이터 (cleaned_data)에서 username 과 password 항목을 가져옴
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # username, password 가 주어졌고 중복되는 User 가 없다면 User 생성
            user = User.objects.create_user(
                username=username,
                password=password,
            )

            return HttpResponse(f'{user.username }, { user.password }')

    # GET 요청시 SignupForm 인스턴스를 signup_form 변수에 할당, context 에 같은 키/값으로 전달
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'member/signup.html', context)
