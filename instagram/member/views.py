from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model, authenticate, login as django_login

from .forms import SignupForm

User = get_user_model()  # helper 함수


def login(request):
    # POST 요청 (Form submit)의 경우
    if request.method == 'POST':
        # 요청에서 username, password를 가져옴
        username = request.POST['username']
        password = request.POST['password']
        # 해당하는 User 객체가 있는지 인증
        user = authenticate(
            username=username,
            password=password,
        )
        # 인증에 성공하면 user변수에 User객체가 할당 실패시 None
        if user is not None:
            # Django의 Session에 해당 User정보를 추가
            # Response에는 SessionKey값을 Set-Cookie 헤더에 담아 보냄
            # 이후 브라우저와의 요청응답에서는 로그인을 유지함
            django_login(request, user)
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
