from django.shortcuts import redirect, render
from platformdirs import user_log_dir
from . models import Account, Trans
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# Create your views here.
# 1. 메인페이지
def index(request):
    return render(request, 'index.html')

# 2. 프로필
# def user_profile(request):
#     return render(request, 'user_profile.html')

# 3. 로그인
def login(request):
    if request.method == 'POST':
        user_name = request.POST['userID']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'error': 'user_name or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')

# 4. 회원가입    
def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['userID'],
                password=request.POST['password1'],
                first_name=request.POST['username'],
            )
            auth.login(request, user)
            return redirect('/login')
        return render(request, 'register.html')
    return render(request, 'register.html')

# 5. FAQ
def faq(request):
    return render(request, 'faq.html')

# 6. Contact   
def contact(request):
    return render(request, 'contact.html')

# 7. 차트 페이지
def charts(request):
    return render(request, 'charts.html')    

# 8. 계좌 전체 페이지
def total_accounts(request):
    return render(request, 'total_accounts.html') 

# 9. 계좌 페이지
def accounts(request):
    return render(request, 'accounts.html')    

# 10. 공모주 알림 페이지
def alarms(request):
    return render(request, 'alarms.html') 

# 11. 카드 목록 페이지
def cards(request):
    return render(request, 'cards.html') 

# 12. 계좌 이체 페이지
def transfer(request):
    return render(request, 'transfer.html')

# 13. 지점찾기 페이지
def find_kb(request):
    return render(request, 'find_kb.html')

# 14. 카드 추천 페이지
def cards_recom(request):
    return render(request, 'cards_recom.html')

# 15. 주식 잔고 페이지
def stock(request):
    return render(request, 'stock.html')

# 16. 주식 예측 게임 페이지
def stock_game(request):
    return render(request, 'stock_game.html')

# 17. 나의 자산현황 페이지
def myAsset(request):
    return render(request, 'myAsset.html')

# 18. 나의 Gold 확인하기 페이지
def myGold(request):
    return render(request, 'myGold.html')

# 19. 주식 전체 차트 페이지
def stock_charts(request):
    return render(request, 'stock_charts.html')

# 20. 출석체크 페이지
def attendance(request):
    return render(request, 'attendance.html')

def stock_account(request):
    return render(request, 'stock_account.html')