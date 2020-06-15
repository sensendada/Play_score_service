from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from Play_score_service.Play_score_service.apps.query.models import Score, Rank


"""
实现用户登录
"""
class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = Score.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)

    @csrf_exempt
    def login(self, request):
        if request.method == 'GET':
            return render(request, 'front_end_pc/login.html')
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('upload/')
            else:
                return render(request, 'front_end_pc/login.html')


class Upload(APIView):
    def upload(self, request):
        if request.method == 'GET':
            return render(request, 'front_end_pc/upload.html', {'user': request.user, })
        if request.method == 'POST':
            score = request.POST.get('score', '')
            if score:
                old_scor = Score.objects.filter(client=request.user).first()
                if old_scor:
                    if old_scor.score != score:
                        old_scor.score = score
                        old_scor.save()
                else:
                    Score.objects.create(client=request.user, score=score)
                # 排名表数据更新
                Rank.objects.all().delete()
                score_li = [score_obj.id for score_obj in Score.objects.all().order_by('-score')]
                n = 1
                for i in score_li:
                    Rank.objects.create(c_id_id=i, rank=n)
                    n = n + 1
                return JsonResponse({'status': 'sucess'})
            return JsonResponse({'status': 'error'})


class Show(APIView):
    def show(self, request):
        context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                              Score.objects.all().order_by('-score')]}
        if request.method == 'GET':
            count = Score.objects.all().count()
            uscore = Score.objects.filter(client=request.user).first()
            uscore = {'ranking': uscore.rank.rank, 'score': uscore.score}
            return render(request, 'demo1/show.html', {'context': context, 'count': count, 'uscore': uscore})
        if request.method == 'POST':
            try:
                start = int(request.POST.get('start'))
                end = int(request.POST.get('end'))
            except ValueError as e1:
                return JsonResponse({'status': 'error'})
            context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                                  Score.objects.all().order_by('-score')[start - 1:end]]}
            return JsonResponse({'status': 'ok', 'context': context})

