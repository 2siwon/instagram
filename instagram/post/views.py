from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from post.forms import PostForm, CommentForm
from .models import Post, PostComment


def post_list(request):
    posts = Post.objects.exclude(author__isnull=True)
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
    }

    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post = Post.objects.get(pk=post_pk)

    # Post 에서 pk값을 찾고 없으면 404 error
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
    }

    return render(request, 'post/post_detail.html', context)


def post_create(request):
    # 로그인한 유저만 접근 및 POST요청 가능
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        # POST요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # 만약 form이 유효성검사를 통과헀다면 true리턴
        if form.is_valid():
            # 유효할 경우 Post인스턴스를 생성 및 저장
            post = Post.objects.create(
                author=request.user,
                photo=form.cleaned_data['photo'],
            )
            return redirect('post:post_list')

    else:
        # GET 요청의 경우 빈 PostForm인스턴스를 생성해서 템플릿에 전달
        form = PostForm()

    # GET 요청에선 이 부분이 무조건 실행
    # POST 요청에선 form.is_valid()를 통과하지 못하면 이 부분이 실행
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def comment_create(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')
    # URL get parameter로 온 'post_pk'에 해당하는
    # Post instacne를 'post'변수에 할당
    # 찾지못하면 404Error를 브라우저에 리턴
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # 데이터가 바인딩된 CommentForm인스턴스를 form에 할당
        form = CommentForm(request.POST)
        # 유효성 검증
        if form.is_valid():
            # 통과한 경우, Post에 해당하는 Comment 인스턴스 생성
            PostComment.objects.create(
                author=request.user,
                post=post,
                content=form.cleaned_data['content']
            )

            # post_list에서 오는 요청 처리
            next = request.GET.get('next')
            print(next)

            if next:
                return redirect(next)
            # 생성 후 Post의 detail화면으로 이동
            return redirect('post:post_detail', post_pk=post_pk)


def post_delete(request, author_pk, post_pk):
    if request.user.is_authenticated:
        post = Post.objects.filter(author_id=author_pk).get(pk=post_pk)
        post.delete()
    return redirect('post:post_list')


def comment_delete(request, author_pk, comment_pk):
    if request.user.is_authenticated:
        comment = PostComment.objects.filter(author_id=author_pk).get(pk=comment_pk)
        comment.delete()
    return redirect('post:post_list')
