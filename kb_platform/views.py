from django.shortcuts import get_object_or_404, redirect, render
from platformdirs import user_log_dir
from . models import Card, Benefit, Account, Trans
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q

# 1. 메인페이지
def index(request):
    return render(request, 'index.html')

# 2. 로그인
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

# 3. 로그아웃
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

# 5. 차트 페이지
def charts(request):
    all_accounts = Account.objects.filter(user=request.user)  # 해당 user에 해당하는 계좌 list
    all_accounts = all_accounts.filter(acc_type=0)   # 해당 user의 은행 계좌만 (증권, 금 제외)

    types = [0, 0, 0, 0, 0, 0]
    # 은행 계좌 for문
    for i in range(len(all_accounts)):
        all_trans = Trans.objects.filter(account_id=all_accounts[i].acc_num)
        for trans in all_trans:
            if trans.trans_date.year==2022 and trans.trans_date.month==5:
                # 출금일 때만 type 체크
                if trans.trans_price < 0 :
                    # 소비 type이 0인 경우 :: 식비
                    if trans.trans_type == '0':
                        types[0] += trans.trans_price
                    # 소비 type이 1인 경우 :: 이동통신
                    elif trans.trans_type == '1':
                        types[1] += trans.trans_price
                    # 소비 type이 2인 경우 :: 쇼핑
                    elif trans.trans_type == '2':
                        types[2] += trans.trans_price
                    # 소비 type이 3인 경우 :: 문화생활
                    elif trans.trans_type == '3':
                        types[3] += trans.trans_price
                    # 소비 type이 4인 경우 :: 의료
                    elif trans.trans_type == '4':
                        types[4] += trans.trans_price
                    # 소비 type이 5인 경우 :: 교통비
                    elif trans.trans_type == '5':
                        types[5] += trans.trans_price

    for i in range(len(types)):
        types[i] *= -1

    months = [0, 0, 0, 0, 0, 0]
    for i in range(len(all_accounts)):
        all_trans = Trans.objects.filter(account_id=all_accounts[i].acc_num)
        for trans in all_trans:
            if trans.trans_date.year==2022:
                # 출금일 때만 type 체크
                if trans.trans_price < 0 :
                    # 1월달 소비
                    if trans.trans_date.month==1:
                        months[0] += trans.trans_price
                    # 2월달 소비
                    elif trans.trans_date.month==2:
                        months[1] += trans.trans_price
                    # 3월달 소비
                    elif trans.trans_date.month==3:
                        months[2] += trans.trans_price
                    # 4월달 소비
                    elif trans.trans_date.month==4:
                        months[3] += trans.trans_price
                    # 5월달 소비
                    elif trans.trans_date.month==5:
                        months[4] += trans.trans_price
    for i in range(len(months)):
        months[i] *= -1
        months[i] //= 10000  # 만원 단위를 위해 10000으로 나눠줌


    days = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(all_accounts)):
        all_trans = Trans.objects.filter(account_id=all_accounts[i].acc_num)
        for trans in all_trans:
            # 이번년도 이번 달 소비 CHECK !
            if trans.trans_date.year==2022 and trans.trans_date.month==5:
                # 출금일 때만 type 체크
                if trans.trans_price < 0 :
                    # 월요일 소비
                    if trans.trans_date.weekday()==1:
                        days[0] += trans.trans_price
                    # 화요일 소비
                    elif trans.trans_date.weekday()==2:
                        days[1] += trans.trans_price
                    # 수요일 소비
                    elif trans.trans_date.weekday()==3:
                        days[2] += trans.trans_price
                    # 목요일 소비
                    elif trans.trans_date.weekday()==4:
                        days[3] += trans.trans_price
                    # 금요일 소비
                    elif trans.trans_date.weekday()==5:
                        days[4] += trans.trans_price
                    # 토요일 소비
                    elif trans.trans_date.weekday()==6:
                        days[5] += trans.trans_price
                    # 일요일 소비
                    elif trans.trans_date.weekday()==0:
                        days[6] += trans.trans_price
    for i in range(len(days)):
        days[i] *= -1
        days[i] //= 10000  # 만원 단위를 위해 10000으로 나눠줌

    context = {
        'months' : months,
        'days' : days,
        'types' : types,
    }

    return render(request, 'charts.html', context)    

# 6. 계좌 전체 페이지
def total_accounts(request):
    # 해당 user에 해당하는 계좌 list
    all_accounts = Account.objects.filter(user=request.user)
    acc_total = sum(all_accounts.values_list('total', flat=True))
    
    account_0 = all_accounts.filter(acc_detail=0)
    account_1 = all_accounts.filter(acc_detail=1)
    account_2 = all_accounts.filter(acc_detail=2)

    ###### 입출금 자유 ######
    total_bank0 = []
    for i in range(len(account_0)):
        tmp = 0
        all_trans = Trans.objects.filter(account_id=account_0[i].acc_num)
        tmp_acc = Account.objects.get(acc_num=account_0[i].acc_num)
        for trans in all_trans:
            tmp += trans.trans_price
        total_bank0.append(tmp)
        tmp_acc.total = tmp
        tmp_acc.save()
        
    
    ###### 예금 / 적금 / 주택청약 ######
    total_bank1 = []
    for i in range(len(account_1)):
        tmp = 0
        all_trans = Trans.objects.filter(account_id=account_1[i].acc_num)
        tmp_acc = Account.objects.get(acc_num=account_1[i].acc_num)
        for trans in all_trans:
            tmp += trans.trans_price
        total_bank1.append(tmp)
        tmp_acc.total = tmp
        tmp_acc.save()

    ###### 골드 ######
    total_bank2 = []
    for i in range(len(account_2)):
        tmp = 0
        all_trans = Trans.objects.filter(account_id=account_2[i].acc_num)
        tmp_acc = Account.objects.get(acc_num=account_2[i].acc_num)
        for trans in all_trans:
            tmp += trans.trans_price
        total_bank2.append(tmp)
        tmp_acc.total = tmp
        tmp_acc.save()

    context = {
        'all_accounts': all_accounts,
        'account_0' : account_0,
        'account_1' : account_1,
        'account_2' : account_2,
        'acc_total': acc_total,
        
        'sum_total0' : sum(total_bank0),
        'sum_total1' : sum(total_bank1),
        'sum_total2' : sum(total_bank2),
    }
    return render(request, 'total_accounts.html', context) 

# 7. 계좌 페이지
def accounts(request, pk):
    account = get_object_or_404(Account, pk=pk)
    all_trans = account.trans.all().order_by('-id')
    tmp_trans = account.trans.all()

    trans_sum = sum(all_trans.values_list('trans_price', flat=True))
    totals = []
    result = 0 
    for trans in tmp_trans:
        result += trans.trans_price
        totals.append(result)
    totals = totals[::-1]
    datas = zip(all_trans, totals)
    context = {
        "account" : account,
        "all_trans" : datas,
        'trans_sum' : trans_sum,
    }

    return render(request, 'accounts.html', context)    

# 8. 카드 목록 페이지
def cards(request):
    check_cards = Card.objects.filter(card_type=0) # 체크카드 목록
    debit_cards = Card.objects.filter(card_type=1) # 신용카드 목록

    benefits = Benefit.objects.all() # 카드 혜택 목록
    context = {
        'check_cards' : check_cards,
        'debit_cards' : debit_cards,
        'benefits' : benefits,
    }
    return render(request, 'cards.html', context) 

# 9. 계좌 이체 페이지
def transfer(request):
    return render(request, 'transfer.html')

# 10. 지점찾기 페이지
def find_kb(request):
    return render(request, 'find_kb.html')

# 11. 카드 추천 페이지
def cards_recom(request):
    ### ========= 카드추천 알고리즘 ========= ###
    cards = [0, 0, 0, 0, 0, 0, 0]

    all_accounts = Account.objects.filter(user=request.user)  # 해당 user에 해당하는 계좌 list
    all_accounts = all_accounts.filter(acc_type=0)   # 해당 user의 은행 계좌만 (증권, 금 제외)

    # for 알고리즘
    cards = [0, 0, 0, 0, 0, 0, 0, 0]
    for j in range(len(cards)):
        # card 0번째 5번째 object 없음
        if j == 0 or j == 5:
            continue
        # 그렇지 않으면 확인 !
        else:
            # 카드에 해당 하는 benefits 뽑아내기 
            benefits = Benefit.objects.filter(card_id=j)
            for i in range(len(all_accounts)):
                all_trans = Trans.objects.filter(account_id=all_accounts[i].acc_num)
                
                for trans in all_trans:
                    # if trans.trans_date.year==2022 and trans.trans_date.month==3:
                    if trans.trans_date.year==2022:
                        # 출금일 때만 type 체크
                        if trans.trans_price < 0 :
                            # benefit 확인
                            for benefit in benefits:
                                # 해당 내용이 컨텐츠 안에 있다면
                                if trans.trans_content.find(benefit.service_name) != -1:
                                    # 할인이 %인것만 
                                    if benefit.percent < 100:
                                        cards[j] += (trans.trans_price * -1) * benefit.percent

    # 1, 3, 4
    check_max = max(cards[1], cards[3], cards[4])
       
    # 2, 6, 7
    debit_max = max(cards[2], cards[6], cards[7])

    for i in range(len(cards)):
        if cards[i] == check_max:
            check_id = i
        elif cards[i] == debit_max:
            debet_id = i

    # for 차트 
    types = [0, 0, 0, 0, 0, 0]
    # 은행 계좌 for문
    for i in range(len(all_accounts)):
        all_trans = Trans.objects.filter(account_id=all_accounts[i].acc_num)
        for trans in all_trans:
            if trans.trans_date.year==2022 and trans.trans_date.month==5:
                # 출금일 때만 type 체크
                if trans.trans_price < 0 :
                    # 소비 type이 0인 경우 :: 식비
                    if trans.trans_type == '0':
                        types[0] += trans.trans_price
                    # 소비 type이 1인 경우 :: 이동통신
                    elif trans.trans_type == '1':
                        types[1] += trans.trans_price
                    # 소비 type이 2인 경우 :: 쇼핑
                    elif trans.trans_type == '2':
                        types[2] += trans.trans_price
                    # 소비 type이 3인 경우 :: 문화생활
                    elif trans.trans_type == '3':
                        types[3] += trans.trans_price
                    # 소비 type이 4인 경우 :: 의료
                    elif trans.trans_type == '4':
                        types[4] += trans.trans_price
                    # 소비 type이 5인 경우 :: 교통비
                    elif trans.trans_type == '5':
                        types[5] += trans.trans_price

    for i in range(len(types)):
        types[i] *= -1

    check_card = Card.objects.get(id=check_id) # 체크카드 PICK
    debit_card = Card.objects.get(id=debet_id) # 신용카드 PICK

    cc_id = check_card.id
    dc_id = debit_card.id 
    cc_benefits = Benefit.objects.filter(card_id = cc_id) # 카드 혜택 목록
    cc3 = cc_benefits[:3]

    dc_benefits = Benefit.objects.filter(card_id = dc_id) # 카드 혜택 목록
    dc3 = dc_benefits[:3]

    context = {
        'check_card' : check_card,
        'debit_card' : debit_card,
        'cc_benefits' : cc_benefits,
        'cc3' : cc3,
        'dc_benefits' : dc_benefits,
        'dc3' : dc3,
        'types' : types,
        'cards' : cards,
    }
    return render(request, 'cards_recom.html', context)

# 15. 주식 잔고 페이지
def stock(request):
    return render(request, 'stock.html')

# 16. 주식 예측 게임 페이지
def stock_game(request):
    return render(request, 'stock_game.html')

# 17. 나의 자산현황 페이지
def myAsset(request):
    all_accounts = Account.objects.filter(user=request.user)  # 해당 user에 해당하는 계좌 list

    all_bank = all_accounts.filter(acc_type=0)  # user의 은행 계좌
    all_stock = all_accounts.filter(acc_type=1) # user의 증권 계좌
    all_gold = all_accounts.filter(acc_type=2)  # user의  금  계좌

    # 은행 계좌 전체 총액
    bank_total = 0
    # 주식 계좌 전체 총액
    stock_total = 0
    # 주식 계좌 중 예수금 금액
    stock_tmp = 0
    # 금 계좌 전체 총액
    gold_total = 0
    # 금 계좌 중 리워드 금액
    goldReward = 0

    # ========================== detail 값 저장 ==========================
    bank_detail0 = 0
    bank_detail1 = 0

    d_bank0 = all_bank.filter(acc_detail=0)  # 입출금자유
    d_bank1 = all_bank.filter(acc_detail=1)  # 예금 / 적금 / 주택청약

    for i in range(len(d_bank0)):
        all_trans = Trans.objects.filter(account_id=d_bank0[i].acc_num)
        for trans in all_trans:
            bank_detail0 += trans.trans_price

    for i in range(len(d_bank1)):
        all_trans = Trans.objects.filter(account_id=d_bank1[i].acc_num)
        for trans in all_trans:
            bank_detail1 += trans.trans_price
    # ========================== detail 값 저장 ==========================

    ## 은행 계좌
    for i in range(len(all_bank)):
        all_trans = Trans.objects.filter(account_id=all_bank[i].acc_num)
        for trans in all_trans:
            bank_total += trans.trans_price


    ## 주식 계좌
    for i in range(len(all_stock)):
        all_trans = Trans.objects.filter(account_id=all_stock[i].acc_num)
        for trans in all_trans:
            stock_total += trans.trans_price
            # 예수금이 들어가 있다면 
            if trans.trans_content.find("예수금") != -1:
                stock_tmp += trans.trans_price

    for i in range(len(all_gold)):
        all_trans = Trans.objects.filter(account_id=all_gold[i].acc_num)
        for trans in all_trans:
            gold_total += trans.trans_price
            # 예수금이 들어가 있다면 
            if trans.trans_content == 'KB금쪽리워드환급':
                goldReward += trans.trans_price

    context = {
        # 값 정보 (파이차트용)
        'bank_total' : bank_total,
        'stock_total' : stock_total,
        'stock_tmp' : stock_tmp,
        'gold_total' : gold_total,
        'goldReward' : goldReward,
        'bank_detail0' : bank_detail0,
        'bank_detail1' : bank_detail1,

        # 계좌 정보 (표 출력용)
        'all_bank' : all_bank,
        'all_stock' : all_stock,
        'all_gold' : all_gold
    }    
    return render(request, 'myAsset.html', context)

# 18. 나의 Gold 확인하기 페이지
def myGold(request):
    return render(request, 'myGold.html')

# 19. 주식 전체 차트 페이지
def stock_charts(request):
    return render(request, 'stock_charts.html')

# 20. 출석체크 페이지
def attendance(request):
    return render(request, 'attendance.html')

# 21. 주식계좌 페이지
def stock_account(request):
    all_accounts = Account.objects.filter(user=request.user)  # 해당 user에 해당하는 계좌 list
    stock_acc = all_accounts.filter(acc_type=1) # user의 증권 계좌

    total_bank0 = []
    for i in range(len(stock_acc)):
        tmp = 0
        all_trans = Trans.objects.filter(account_id=stock_acc[i].acc_num)
        tmp_acc = Account.objects.get(acc_num=stock_acc[i].acc_num)
        for trans in all_trans:
            tmp += trans.trans_price
        total_bank0.append(tmp)
        tmp_acc.total = tmp
        tmp_acc.save()

        
    context = {
        'all_accounts' : stock_acc
    }
    return render(request, 'stock_account.html', context)

def updown_result(request):
    return render(request, 'updown_result.html')
