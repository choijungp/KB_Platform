from django.shortcuts import render

# Create your views here.
# 1. 메인페이지
def index(request):
    return render(request, 'index.html')

# 2. 프로필
def user_profile(request):
    return render(request, 'user_profile.html')

# 3. 로그인
def login(request):
    return render(request, 'login.html')

# 4. 회원가입    
def register(request):
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