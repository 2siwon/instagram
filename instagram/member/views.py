from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth import get_user_model

User = get_user_model()  # helper 함수


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password,
            )

            return HttpResponse(f'{user.username }, { user.password }')

    else:
        return render(request, 'member/signup.html')
